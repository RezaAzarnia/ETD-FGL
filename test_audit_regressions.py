"""ETD-FGL Scientific Code Audit Regression and Invariant Test Suite.

This module provides exhaustive, offline deterministic tests verifying:
- Issue 1: Production 5D label-free descriptor invariants and degenerate graph handling.
- Issue 2: Aggregator dispatch without broad TypeError suppression.
- Issue 3: Strict FedTGE energy diagnostic validation (no artificial fallback).
- Issue 4: FedTGE edge augmentation determinism, mode support, and invariants.
- Issue 5: Architecture metadata alignment with runtime configuration.
- Issue 6: Experiment provenance and partition integrity validation.
- Issue 8: Production vs historical ablation weight and risk fusion correctness.
- Phase 4: Mathematical correctness of drift, update anomalies, trust mapping, and aggregation.
"""

from __future__ import annotations

from dataclasses import asdict
import json
import math
import tempfile
from pathlib import Path

import numpy as np
import pytest
import torch
import torch.nn as nn
from torch_geometric.data import Data

from build_section4_extra_figures import grouped_bar
from multidata_suite.config import BENCHMARK_METHODS, DatasetConfig
from multidata_suite.core import (
    ExperimentContext,
    _atomic_save_json,
    _file_sha256,
    invoke_aggregator,
    run_method,
    validate_existing_experiment,
)
from multidata_suite.data import (
    create_dirichlet_partition,
    create_partition,
    load_or_create_partition,
)
from multidata_suite.defenses import (
    ETDFGL_DESCRIPTOR_COORDINATES,
    ETDFGL_DESCRIPTOR_DIM,
    ConfigurableETDFGLAggregator,
    ETDFGLAggregator,
    _flatten_delta,
    _graph_descriptor,
    _robust_positive,
    compute_homophily_diagnostics,
)
from multidata_suite.controlled_ablation import (
    CONTROLLED_VARIANTS,
    ControlledAblationETDFGLAggregator,
    ControlledAblationVariant,
    get_equivalent_configurable_params,
    make_scaled_configurable_aggregator,
)
from multidata_suite.fedtge import FedTGEAggregator, _aug_random_edge
from multidata_suite.model import GCN


# ==============================================================================
# Helper fixtures & synthetic graph generators (Offline, no downloads)
# ==============================================================================

def make_synthetic_graph(
    num_nodes: int = 20,
    edge_prob: float = 0.2,
    num_features: int = 8,
    num_classes: int = 3,
    seed: int = 42,
) -> Data:
    """Generate a reproducible synthetic undirected PyG graph for offline testing."""
    rng = np.random.default_rng(seed)
    features = torch.tensor(rng.standard_normal((num_nodes, num_features)), dtype=torch.float32)
    labels = torch.tensor(rng.integers(0, num_classes, size=num_nodes), dtype=torch.long)

    edges = []
    for u in range(num_nodes):
        for v in range(u + 1, num_nodes):
            if rng.uniform() < edge_prob:
                edges.append((u, v))
                edges.append((v, u))

    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    perm = rng.permutation(num_nodes)
    train_mask[perm[: num_nodes // 2]] = True
    val_mask[perm[num_nodes // 2 : 3 * num_nodes // 4]] = True
    test_mask[perm[3 * num_nodes // 4 :]] = True

    data = Data(
        x=features,
        edge_index=edge_index,
        y=labels,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
    )
    return data


# ==============================================================================
# Issue 1: Production 5D Descriptor & Homophily Decoupling
# ==============================================================================

@pytest.mark.unit
def test_production_descriptor_shape_and_coordinates():
    """Verify production _graph_descriptor produces exactly 5 coordinates."""
    graph = make_synthetic_graph()
    desc = _graph_descriptor(graph)
    assert isinstance(desc, np.ndarray)
    assert desc.ndim == 1
    assert desc.shape[0] == 5
    assert ETDFGL_DESCRIPTOR_DIM == 5
    assert len(ETDFGL_DESCRIPTOR_COORDINATES) == 5
    assert np.all(np.isfinite(desc))


@pytest.mark.unit
def test_production_descriptor_strict_label_independence():
    """Verify descriptor values are strictly invariant to node label changes."""
    g1 = make_synthetic_graph(seed=101)
    g2 = g1.clone()
    g2.y = (g2.y + 1) % 3  # Permute all labels

    d1 = _graph_descriptor(g1)
    d2 = _graph_descriptor(g2)
    assert np.allclose(d1, d2, atol=1e-12)


@pytest.mark.unit
def test_production_descriptor_strict_mask_independence():
    """Verify descriptor values are strictly invariant to train/val/test mask changes."""
    g1 = make_synthetic_graph(seed=102)
    g2 = g1.clone()
    g2.train_mask = ~g1.train_mask
    g2.val_mask = torch.zeros_like(g1.val_mask)
    g2.test_mask = torch.zeros_like(g1.test_mask)

    d1 = _graph_descriptor(g1)
    d2 = _graph_descriptor(g2)
    assert np.allclose(d1, d2, atol=1e-12)


@pytest.mark.unit
def test_production_descriptor_degenerate_graphs():
    """Verify descriptor gracefully handles empty, isolated, and single-node graphs."""
    # 1. Empty graph (0 nodes)
    empty_graph = Data(
        x=torch.empty((0, 4)),
        edge_index=torch.empty((2, 0), dtype=torch.long),
        y=torch.empty((0,), dtype=torch.long),
    )
    desc_empty = _graph_descriptor(empty_graph)
    assert desc_empty.shape == (5,)
    assert np.all(np.isfinite(desc_empty))
    assert np.all(desc_empty == 0.0)

    # 2. Single node, no edges
    single_node = Data(
        x=torch.randn((1, 4)),
        edge_index=torch.empty((2, 0), dtype=torch.long),
        y=torch.tensor([0]),
    )
    desc_single = _graph_descriptor(single_node)
    assert desc_single.shape == (5,)
    assert np.all(np.isfinite(desc_single))
    assert np.all(desc_single == 0.0)

    # 3. Disconnected graph with isolated nodes
    isolated = Data(
        x=torch.randn((10, 4)),
        edge_index=torch.empty((2, 0), dtype=torch.long),
        y=torch.zeros(10, dtype=torch.long),
    )
    desc_iso = _graph_descriptor(isolated)
    assert desc_iso.shape == (5,)
    assert np.all(np.isfinite(desc_iso))
    assert np.all(desc_iso == 0.0)


@pytest.mark.unit
def test_historical_homophily_diagnostics_decoupled():
    """Verify compute_homophily_diagnostics returns dict for diagnostics without altering descriptor."""
    g = make_synthetic_graph(seed=103)
    diag = compute_homophily_diagnostics(g)
    assert isinstance(diag, dict)
    assert "homophily" in diag
    assert isinstance(diag["homophily"], float)
    assert 0.0 <= diag["homophily"] <= 1.0
    assert "total_edges" in diag
    assert "homophily_eligible_edges" in diag


# ==============================================================================
# Issue 2: Aggregator Dispatch & Explicit Capability Detection
# ==============================================================================

@pytest.mark.unit
def test_invoke_aggregator_with_diagnostics():
    """Verify aggregator that accepts local_diags receives them properly."""
    received = {}

    def aggregator_with_diags(local_states, counts, global_state, round_number, local_diags=None):
        received["local_diags"] = local_diags
        return global_state, {"agg_diag": 1.0}

    dummy_state = {"w": torch.tensor([1.0])}
    diags = [{"energy": 0.5}, {"energy": 0.7}]
    state, d = invoke_aggregator(
        aggregator_with_diags,
        [dummy_state, dummy_state],
        [10, 10],
        dummy_state,
        1,
        local_diags=diags,
    )
    assert received["local_diags"] == diags
    assert d == {"agg_diag": 1.0}


@pytest.mark.unit
def test_invoke_aggregator_without_diagnostics():
    """Verify aggregator without local_diags parameter is called cleanly without error."""
    def aggregator_without_diags(local_states, counts, global_state, round_number):
        return global_state, {"standard": True}

    dummy_state = {"w": torch.tensor([1.0])}
    diags = [{"energy": 0.5}]
    state, d = invoke_aggregator(
        aggregator_without_diags,
        [dummy_state],
        [10],
        dummy_state,
        1,
        local_diags=diags,
    )
    assert d == {"standard": True}


@pytest.mark.unit
def test_invoke_aggregator_propagates_internal_typeerror():
    """Verify internal TypeError inside aggregator is NOT swallowed or retried."""
    def buggy_aggregator(local_states, counts, global_state, round_number, local_diags=None):
        # Internal code bug: trying to add int and str
        _ = 1 + "crash"
        return global_state, {}

    dummy_state = {"w": torch.tensor([1.0])}
    with pytest.raises(TypeError, match="unsupported operand type"):
        invoke_aggregator(
            buggy_aggregator,
            [dummy_state],
            [10],
            dummy_state,
            1,
            local_diags=[{}],
        )


@pytest.mark.unit
def test_invoke_aggregator_invalid_output_type():
    """Verify non-tuple return raises ValueError."""
    def bad_aggregator(local_states, counts, global_state, round_number):
        return "invalid_return_value"

    dummy_state = {"w": torch.tensor([1.0])}
    with pytest.raises(ValueError, match="must return a tuple"):
        invoke_aggregator(
            bad_aggregator,
            [dummy_state],
            [10],
            dummy_state,
            1,
        )


# ==============================================================================
# Issue 3: FedTGE Energy Diagnostics Validation
# ==============================================================================

@pytest.mark.unit
def test_fedtge_aggregator_rejects_missing_diags():
    """Verify FedTGEAggregator raises ValueError when local_diags is None."""
    agg = FedTGEAggregator()
    dummy_state = {"w": torch.tensor([1.0])}
    with pytest.raises(ValueError, match="requires client diagnostics"):
        agg([dummy_state, dummy_state], [10, 10], dummy_state, 1, local_diags=None)


@pytest.mark.unit
def test_fedtge_aggregator_rejects_mismatched_client_count():
    """Verify FedTGEAggregator raises ValueError when local_diags length differs."""
    agg = FedTGEAggregator()
    dummy_state = {"w": torch.tensor([1.0])}
    with pytest.raises(ValueError, match="expected 2 client diagnostics"):
        agg(
            [dummy_state, dummy_state],
            [10, 10],
            dummy_state,
            1,
            local_diags=[{"energy_vector": np.array([1.0])}],
        )


@pytest.mark.unit
def test_fedtge_aggregator_rejects_missing_energy_vector_key():
    """Verify FedTGEAggregator raises ValueError if energy_vector key is missing."""
    agg = FedTGEAggregator()
    dummy_state = {"w": torch.tensor([1.0])}
    with pytest.raises(ValueError, match="missing required 'energy_vector'"):
        agg(
            [dummy_state, dummy_state],
            [10, 10],
            dummy_state,
            1,
            local_diags=[{"other": 1}, {"energy_vector": np.array([1.0])}],
        )


@pytest.mark.unit
def test_fedtge_aggregator_rejects_nan_or_inf_energy():
    """Verify FedTGEAggregator raises ValueError on NaN or Inf energy values."""
    agg = FedTGEAggregator()
    dummy_state = {"w": torch.tensor([1.0])}
    nan_diags = [
        {"energy_vector": np.array([np.nan, 1.0])},
        {"energy_vector": np.array([1.0, 2.0])},
    ]
    with pytest.raises(ValueError, match="NaN or infinite"):
        agg([dummy_state, dummy_state], [10, 10], dummy_state, 1, local_diags=nan_diags)

    inf_diags = [
        {"energy_vector": np.array([np.inf, 1.0])},
        {"energy_vector": np.array([1.0, 2.0])},
    ]
    with pytest.raises(ValueError, match="NaN or infinite"):
        agg([dummy_state, dummy_state], [10, 10], dummy_state, 1, local_diags=inf_diags)


@pytest.mark.unit
def test_fedtge_aggregator_valid_run():
    """Verify FedTGEAggregator succeeds with clean, valid energy vectors."""
    agg = FedTGEAggregator()
    state0 = {"layer.weight": torch.tensor([[1.0, 2.0]])}
    state1 = {"layer.weight": torch.tensor([[3.0, 4.0]])}
    global_state = {"layer.weight": torch.tensor([[0.0, 0.0]])}
    valid_diags = [
        {"energy_vector": np.array([0.5, 0.2, 0.1])},
        {"energy_vector": np.array([0.4, 0.3, 0.2])},
    ]
    new_state, diags = agg(
        [state0, state1],
        [10, 10],
        global_state,
        1,
        local_diags=valid_diags,
    )
    assert isinstance(new_state, dict)
    assert "fedtge_num_selected_clients" in diags


# ==============================================================================
# Issue 4: FedTGE Augmentation Determinism & Edge Invariants
# ==============================================================================

@pytest.mark.unit
def test_aug_random_edge_determinism():
    """Verify _aug_random_edge is deterministic when seed is provided."""
    g = make_synthetic_graph(num_nodes=30, edge_prob=0.3, seed=201)

    aug1 = _aug_random_edge(g.num_nodes, g.edge_index, seed=999)
    aug2 = _aug_random_edge(g.num_nodes, g.edge_index, seed=999)

    assert torch.equal(aug1, aug2)


@pytest.mark.unit
def test_aug_random_edge_node_index_bounds():
    """Verify augmented edges never exceed valid node range [0, num_nodes - 1]."""
    g = make_synthetic_graph(num_nodes=25, edge_prob=0.2, seed=202)
    aug = _aug_random_edge(g.num_nodes, g.edge_index, seed=1234)

    assert aug.min() >= 0
    assert aug.max() < g.num_nodes


@pytest.mark.unit
def test_aug_random_edge_percentage_mode_sensitivity():
    """Verify perturb_percent changes number of modified edges in percentage mode."""
    g = make_synthetic_graph(num_nodes=50, edge_prob=0.2, seed=203)

    aug_low = _aug_random_edge(g.num_nodes, g.edge_index, perturb_percent=0.05, mode="percentage", seed=42)
    aug_high = _aug_random_edge(g.num_nodes, g.edge_index, perturb_percent=0.40, mode="percentage", seed=42)

    assert not torch.equal(aug_low, aug_high)


# ==============================================================================
# Issue 5: Runtime Architecture vs Metadata Alignment
# ==============================================================================

@pytest.mark.unit
def test_gcn_architecture_runtime_parameters():
    """Verify GCN hidden dimension and parameter structure matches configuration."""
    cfg = DatasetConfig(key="cora", display_name="Cora", hidden_channels=32, dropout=0.5)
    model = GCN(input_channels=1433, hidden_channels=cfg.hidden_channels, output_channels=7, dropout=cfg.dropout)

    assert model.conv1.out_channels == 32
    assert model.conv2.in_channels == 32
    assert model.conv2.out_channels == 7
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    expected_params = (1433 * 32 + 32) + (32 * 7 + 7)
    assert total_params == expected_params


# ==============================================================================
# Issue 6: Result Reuse & Partition Manifest Validation
# ==============================================================================

@pytest.mark.unit
def test_validate_existing_experiment_guards():
    """Verify validate_existing_experiment rejects corrupted or mismatched runs."""
    class MockContext:
        def __init__(self, base_output: Path, config: DatasetConfig):
            self.base_output = base_output
            self.config = config

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cfg = DatasetConfig(key="cora", display_name="Cora", seed=42, rounds=50, local_epochs=3)
        context = MockContext(tmp_path, cfg)
        slug = "test_method"
        method_dir = tmp_path / slug

        # 1. Non-existent summary
        assert validate_existing_experiment(context, slug) is None

        # 2. Corrupted 0-byte file
        method_dir.mkdir(parents=True, exist_ok=True)
        summary_file = method_dir / "final_summary.json"
        summary_file.write_text("")
        assert validate_existing_experiment(context, slug) is None

        # 3. Invalid JSON content
        summary_file.write_text("{ incomplete json")
        assert validate_existing_experiment(context, slug) is None

        # 4. Valid JSON but missing required checkpoint / history files
        from dataclasses import asdict
        valid_data = {
            "dataset": "Cora",
            "method": "test_method",
            "output_slug": "test_method",
            "config": asdict(cfg),
            "final_metrics": {"clean_test_acc": 0.8},
            "best_round": 10,
        }
        _atomic_save_json(valid_data, summary_file)
        assert validate_existing_experiment(context, slug) is None  # Fails because checkpoint is missing

        # 5. Create valid checkpoint and history files -> Now passes
        torch.save(
            {"model_state_dict": {"conv1.weight": torch.randn(32, 1433), "conv2.weight": torch.randn(7, 32)}},
            method_dir / "best_model.pt",
        )
        (method_dir / "training_history.csv").write_text("round,clean_test_acc,attack_success_rate\n0,0.5,0.1\n")
        assert validate_existing_experiment(context, slug) is not None

        # 6. Seed mismatch in requested cfg -> Fails validation
        cfg_mismatched = DatasetConfig(key="cora", display_name="Cora", seed=43, rounds=50, local_epochs=3)
        context_mismatched = MockContext(tmp_path, cfg_mismatched)
        assert validate_existing_experiment(context_mismatched, slug) is None


@pytest.mark.unit
def test_partition_validation_and_caching():
    """Verify load_or_create_partition validates cached node count and parameters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        cfg = DatasetConfig(key="synthetic", display_name="Synthetic", num_clients=3, seed=42)
        graph = make_synthetic_graph(num_nodes=30, seed=301)

        # Generate and save partition
        p1 = load_or_create_partition(
            project_dir,
            cfg,
            graph,
            num_classes=3,
            base_output=project_dir / "outputs",
            strategy="iid",
        )
        assert len(p1) == 3
        total_nodes = sum(len(c) for c in p1.values())
        assert total_nodes == 30

        # Load from valid cache
        p2 = load_or_create_partition(
            project_dir,
            cfg,
            graph,
            num_classes=3,
            base_output=project_dir / "outputs",
            strategy="iid",
        )
        for client_id in p1:
            assert torch.equal(p1[client_id], p2[client_id])

        # Changing seed regenerates rather than reusing wrong cache
        cfg_seed = DatasetConfig(key="synthetic", display_name="Synthetic", num_clients=3, seed=99)
        p_seed = load_or_create_partition(
            project_dir,
            cfg_seed,
            graph,
            num_classes=3,
            base_output=project_dir / "outputs",
            strategy="iid",
        )
        assert len(p_seed) == 3


# ==============================================================================
# Issue 7: Central Method Registry
# ==============================================================================

@pytest.mark.unit
def test_benchmark_methods_registry():
    """Verify all 8 benchmark methods are present in the central registry."""
    slugs = [slug for _, slug in BENCHMARK_METHODS]
    assert "fedavg_clean" in slugs
    assert "fedavg_structural_backdoor" in slugs
    assert "baseline_pdfl" in slugs
    assert "baseline_gsp" in slugs
    assert "baseline_flpurifier" in slugs
    assert "baseline_dmgnn" in slugs
    assert "baseline_fedtge" in slugs
    assert "defended_etdfgl" in slugs
    assert len(BENCHMARK_METHODS) == 8


# ==============================================================================
# Issue 8: Component Weights & Risk Fusion Verification
# ==============================================================================

@pytest.mark.unit
def test_production_aggregator_weights_frozen():
    """Verify production ETDFGLAggregator strictly fixes topology 9/13, update 4/13, explanation 0."""
    clean_graphs = [make_synthetic_graph(seed=i) for i in range(3)]
    current_graphs = [g.clone() for g in clean_graphs]

    agg = ETDFGLAggregator(clean_graphs, current_graphs)
    assert math.isclose(agg.ALPHA_TOPOLOGY, 9.0 / 13.0, rel_tol=1e-12)
    assert math.isclose(agg.ALPHA_UPDATE, 4.0 / 13.0, rel_tol=1e-12)
    assert agg.ALPHA_EXPLANATION == 0.0
    assert math.isclose(agg.ALPHA_TOPOLOGY + agg.ALPHA_UPDATE + agg.ALPHA_EXPLANATION, 1.0, rel_tol=1e-12)


@pytest.mark.unit
def test_configurable_aggregator_ablation_variants():
    """Verify ConfigurableETDFGLAggregator isolates components correctly."""
    clean_graphs = [make_synthetic_graph(seed=i) for i in range(3)]
    current_graphs = [g.clone() for g in clean_graphs]

    # 1. Default matches production
    default_agg = ConfigurableETDFGLAggregator(clean_graphs, current_graphs)
    assert math.isclose(default_agg.component_weights[0], 9.0 / 13.0, rel_tol=1e-12)
    assert math.isclose(default_agg.component_weights[1], 0.0, abs_tol=1e-12)
    assert math.isclose(default_agg.component_weights[2], 4.0 / 13.0, rel_tol=1e-12)
    assert default_agg.use_trust_weighting is True

    # 2. Topology-only ablation (update = 0)
    topo_agg = ConfigurableETDFGLAggregator(
        clean_graphs, current_graphs, topology_weight=1.0, explanation_weight=0.0, update_weight=0.0
    )
    assert math.isclose(topo_agg.component_weights[0], 1.0, rel_tol=1e-12)
    assert topo_agg.component_weights[1] == 0.0
    assert topo_agg.component_weights[2] == 0.0

    # 3. Update-only ablation (topology = 0)
    upd_agg = ConfigurableETDFGLAggregator(
        clean_graphs, current_graphs, topology_weight=0.0, explanation_weight=0.0, update_weight=1.0
    )
    assert upd_agg.component_weights[0] == 0.0
    assert upd_agg.component_weights[1] == 0.0
    assert math.isclose(upd_agg.component_weights[2], 1.0, rel_tol=1e-12)

    # 4. No-trust ablation
    notrust_agg = ConfigurableETDFGLAggregator(
        clean_graphs, current_graphs, use_trust_weighting=False
    )
    assert notrust_agg.use_trust_weighting is False

    # 5. Historical three-channel variant
    hist_agg = ConfigurableETDFGLAggregator(
        clean_graphs,
        current_graphs,
        topology_weight=0.45,
        explanation_weight=0.35,
        update_weight=0.20,
    )
    assert math.isclose(hist_agg.component_weights[0], 0.45, rel_tol=1e-12)
    assert math.isclose(hist_agg.component_weights[1], 0.35, rel_tol=1e-12)
    assert math.isclose(hist_agg.component_weights[2], 0.20, rel_tol=1e-12)


# ==============================================================================
# Phase 4: Mathematical Operations Correctness
# ==============================================================================

@pytest.mark.unit
def test_robust_positive_scaling():
    """Verify _robust_positive median-absolute-deviation scaling and non-negativity."""
    values = np.array([1.0, 2.0, 2.0, 3.0, 10.0])
    scaled = _robust_positive(values)
    assert isinstance(scaled, np.ndarray)
    assert np.all(scaled >= 0.0)
    assert np.all(np.isfinite(scaled))
    # Outlier at index 4 must have the largest score
    assert np.argmax(scaled) == 4


@pytest.mark.unit
def test_flatten_delta_and_update_anomaly():
    """Verify model parameter flattening and coordinate-wise median subtraction."""
    g_state = {"w": torch.zeros((2, 2)), "b": torch.zeros(2)}
    l_state1 = {"w": torch.ones((2, 2)), "b": torch.ones(2)}
    l_state2 = {"w": torch.full((2, 2), 2.0), "b": torch.full((2,), 2.0)}

    delta1 = _flatten_delta(l_state1, g_state)
    delta2 = _flatten_delta(l_state2, g_state)

    assert delta1.shape == (6,)  # 4 + 2
    assert delta2.shape == (6,)
    assert torch.allclose(delta1, torch.ones(6))
    assert torch.allclose(delta2, torch.full((6,), 2.0))


@pytest.mark.unit
def test_trust_weight_normalization_and_clipping():
    """Verify trust clipping [0.02, 1.0] and weight normalization to 1.0."""
    clean_graphs = [make_synthetic_graph(seed=i) for i in range(3)]
    current_graphs = [g.clone() for g in clean_graphs]
    agg = ETDFGLAggregator(clean_graphs, current_graphs)

    # Synthetic client states: client 0 benign, client 1 benign, client 2 huge outlier
    global_s = {"w": torch.zeros(4)}
    s0 = {"w": torch.tensor([0.1, 0.1, 0.1, 0.1])}
    s1 = {"w": torch.tensor([0.1, 0.1, 0.1, 0.1])}
    s2 = {"w": torch.tensor([100.0, 100.0, 100.0, 100.0])}

    aggregated, diags = agg([s0, s1, s2], [100, 100, 100], global_s, 1)

    t0 = diags["etdfgl_trust_client_0"]
    t1 = diags["etdfgl_trust_client_1"]
    t2 = diags["etdfgl_trust_client_2"]
    w0 = diags["etdfgl_weight_client_0"]
    w1 = diags["etdfgl_weight_client_1"]
    w2 = diags["etdfgl_weight_client_2"]

    # Bounds
    assert 0.02 <= t0 <= 1.0
    assert 0.02 <= t1 <= 1.0
    assert 0.02 <= t2 <= 1.0
    # Outlier client 2 must have strictly lower trust
    assert t2 < t0
    # Weights sum to 1.0
    assert math.isclose(w0 + w1 + w2, 1.0, rel_tol=1e-6)


# ==============================================================================
# Second-Pass Audit Regressions (Fixes 3, 4, 5, 6, 7)
# ==============================================================================

@pytest.mark.unit
def test_validate_existing_experiment_adversarial_rejections():
    """Verify validate_existing_experiment rejects corrupted or mismatched runs (Fix 3)."""
    class MockContext:
        def __init__(self, base_output: Path, config: DatasetConfig):
            self.base_output = base_output
            self.config = config

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cfg = DatasetConfig(key="cora", display_name="Cora", seed=42, rounds=50, local_epochs=3)
        context = MockContext(tmp_path, cfg)
        slug = "defended_etdfgl"
        method_dir = tmp_path / slug
        method_dir.mkdir(parents=True, exist_ok=True)

        def make_valid_files():
            valid_summary = {
                "dataset": "Cora",
                "method": "defended_etdfgl",
                "output_slug": "defended_etdfgl",
                "config": asdict(cfg),
                "final_metrics": {"clean_test_acc": 0.8},
                "best_round": 10,
            }
            _atomic_save_json(valid_summary, method_dir / "final_summary.json")
            torch.save(
                {"model_state_dict": {"conv1.weight": torch.randn(32, 1433), "conv2.weight": torch.randn(7, 32)}},
                method_dir / "best_model.pt",
            )
            (method_dir / "training_history.csv").write_text("round,clean_test_acc,attack_success_rate\n0,0.5,0.1\n")

        # 1. Base valid passes
        make_valid_files()
        assert validate_existing_experiment(context, slug, expected_method_name="defended_etdfgl") is not None

        # 2. Wrong method name rejected
        assert validate_existing_experiment(context, slug, expected_method_name="fedavg_clean") is None

        # 3. Missing config key rejected
        summary = json.loads((method_dir / "final_summary.json").read_text(encoding="utf-8"))
        del summary["config"]["poison_rate"]
        _atomic_save_json(summary, method_dir / "final_summary.json")
        assert validate_existing_experiment(context, slug) is None

        # 4. Incompatible architectural config rejected
        make_valid_files()
        summary = json.loads((method_dir / "final_summary.json").read_text(encoding="utf-8"))
        summary["config"]["hidden_channels"] = 64
        _atomic_save_json(summary, method_dir / "final_summary.json")
        assert validate_existing_experiment(context, slug) is None

        # 5. Garbage checkpoint bytes safely rejected without crash
        make_valid_files()
        (method_dir / "best_model.pt").write_bytes(b"corrupted garbage bytes not torch")
        assert validate_existing_experiment(context, slug) is None

        # 6. Checkpoint without conv layers rejected
        make_valid_files()
        torch.save({"model_state_dict": {"linear.weight": torch.randn(10, 10)}}, method_dir / "best_model.pt")
        assert validate_existing_experiment(context, slug) is None

        # 7. Checkpoint with empty state_dict rejected
        make_valid_files()
        torch.save({"model_state_dict": {}}, method_dir / "best_model.pt")
        assert validate_existing_experiment(context, slug) is None

        # 8. Empty history CSV rejected
        make_valid_files()
        (method_dir / "training_history.csv").write_text("round,clean_test_acc\n")
        assert validate_existing_experiment(context, slug) is None

        # 9. History CSV missing 'round' column rejected
        make_valid_files()
        (method_dir / "training_history.csv").write_text("epoch,loss\n0,0.5\n")
        assert validate_existing_experiment(context, slug) is None

        # 10. Manifest checksum mismatch rejected
        make_valid_files()
        manifest = {
            "checkpoint_sha256": "wrong_sha256_hash",
            "history_sha256": _file_sha256(method_dir / "training_history.csv"),
        }
        _atomic_save_json(manifest, method_dir / "experiment_manifest.json")
        assert validate_existing_experiment(context, slug) is None


@pytest.mark.unit
def test_run_method_fail_closed_on_existing_outputs():
    """Verify run_method fails closed when output files already exist and force=False (Fix 4)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cfg = DatasetConfig(key="cora", display_name="Cora", seed=42, rounds=2, local_epochs=1)

        # Create dummy context
        graph = make_synthetic_graph(num_nodes=10)
        context = ExperimentContext(
            project_dir=tmp_path,
            config=cfg,
            data_cpu=graph,
            num_features=8,
            num_classes=3,
            metadata={},
            clean_graphs_cpu=[graph],
            attacked_graphs_cpu=[graph],
            attack_metadata={},
            device=torch.device("cpu"),
            triggered_data=graph,
            victim_nodes=torch.tensor([0, 1]),
            base_output_override=tmp_path,
        )

        slug = "test_run_slug"
        out_dir = tmp_path / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        summary_file = out_dir / "final_summary.json"
        summary_file.write_text("existing_data", encoding="utf-8")

        # Calling run_method with force=False must raise RuntimeError
        with pytest.raises(RuntimeError, match="Automatic overwrite without authorization is prohibited"):
            run_method(
                context=context,
                method_name="FedAvg",
                output_slug=slug,
                client_graphs_cpu=[graph],
                force=False,
            )

        # Verify existing file was not modified
        assert summary_file.read_text(encoding="utf-8") == "existing_data"


@pytest.mark.unit
def test_partition_duplicate_and_missing_nodes_adversarial():
    """Adversarial reproduction of Fix 5: duplicate and missing node indices in partition cache."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        cfg = DatasetConfig(key="synthetic", display_name="Synthetic", num_clients=3, seed=42)
        graph = make_synthetic_graph(num_nodes=6, seed=501)

        cache_dir = project_dir / "outputs" / "partitions"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / "synthetic_iid_c3_seed42.pt"

        # Direct adversarial reproduction: clients [0,1], [2,3], [3,4]
        # Total nodes is 6, sum of lengths is 6, but node 3 is duplicated and node 5 is missing!
        adversarial_partition = {
            0: torch.tensor([0, 1], dtype=torch.long),
            1: torch.tensor([2, 3], dtype=torch.long),
            2: torch.tensor([3, 4], dtype=torch.long),
        }
        torch.save(
            {
                "partition": adversarial_partition,
                "strategy": "iid",
                "alpha": 0.5,
                "num_clients": 3,
                "seed": 42,
                "dataset": "synthetic",
            },
            cache_path,
        )

        # load_or_create_partition must reject this corrupted cache and recompute
        partition = load_or_create_partition(
            project_dir,
            cfg,
            graph,
            num_classes=3,
            base_output=project_dir / "outputs",
            strategy="iid",
        )
        assert len(partition) == 3
        all_nodes = torch.cat(list(partition.values()))
        assert all_nodes.numel() == 6
        assert torch.unique(all_nodes).numel() == 6
        assert set(all_nodes.tolist()) == set(range(6))

        # Adversarial test 2: Out of bounds node index (e.g. node 99 in 6-node graph)
        oob_partition = {
            0: torch.tensor([0, 1], dtype=torch.long),
            1: torch.tensor([2, 3], dtype=torch.long),
            2: torch.tensor([4, 99], dtype=torch.long),
        }
        torch.save(
            {
                "partition": oob_partition,
                "strategy": "iid",
                "alpha": 0.5,
                "num_clients": 3,
                "seed": 42,
                "dataset": "synthetic",
            },
            cache_path,
        )
        partition_oob = load_or_create_partition(
            project_dir,
            cfg,
            graph,
            num_classes=3,
            base_output=project_dir / "outputs",
            strategy="iid",
        )
        all_nodes_oob = torch.cat(list(partition_oob.values()))
        assert all_nodes_oob.max().item() < 6

        # Adversarial test 3: Missing client ID (e.g. client 2 missing)
        missing_client_partition = {
            0: torch.tensor([0, 1, 2], dtype=torch.long),
            1: torch.tensor([3, 4, 5], dtype=torch.long),
        }
        torch.save(
            {
                "partition": missing_client_partition,
                "strategy": "iid",
                "alpha": 0.5,
                "num_clients": 3,
                "seed": 42,
                "dataset": "synthetic",
            },
            cache_path,
        )
        partition_mc = load_or_create_partition(
            project_dir,
            cfg,
            graph,
            num_classes=3,
            base_output=project_dir / "outputs",
            strategy="iid",
        )
        assert set(partition_mc.keys()) == {0, 1, 2}


@pytest.mark.unit
def test_build_section4_extra_figures_fedtge_optional():
    """Verify build_section4_extra_figures.grouped_bar runs cleanly without FedTGE (Fix 6)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir)

        # 1. Synthetic results without FedTGE (reproducing independent audit test)
        results_without_fedtge = {
            "cora": {
                "Clean FedAvg": {"clean_test_acc": "0.81", "asr": "0.02"},
                "Attacked FedAvg": {"clean_test_acc": "0.80", "asr": "0.95"},
                "PD-FL": {"clean_test_acc": "0.79", "asr": "0.10"},
                "GSP-FL": {"clean_test_acc": "0.78", "asr": "0.15"},
                "FLPurifier-GNN": {"clean_test_acc": "0.77", "asr": "0.08"},
                "DMGNN-FL": {"clean_test_acc": "0.80", "asr": "0.05"},
                "ETD-FGL": {"clean_test_acc": "0.81", "asr": "0.01"},
            },
            "pubmed": {
                "Clean FedAvg": {"clean_test_acc": "0.78", "asr": "0.03"},
                "Attacked FedAvg": {"clean_test_acc": "0.77", "asr": "0.92"},
                "PD-FL": {"clean_test_acc": "0.76", "asr": "0.12"},
                "GSP-FL": {"clean_test_acc": "0.75", "asr": "0.14"},
                "FLPurifier-GNN": {"clean_test_acc": "0.74", "asr": "0.09"},
                "DMGNN-FL": {"clean_test_acc": "0.77", "asr": "0.06"},
                "ETD-FGL": {"clean_test_acc": "0.78", "asr": "0.02"},
            },
        }

        # Must NOT throw KeyError('FedTGE')
        grouped_bar(
            results_without_fedtge,
            metric="clean_test_acc",
            ylabel="Accuracy",
            stem="fig_no_fedtge",
            caption="Accuracy comparison without FedTGE.",
            output_dir=out_dir,
            include_clean=True,
        )
        assert (out_dir / "fig_no_fedtge.png").is_file()
        assert (out_dir / "fig_no_fedtge_caption.txt").is_file()

        # 2. Results WITH FedTGE
        results_with_fedtge = {
            k: {**v, "FedTGE": {"clean_test_acc": "0.79", "asr": "0.04"}}
            for k, v in results_without_fedtge.items()
        }
        grouped_bar(
            results_with_fedtge,
            metric="clean_test_acc",
            ylabel="Accuracy",
            stem="fig_with_fedtge",
            caption="Accuracy comparison with FedTGE.",
            output_dir=out_dir,
            include_clean=False,
        )
        assert (out_dir / "fig_with_fedtge.png").is_file()

        # 3. Empty results returns without error
        grouped_bar(
            {},
            metric="clean_test_acc",
            ylabel="Accuracy",
            stem="fig_empty",
            caption="Empty",
            output_dir=out_dir,
            include_clean=True,
        )


@pytest.mark.unit
def test_aug_random_edge_percentage_mode_boundaries_and_modes():
    """Verify FedTGE _aug_random_edge boundary conditions and error handling (Fix 7)."""
    g = make_synthetic_graph(num_nodes=20, edge_prob=0.3, seed=701)

    # 1. perturb_percent=0.0 in percentage mode returns exact clone (0 edges added or deleted)
    aug_zero = _aug_random_edge(g.num_nodes, g.edge_index, perturb_percent=0.0, mode="percentage", seed=42)
    assert torch.equal(aug_zero, g.edge_index)

    # 2. perturb_percent=0.20 in percentage mode produces valid graph within node universe
    aug_twenty = _aug_random_edge(g.num_nodes, g.edge_index, perturb_percent=0.20, mode="percentage", seed=42)
    assert aug_twenty.min() >= 0
    assert aug_twenty.max() < g.num_nodes

    # 3. Negative perturb_percent raises ValueError
    with pytest.raises(ValueError, match="perturb_percent must be in"):
        _aug_random_edge(g.num_nodes, g.edge_index, perturb_percent=-0.05, mode="percentage")

    # 4. Out-of-bounds perturb_percent (> 1.0) raises ValueError
    with pytest.raises(ValueError, match="perturb_percent must be in"):
        _aug_random_edge(g.num_nodes, g.edge_index, perturb_percent=1.05, mode="percentage")

    # 5. Unsupported mode raises ValueError
    with pytest.raises(ValueError, match="Unsupported.*mode"):
        _aug_random_edge(g.num_nodes, g.edge_index, mode="unsupported_mode")

    # 6. Default official_degree mode remains bitwise-equivalent for identical seed
    aug_deg1 = _aug_random_edge(g.num_nodes, g.edge_index, mode="official_degree", seed=123)
    aug_deg2 = _aug_random_edge(g.num_nodes, g.edge_index, mode="official_degree", seed=123)
    assert torch.equal(aug_deg1, aug_deg2)


# ==============================================================================
# Legend & Method-to-Color Consistency Verification (ASR Panel Alignment)
# ==============================================================================

@pytest.mark.unit
def test_method_colors_mapping_completeness_and_uniqueness():
    """Verify METHOD_COLORS defines valid, unique colors for all 8 benchmark methods."""
    import matplotlib.colors as mcolors
    from multidata_suite.config import BENCHMARK_METHODS, METHOD_COLORS

    # 1. All 8 methods must be present
    assert len(BENCHMARK_METHODS) == 8
    for method_name, _ in BENCHMARK_METHODS:
        assert method_name in METHOD_COLORS, f"Missing color for method: {method_name}"

    # 2. All color strings must be valid matplotlib colors
    parsed_colors = []
    for method_name, color_str in METHOD_COLORS.items():
        assert isinstance(color_str, str)
        assert color_str.startswith("#")
        rgba = mcolors.to_rgba(color_str)
        assert len(rgba) == 4
        parsed_colors.append(rgba)

    # 3. All 8 methods must have mutually distinct colors
    assert len(set(parsed_colors)) == 8, "Expected 8 mutually distinct colors for 8 benchmark methods"


@pytest.mark.unit
def test_multipanel_figure_color_consistency_and_asr_alignment():
    """Verify ASR panel curves match the shared legend colors and do not suffer cycle shift."""
    import matplotlib.colors as mcolors
    import matplotlib.pyplot as plt
    from build_real_comparisons_and_figures import MARKERS, STYLES
    from multidata_suite.config import BENCHMARK_METHODS, METHOD_COLORS

    # Synthetic setup for all 8 active methods
    active_methods = list(BENCHMARK_METHODS)
    method_idx_map = {m[0]: i for i, m in enumerate(BENCHMARK_METHODS)}

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0))
    metrics = [
        ("test_accuracy", "Clean test accuracy", "(a) Clean accuracy", True),
        ("attack_success_rate", "Attack success rate", "(b) ASR", False),
        ("mean_client_loss", "Mean client loss", "(c) Training loss", True),
    ]

    for axis, (metric, ylabel, title, include_clean) in zip(axes.flat[:3], metrics):
        for method, _ in active_methods:
            idx = method_idx_map[method]
            if not include_clean and method == "Clean FedAvg":
                continue
            x = [0, 1, 2]
            y = [0.5, 0.6, 0.7]
            axis.plot(
                x,
                y,
                label=method,
                color=METHOD_COLORS[method],
                linestyle=STYLES[idx],
                marker=MARKERS[idx],
            )

    # Extract plotted lines from accuracy panel (axes[0, 0]) and ASR panel (axes[0, 1])
    acc_lines = {line.get_label(): line for line in axes[0, 0].get_lines()}
    asr_lines = {line.get_label(): line for line in axes[0, 1].get_lines()}

    # 1. Clean FedAvg is present in accuracy panel but excluded from ASR panel
    assert "Clean FedAvg" in acc_lines
    assert "Clean FedAvg" not in asr_lines
    assert len(acc_lines) == 8
    assert len(asr_lines) == 7

    # 2. For every method in ASR panel, line color must exactly equal METHOD_COLORS[method]
    for method_name, line in asr_lines.items():
        expected_color = mcolors.to_rgba(METHOD_COLORS[method_name])
        actual_color = mcolors.to_rgba(line.get_color())
        assert actual_color == expected_color, f"Color mismatch for {method_name} on ASR panel"

    # 3. Direct verification of the specific reported bug:
    # Attacked FedAvg in ASR panel MUST NOT have Clean FedAvg's color (blue)
    attacked_asr_color = mcolors.to_rgba(asr_lines["Attacked FedAvg"].get_color())
    clean_color = mcolors.to_rgba(METHOD_COLORS["Clean FedAvg"])
    expected_attacked_color = mcolors.to_rgba(METHOD_COLORS["Attacked FedAvg"])

    assert attacked_asr_color == expected_attacked_color
    assert attacked_asr_color != clean_color

    # 4. ETD-FGL in ASR panel matches ETD-FGL in accuracy panel and legend
    etdfgl_asr_color = mcolors.to_rgba(asr_lines["ETD-FGL"].get_color())
    etdfgl_acc_color = mcolors.to_rgba(acc_lines["ETD-FGL"].get_color())
    assert etdfgl_asr_color == etdfgl_acc_color == mcolors.to_rgba(METHOD_COLORS["ETD-FGL"])

    # 5. Shared legend labels and handles strictly match
    handles, labels = axes[0, 0].get_legend_handles_labels()
    for handle, label in zip(handles, labels):
        assert mcolors.to_rgba(handle.get_color()) == mcolors.to_rgba(METHOD_COLORS[label])

    plt.close(fig)


@pytest.mark.unit
def test_color_invariance_when_fedtge_absent():
    """Verify method colors remain invariant and unshifted when optional FedTGE is omitted."""
    import matplotlib.colors as mcolors
    import matplotlib.pyplot as plt
    from build_real_comparisons_and_figures import MARKERS, STYLES
    from multidata_suite.config import BENCHMARK_METHODS, METHOD_COLORS

    # Simulate run without optional FedTGE (7 methods)
    active_without_fedtge = [m for m in BENCHMARK_METHODS if m[0] != "FedTGE"]
    assert len(active_without_fedtge) == 7

    method_idx_map = {m[0]: i for i, m in enumerate(BENCHMARK_METHODS)}

    fig, axes = plt.subplots(1, 2)
    for method, _ in active_without_fedtge:
        idx = method_idx_map[method]
        # Accuracy panel (includes Clean FedAvg)
        axes[0].plot([0, 1], [0.5, 0.6], label=method, color=METHOD_COLORS[method], linestyle=STYLES[idx], marker=MARKERS[idx])
        # ASR panel (excludes Clean FedAvg)
        if method != "Clean FedAvg":
            axes[1].plot([0, 1], [0.5, 0.6], label=method, color=METHOD_COLORS[method], linestyle=STYLES[idx], marker=MARKERS[idx])

    acc_lines = {line.get_label(): line for line in axes[0].get_lines()}
    asr_lines = {line.get_label(): line for line in axes[1].get_lines()}

    # Assert ETD-FGL color is NOT shifted by the absence of FedTGE
    assert mcolors.to_rgba(acc_lines["ETD-FGL"].get_color()) == mcolors.to_rgba(METHOD_COLORS["ETD-FGL"])
    assert mcolors.to_rgba(asr_lines["ETD-FGL"].get_color()) == mcolors.to_rgba(METHOD_COLORS["ETD-FGL"])

    # Assert Attacked FedAvg color is NOT shifted by the absence of Clean FedAvg on ASR
    assert mcolors.to_rgba(asr_lines["Attacked FedAvg"].get_color()) == mcolors.to_rgba(METHOD_COLORS["Attacked FedAvg"])

    plt.close(fig)


@pytest.mark.unit
def test_purify_explanation_guided_instrumentation():
    """Verify purify_explanation_guided instrumentation, diagnostic reporting, and attributes."""
    from multidata_suite.defenses import purify_explanation_guided
    from multidata_suite.model import GCN

    torch.manual_seed(42)
    num_nodes = 20
    x = torch.randn(num_nodes, 16)
    edge_index = torch.tensor([[0, 1, 1, 2, 2, 3], [1, 0, 2, 1, 3, 2]], dtype=torch.long)
    y = torch.zeros(num_nodes, dtype=torch.long)
    train_mask = torch.ones(num_nodes, dtype=torch.bool)
    data = Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask)

    model = GCN(16, 8, 3, 0.0)
    model.eval()

    purified = purify_explanation_guided(
        model=model,
        data=data,
        target_class=0,
        trigger_size=3,
        client_id=0,
        verbose=False,
    )

    assert hasattr(purified, "num_removed_edges")
    assert isinstance(purified.num_removed_edges, int)
    assert hasattr(purified, "purification_diagnostics")
    diag = purified.purification_diagnostics
    assert diag["client_id"] == 0
    assert "num_candidates" in diag
    assert "num_removed_edges" in diag
    assert "candidate_nodes" in diag
    assert isinstance(diag["candidate_nodes"], list)


@pytest.mark.unit
def test_fig_11_negative_values_and_zero_line():
    """Verify Fig_11 properly accommodates negative metric values and displays a zero reference line."""
    import shutil
    import tempfile
    import matplotlib.pyplot as plt
    from build_section4_extra_figures import grouped_bar

    # Mock results dictionary with negative trigger attack effect
    mock_results = {
        "cora": {
            "Attacked FedAvg": {"trigger_attack_effect": "0.403"},
            "PD-FL": {"trigger_attack_effect": "0.463"},
            "GSP-FL": {"trigger_attack_effect": "0.497"},
            "FLPurifier-GNN": {"trigger_attack_effect": "-0.036"},
            "DMGNN-FL": {"trigger_attack_effect": "0.474"},
            "FedTGE": {"trigger_attack_effect": "0.739"},
            "ETD-FGL": {"trigger_attack_effect": "0.002"},
        },
        "pubmed": {
            "Attacked FedAvg": {"trigger_attack_effect": "0.112"},
            "PD-FL": {"trigger_attack_effect": "0.344"},
            "GSP-FL": {"trigger_attack_effect": "0.171"},
            "FLPurifier-GNN": {"trigger_attack_effect": "-0.027"},
            "DMGNN-FL": {"trigger_attack_effect": "0.084"},
            "FedTGE": {"trigger_attack_effect": "0.667"},
            "ETD-FGL": {"trigger_attack_effect": "-0.038"},
        },
        "reddit": {
            "Attacked FedAvg": {"trigger_attack_effect": "0.721"},
            "PD-FL": {"trigger_attack_effect": "0.730"},
            "GSP-FL": {"trigger_attack_effect": "0.730"},
            "FLPurifier-GNN": {"trigger_attack_effect": "-0.001"},
            "DMGNN-FL": {"trigger_attack_effect": "0.721"},
            "FedTGE": {"trigger_attack_effect": "0.045"},
            "ETD-FGL": {"trigger_attack_effect": "0.006"},
        },
    }

    temp_dir = Path(tempfile.mkdtemp(prefix="test_fig11_"))
    try:
        out_dir = temp_dir / "test_fig11"
        grouped_bar(
            mock_results,
            metric="trigger_attack_effect",
            ylabel="Final trigger attack effect",
            stem="Test_Fig_11",
            caption="Test caption for trigger attack effect.",
            output_dir=out_dir,
            include_clean=False,
        )

        # Check generated files
        assert (out_dir / "Test_Fig_11.png").is_file()
        assert (out_dir / "Test_Fig_11.pdf").is_file()
        caption_content = (out_dir / "Test_Fig_11_caption.txt").read_text(encoding="utf-8")
        assert "Test caption" in caption_content
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.unit
def test_captions_five_baselines_and_runtime_clarification():
    """Verify that section 4 figure captions declare five baselines and clarify runtime loop timing."""
    from build_section4_extra_figures import load_all_results
    project_dir = Path(__file__).resolve().parent
    script_content = (project_dir / "build_section4_extra_figures.py").read_text(encoding="utf-8")

    # Assert 'four baseline defenses' is completely eliminated
    assert "four baseline defenses" not in script_content
    assert "five baseline defenses" in script_content

    # Assert runtime clarification is documented
    assert "timed federated training loop" in script_content
    assert "offline" in script_content


@pytest.mark.unit
def test_extended_experiments_symbol_safety():
    """Verify run_extended_experiments.py has no undefined global variables or missing imports."""
    import builtins
    import symtable
    project_dir = Path(__file__).resolve().parent
    script_path = project_dir / "run_extended_experiments.py"
    code = script_path.read_text(encoding="utf-8")

    table = symtable.symtable(code, str(script_path), "exec")

    global_symbols = set(dir(builtins)) | {"__file__", "__name__"}
    for sym in table.get_symbols():
        if sym.is_assigned() or sym.is_imported():
            global_symbols.add(sym.get_name())

    undefined = []
    def check_table(t):
        for sym in t.get_symbols():
            if sym.is_global() and sym.is_referenced() and sym.get_name() not in global_symbols:
                undefined.append((t.get_name(), sym.get_name()))
        for child in t.get_children():
            check_table(child)

    check_table(table)
    assert not undefined, f"Found undefined global symbols in run_extended_experiments.py: {undefined}"


@pytest.mark.unit
def test_get_config_all_datasets():
    """Verify get_config resolves successfully for all target datasets."""
    from multidata_suite.config import DatasetConfig, get_config

    for dataset_key in ["cora", "pubmed", "reddit"]:
        cfg = get_config(dataset_key)
        assert isinstance(cfg, DatasetConfig)
        assert cfg.key == dataset_key
        assert cfg.rounds > 0
        assert cfg.hidden_channels == 32
        assert cfg.num_clients > 0


@pytest.mark.unit
def test_extended_experiments_cli_parsing():
    """Verify CLI parsing and method parsing across varied input formats."""
    from run_extended_experiments import build_parser, parse_methods, ALL_METHODS

    # Test parse_methods variations
    assert parse_methods("attacked,etdfgl") == ("attacked", "etdfgl")
    assert parse_methods(["attacked,etdfgl"]) == ("attacked", "etdfgl")
    assert parse_methods(["attacked", "etdfgl"]) == ("attacked", "etdfgl")
    assert parse_methods("all") == ALL_METHODS
    assert parse_methods(["all"]) == ALL_METHODS

    # Test user command: multiseed --datasets cora pubmed reddit --methods attacked,etdfgl --seeds 42 43 44
    parser = build_parser()
    args = parser.parse_args([
        "multiseed",
        "--datasets", "cora", "pubmed", "reddit",
        "--methods", "attacked,etdfgl",
        "--seeds", "42", "43", "44",
    ])
    assert args.study == "multiseed"
    assert args.datasets == ["cora", "pubmed", "reddit"]
    assert parse_methods(args.methods) == ("attacked", "etdfgl")
    assert args.seeds == [42, 43, 44]
    assert not args.force

    # Test single-dataset user command
    args_single = parser.parse_args([
        "multiseed",
        "--datasets", "cora",
        "--methods", "attacked,etdfgl",
        "--seeds", "42", "43", "44",
    ])
    assert args_single.datasets == ["cora"]
    assert parse_methods(args_single.methods) == ("attacked", "etdfgl")


@pytest.mark.unit
def test_multiseed_setup_without_training(monkeypatch):
    """Verify run_multiseed executes setup, metadata writing, and context creation without NameError."""
    import tempfile
    import shutil
    import run_extended_experiments
    from multidata_suite.config import get_config

    temp_dir = Path(tempfile.mkdtemp(prefix="test_multiseed_"))
    try:
        recorded_calls = []
        def fake_run_selected_methods(context, methods, force):
            recorded_calls.append({
                "dataset": context.config.key,
                "seed": context.config.seed,
                "methods": methods,
                "base_output": str(context.base_output),
            })
            return []

        monkeypatch.setattr(run_extended_experiments, "_run_selected_methods", fake_run_selected_methods)

        run_extended_experiments.run_multiseed(
            project_dir=temp_dir,
            datasets=["cora"],
            seeds=[42, 43],
            methods=("attacked", "etdfgl"),
            force=False,
        )

        assert len(recorded_calls) == 2
        assert recorded_calls[0]["seed"] == 42
        assert recorded_calls[1]["seed"] == 43
        assert recorded_calls[0]["methods"] == ("attacked", "etdfgl")

        # Check condition metadata file was written
        meta_path = temp_dir / "outputs" / "extended_experiments" / "multiseed" / "cora" / "seed_42" / "condition_metadata.json"
        assert meta_path.is_file()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Phase 7: Controlled Ablation Mathematical Equivalence and Invariants
# ==============================================================================

@pytest.mark.unit
def test_controlled_ablation_scaling_parameters():
    """Verify conversion of unnormalized coefficients to equivalent ConfigurableETDFGLAggregator parameters."""
    # 1. Fixed No Update: R = (9/13) * A_topo
    norm_topo, norm_upd, scaled_trust = get_equivalent_configurable_params(9.0 / 13.0, 0.0, trust_strength=3.0)
    assert math.isclose(norm_topo, 1.0, rel_tol=1e-14)
    assert norm_upd == 0.0
    assert math.isclose(scaled_trust, 3.0 * (9.0 / 13.0), rel_tol=1e-14)
    assert math.isclose(scaled_trust, 27.0 / 13.0, rel_tol=1e-14)

    # 2. Fixed No Topology: R = (4/13) * A_upd
    norm_topo, norm_upd, scaled_trust = get_equivalent_configurable_params(0.0, 4.0 / 13.0, trust_strength=3.0)
    assert norm_topo == 0.0
    assert math.isclose(norm_upd, 1.0, rel_tol=1e-14)
    assert math.isclose(scaled_trust, 3.0 * (4.0 / 13.0), rel_tol=1e-14)
    assert math.isclose(scaled_trust, 12.0 / 13.0, rel_tol=1e-14)

    # 3. Full ETD-FGL: R = (9/13) * A_topo + (4/13) * A_upd
    norm_topo, norm_upd, scaled_trust = get_equivalent_configurable_params(9.0 / 13.0, 4.0 / 13.0, trust_strength=3.0)
    assert math.isclose(norm_topo, 9.0 / 13.0, rel_tol=1e-14)
    assert math.isclose(norm_upd, 4.0 / 13.0, rel_tol=1e-14)
    assert math.isclose(scaled_trust, 3.0, rel_tol=1e-14)


@pytest.mark.unit
def test_controlled_ablation_analytical_formula_equivalence():
    """Verify analytical identity exp(-3.0 * (c * A)) == exp(-(3.0 * c) * A) over continuous domain."""
    # Dense test grid of anomaly values covering linear, exponential, and clipped saturation regimes
    a_values = np.linspace(0.0, 50.0, 1000, dtype=np.float64)

    # Fixed No Update: R = (9/13) * A_topo
    r_direct_topo = (9.0 / 13.0) * a_values
    t_direct_topo = np.clip(np.exp(-3.0 * r_direct_topo), 0.02, 1.0)
    t_scaled_topo = np.clip(np.exp(-(3.0 * (9.0 / 13.0)) * a_values), 0.02, 1.0)
    np.testing.assert_allclose(t_direct_topo, t_scaled_topo, rtol=1e-15, atol=1e-15)

    # Fixed No Topology: R = (4/13) * A_upd
    r_direct_upd = (4.0 / 13.0) * a_values
    t_direct_upd = np.clip(np.exp(-3.0 * r_direct_upd), 0.02, 1.0)
    t_scaled_upd = np.clip(np.exp(-(3.0 * (4.0 / 13.0)) * a_values), 0.02, 1.0)
    np.testing.assert_allclose(t_direct_upd, t_scaled_upd, rtol=1e-15, atol=1e-15)

    # Clipping bounds strictly respected everywhere
    assert np.all(t_direct_topo >= 0.02) and np.all(t_direct_topo <= 1.0)
    assert np.all(t_direct_upd >= 0.02) and np.all(t_direct_upd <= 1.0)


@pytest.mark.unit
def test_controlled_ablation_mathematical_equivalence_fixed_no_update():
    """Verify ControlledAblationETDFGLAggregator and trust_strength-scaled ConfigurableETDFGLAggregator match."""
    torch.manual_seed(101)
    np.random.seed(101)

    clean_graphs = [make_synthetic_graph(seed=i) for i in range(4)]
    current_graphs = [g.clone() for g in clean_graphs]
    # Add perturbing edges to client 0 to induce topology drift
    extra_edges = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)
    current_graphs[0].edge_index = torch.cat([current_graphs[0].edge_index, extra_edges], dim=1)

    # 1. Controlled implementation: R = (9/13) * A_topo, trust_strength = 3.0
    controlled_agg = ControlledAblationETDFGLAggregator(
        clean_graphs,
        current_graphs,
        topology_coeff=9.0 / 13.0,
        update_coeff=0.0,
        trust_strength=3.0,
    )

    # 2. Scaled Configurable implementation: topology_weight = 1.0, trust_strength = 3.0 * (9/13)
    configurable_agg = make_scaled_configurable_aggregator(
        "etdfgl_fixed_no_update",
        clean_graphs,
        current_graphs,
    )

    # Synthetic client updates
    global_state = {"w": torch.zeros((4, 4)), "b": torch.zeros(4)}
    local_states = [
        {"w": torch.randn((4, 4)), "b": torch.randn(4)}
        for _ in range(4)
    ]
    counts = [100, 120, 90, 110]

    out_controlled, diag_controlled = controlled_agg(local_states, counts, global_state, round_number=1)
    out_configurable, diag_configurable = configurable_agg(local_states, counts, global_state, round_number=1)

    # Client trust values must be bitwise equal within floating precision
    for i in range(4):
        t_ctrl = diag_controlled[f"etdfgl_trust_client_{i}"]
        t_conf = diag_configurable[f"etdfgl_trust_client_{i}"]
        assert math.isclose(t_ctrl, t_conf, rel_tol=1e-14, abs_tol=1e-14)

        w_ctrl = diag_controlled[f"etdfgl_weight_client_{i}"]
        w_conf = diag_configurable[f"etdfgl_weight_client_{i}"]
        assert math.isclose(w_ctrl, w_conf, rel_tol=1e-14, abs_tol=1e-14)

    # Aggregated state tensors must match to float precision
    for k in global_state.keys():
        assert torch.allclose(out_controlled[k], out_configurable[k], atol=1e-7)


@pytest.mark.unit
def test_controlled_ablation_mathematical_equivalence_fixed_no_topology():
    """Verify No-Topology controlled implementation matches trust_strength-scaled ConfigurableETDFGLAggregator."""
    torch.manual_seed(202)
    np.random.seed(202)

    clean_graphs = [make_synthetic_graph(seed=i) for i in range(4)]
    current_graphs = [g.clone() for g in clean_graphs]

    controlled_agg = ControlledAblationETDFGLAggregator(
        clean_graphs,
        current_graphs,
        topology_coeff=0.0,
        update_coeff=4.0 / 13.0,
        trust_strength=3.0,
    )

    configurable_agg = make_scaled_configurable_aggregator(
        "etdfgl_fixed_no_topology",
        clean_graphs,
        current_graphs,
    )

    global_state = {"w": torch.zeros((4, 4)), "b": torch.zeros(4)}
    # Client 0 is an update outlier
    local_states = [
        {"w": torch.full((4, 4), 10.0), "b": torch.full((4,), 10.0)},
        {"w": torch.randn((4, 4)) * 0.1, "b": torch.randn(4) * 0.1},
        {"w": torch.randn((4, 4)) * 0.1, "b": torch.randn(4) * 0.1},
        {"w": torch.randn((4, 4)) * 0.1, "b": torch.randn(4) * 0.1},
    ]
    counts = [100, 100, 100, 100]

    out_controlled, diag_controlled = controlled_agg(local_states, counts, global_state, round_number=1)
    out_configurable, diag_configurable = configurable_agg(local_states, counts, global_state, round_number=1)

    for i in range(4):
        t_ctrl = diag_controlled[f"etdfgl_trust_client_{i}"]
        t_conf = diag_configurable[f"etdfgl_trust_client_{i}"]
        assert math.isclose(t_ctrl, t_conf, rel_tol=1e-14, abs_tol=1e-14)

        w_ctrl = diag_controlled[f"etdfgl_weight_client_{i}"]
        w_conf = diag_configurable[f"etdfgl_weight_client_{i}"]
        assert math.isclose(w_ctrl, w_conf, rel_tol=1e-14, abs_tol=1e-14)

    for k in global_state.keys():
        assert torch.allclose(out_controlled[k], out_configurable[k], atol=1e-7)


@pytest.mark.unit
def test_controlled_ablation_full_production_match():
    """Verify ControlledAblationETDFGLAggregator with (9/13, 4/13) matches ETDFGLAggregator."""
    clean_graphs = [make_synthetic_graph(seed=i) for i in range(3)]
    current_graphs = [g.clone() for g in clean_graphs]

    controlled_agg = ControlledAblationETDFGLAggregator(
        clean_graphs,
        current_graphs,
        topology_coeff=9.0 / 13.0,
        update_coeff=4.0 / 13.0,
        trust_strength=3.0,
    )
    production_agg = ETDFGLAggregator(clean_graphs, current_graphs)

    global_state = {"w": torch.zeros((3, 3))}
    local_states = [
        {"w": torch.tensor([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])},
        {"w": torch.tensor([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])},
        {"w": torch.tensor([[5.0, 5.0, 5.0], [5.0, 5.0, 5.0], [5.0, 5.0, 5.0]])},
    ]
    counts = [100, 100, 100]

    out_ctrl, diag_ctrl = controlled_agg(local_states, counts, global_state, 1)
    out_prod, diag_prod = production_agg(local_states, counts, global_state, 1)

    for i in range(3):
        # Fused risk must match exactly
        assert math.isclose(
            diag_ctrl[f"etdfgl_fused_risk_client_{i}"],
            diag_prod[f"etdfgl_fused_risk_client_{i}"],
            rel_tol=1e-14,
        )
        assert math.isclose(
            diag_ctrl[f"etdfgl_trust_client_{i}"],
            diag_prod[f"etdfgl_trust_client_{i}"],
            rel_tol=1e-14,
        )
        assert math.isclose(
            diag_ctrl[f"etdfgl_weight_client_{i}"],
            diag_prod[f"etdfgl_weight_client_{i}"],
            rel_tol=1e-14,
        )

    for k in global_state.keys():
        assert torch.allclose(out_ctrl[k], out_prod[k], atol=1e-7)


@pytest.mark.unit
def test_controlled_ablation_diagnostics_fused_risk_unnormalized():
    """Verify that ControlledAblationETDFGLAggregator logs unnormalized R = c_topo * A_topo or c_upd * A_upd."""
    clean_graphs = [make_synthetic_graph(seed=i) for i in range(3)]
    current_graphs = [g.clone() for g in clean_graphs]

    # Variant 1: Fixed No Update
    agg_no_upd = ControlledAblationETDFGLAggregator(
        clean_graphs,
        current_graphs,
        topology_coeff=9.0 / 13.0,
        update_coeff=0.0,
        trust_strength=3.0,
    )
    global_s = {"w": torch.zeros(4)}
    local_s = [{"w": torch.randn(4)} for _ in range(3)]
    _, diags_no_upd = agg_no_upd(local_s, [100, 100, 100], global_s, 1)

    for i in range(3):
        topo_r = diags_no_upd[f"etdfgl_topology_risk_client_{i}"]
        fused_r = diags_no_upd[f"etdfgl_fused_risk_client_{i}"]
        assert math.isclose(fused_r, (9.0 / 13.0) * topo_r, rel_tol=1e-14)

    # Variant 2: Fixed No Topology
    agg_no_topo = ControlledAblationETDFGLAggregator(
        clean_graphs,
        current_graphs,
        topology_coeff=0.0,
        update_coeff=4.0 / 13.0,
        trust_strength=3.0,
    )
    _, diags_no_topo = agg_no_topo(local_s, [100, 100, 100], global_s, 1)

    for i in range(3):
        upd_r = diags_no_topo[f"etdfgl_update_risk_client_{i}"]
        fused_r = diags_no_topo[f"etdfgl_fused_risk_client_{i}"]
        assert math.isclose(fused_r, (4.0 / 13.0) * upd_r, rel_tol=1e-14)


@pytest.mark.unit
def test_controlled_ablation_runner_dry_run_unit():
    """Verify run_controlled_ablation dry-run validates configurations and writes metadata without training."""
    from run_controlled_ablation import run_controlled_ablation

    results = run_controlled_ablation(
        project_dir=Path(__file__).resolve().parent,
        datasets=["cora"],
        seeds=[42],
        variants=["fixed_no_update", "fixed_no_topology", "full"],
        dry_run=True,
    )
    # Dry run should succeed and return dictionary of datasets
    assert "cora" in results
    assert len(results["cora"]) == 0  # No training executed in dry-run mode


@pytest.mark.unit
def test_build_controlled_ablation_tables_unit():
    """Verify build_controlled_ablation_tables compiles Markdown, LaTeX, and JSON without error."""
    import build_controlled_ablation_tables

    project_dir = Path(__file__).resolve().parent
    data = build_controlled_ablation_tables.collect_ablation_data(project_dir)
    assert "cora" in data

    md_report = build_controlled_ablation_tables.build_markdown_report(data)
    assert "# ETD-FGL Controlled Scientific Ablation: Paired Comparison Report" in md_report
    assert "CORA" in md_report

    tex_table = build_controlled_ablation_tables.build_latex_tables(data)
    assert "\\begin{table*}" in tex_table
    assert "Fixed No Update" in tex_table


@pytest.mark.unit
def test_controlled_ablation_manifest_integrity():
    """Verify that every experiment in controlled_ablation_v1 matches its manifest hashes with zero errors."""
    import hashlib
    project_dir = Path(__file__).resolve().parent
    root = project_dir / "outputs" / "extended_experiments" / "controlled_ablation_v1"

    if not root.is_dir():
        pytest.skip("controlled_ablation_v1 directory not present")

    datasets = ["cora", "pubmed", "reddit"]
    seeds = [42, 43, 44]
    methods = [
        "fedavg_structural_backdoor",
        "etdfgl_full",
        "etdfgl_fixed_no_update",
        "etdfgl_fixed_no_topology",
    ]

    total_verified = 0
    for ds in datasets:
        for seed in seeds:
            seed_dir = root / ds / f"seed_{seed}"
            assert (seed_dir / "condition_metadata.json").is_file(), f"Missing condition_metadata.json in {seed_dir}"

            for method in methods:
                exp_dir = seed_dir / method
                assert exp_dir.is_dir(), f"Missing experiment dir {exp_dir}"

                manifest_file = exp_dir / "experiment_manifest.json"
                assert manifest_file.is_file(), f"Missing manifest in {exp_dir}"
                manifest = json.loads(manifest_file.read_text(encoding="utf-8"))

                for file_key, fname in [
                    ("summary_sha256", "final_summary.json"),
                    ("checkpoint_sha256", "best_model.pt"),
                    ("history_sha256", "training_history.csv"),
                ]:
                    target_file = exp_dir / fname
                    assert target_file.is_file(), f"Missing {fname} in {exp_dir}"
                    actual_sha = hashlib.sha256(target_file.read_bytes()).hexdigest()
                    expected_sha = manifest.get(file_key)
                    assert actual_sha == expected_sha, (
                        f"Manifest SHA256 mismatch in {target_file}: {actual_sha} vs {expected_sha}"
                    )
                total_verified += 1

    assert total_verified == 36, f"Expected 36 verified experiments, got {total_verified}"


@pytest.mark.unit
def test_controlled_ablation_report_not_stale():
    """Verify that generated report files are up to date and contain no pending execution placeholders."""
    project_dir = Path(__file__).resolve().parent
    out_dir = project_dir / "outputs" / "extended_experiments" / "controlled_ablation_v1"

    md_file = out_dir / "controlled_ablation_results.md"
    tex_file = out_dir / "controlled_ablation_tables.tex"
    json_file = out_dir / "controlled_ablation_summary.json"

    assert md_file.is_file(), "controlled_ablation_results.md missing"
    assert tex_file.is_file(), "controlled_ablation_tables.tex missing"
    assert json_file.is_file(), "controlled_ablation_summary.json missing"

    md_content = md_file.read_text(encoding="utf-8")
    assert "Pending Execution" not in md_content, "controlled_ablation_results.md contains stale 'Pending Execution' text"
    assert "Pending" not in md_content, "controlled_ablation_results.md contains pending placeholders"

    # Verify all variants and datasets exist in JSON summary
    summary_data = json.loads(json_file.read_text(encoding="utf-8"))
    for ds in ["cora", "pubmed", "reddit"]:
        assert ds in summary_data, f"Missing {ds} in summary JSON"
        for var in ["etdfgl_full", "etdfgl_fixed_no_update", "etdfgl_fixed_no_topology"]:
            assert var in summary_data[ds], f"Missing {var} under {ds} in summary JSON"
            assert set(summary_data[ds][var].keys()) == {"42", "43", "44"}, (
                f"Variant {var} under {ds} does not have seeds 42, 43, 44"
            )
