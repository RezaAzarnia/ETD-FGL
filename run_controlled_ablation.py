#!/usr/bin/env python3
"""Controlled Scientific Ablation Experiment Runner for ETD-FGL.

This script executes a controlled scientific ablation isolating the evidence channels
without confounding the channel selection with coefficient changes:

Variants:
1. Fixed-coefficient No Update:
   R_i = (9/13) * A_topology,i
   T_i = clip(exp(-3.0 * R_i), 0.02, 1.0)
   Holds the topology coefficient fixed at 9/13 while removing the update channel.

2. Fixed-coefficient No Topology:
   R_i = (4/13) * A_update,i
   T_i = clip(exp(-3.0 * R_i), 0.02, 1.0)
   Holds the update coefficient fixed at 4/13 while removing the topology channel.

3. Full ETD-FGL:
   R_i = (9/13) * A_topology,i + (4/13) * A_update,i
   T_i = clip(exp(-3.0 * R_i), 0.02, 1.0)

All variants preserve:
- Trust mapping: T = clip(exp(-3R), 0.02, 1.0)
- Clipping bounds: [0.02, 1.0]
- Model architecture: 2-layer GCN (hidden=32, dropout=0.5)
- Attack configuration: clique trigger (size=3, poison_rate=0.2, target_class=0)
- Datasets: Cora, PubMed, Reddit
- Random seeds: 42, 43, 44

Outputs are stored strictly under:
    outputs/extended_experiments/controlled_ablation_v1/
Existing results are never overwritten unless --force is explicitly provided.
"""

from __future__ import annotations

import argparse
import json
import shutil
import time
from dataclasses import asdict, replace
from pathlib import Path
from typing import Sequence

import numpy as np
import torch

from multidata_suite.config import DatasetConfig, get_config
from multidata_suite.controlled_ablation import (
    CONTROLLED_VARIANTS,
    ControlledAblationETDFGLAggregator,
    ControlledAblationVariant,
    make_scaled_configurable_aggregator,
)
from multidata_suite.core import (
    ExperimentContext,
    _atomic_save_json,
    build_context,
    fedavg,
    run_method,
    validate_existing_experiment,
)
from multidata_suite.defenses import ETDFGLAggregator
from multidata_suite.model import GCN

DATASETS = ("cora", "pubmed", "reddit")
SEEDS = (42, 43, 44)
DEFAULT_VARIANTS = ("fixed_no_update", "fixed_no_topology", "full")


def _load_checkpoint_model(context: ExperimentContext, slug: str) -> GCN:
    path = context.base_output / slug / "best_model.pt"
    if not path.exists():
        raise FileNotFoundError(f"Required checkpoint was not found: {path}")
    checkpoint = torch.load(path, map_location=context.device, weights_only=False)
    model = GCN(
        context.num_features,
        context.config.hidden_channels,
        context.num_classes,
        context.config.dropout,
    ).to(context.device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model


def _write_condition_metadata(
    base_output: Path,
    config: DatasetConfig,
    seed: int,
    variants: Sequence[str],
) -> None:
    base_output.mkdir(parents=True, exist_ok=True)
    meta = {
        "study": "controlled_ablation_v1",
        "dataset": config.key,
        "seed": seed,
        "timestamp": time.time(),
        "config": asdict(config),
        "invariants": {
            "trust_mapping": "exp(-3.0 * R)",
            "clipping_bounds": [0.02, 1.0],
            "model_architecture": f"GCN (hidden={config.hidden_channels}, dropout={config.dropout})",
            "attack_type": "structural_clique_backdoor",
            "trigger_size": config.trigger_size,
            "poison_rate": config.poison_rate,
            "target_class": config.target_class,
        },
        "variants": {
            v_key: asdict(CONTROLLED_VARIANTS[f"etdfgl_{v_key}" if not v_key.startswith("etdfgl_") else v_key])
            for v_key in variants
            if (f"etdfgl_{v_key}" if not v_key.startswith("etdfgl_") else v_key) in CONTROLLED_VARIANTS
        },
    }
    _atomic_save_json(meta, base_output / "condition_metadata.json")


def _execute(
    context: ExperimentContext,
    *,
    slug: str,
    method_name: str,
    force: bool,
    **kwargs,
) -> dict:
    if not force:
        cached_summary = validate_existing_experiment(context, slug, expected_method_name=method_name)
        if cached_summary is not None:
            print(f"  SKIP {slug}: validated compatible existing experiment found")
            return cached_summary
        output_dir = context.base_output / slug
        has_existing = (
            (output_dir / "final_summary.json").is_file()
            or (output_dir / "best_model.pt").is_file()
            or (output_dir / "training_history.csv").is_file()
        )
        if has_existing:
            raise RuntimeError(
                f"Existing experiment in {output_dir} is incompatible or failed validation. "
                "Automatic overwrite without authorization is prohibited. "
                "Pass force=True (or --force on CLI) to explicitly authorize an overwrite."
            )
    return run_method(
        context=context,
        output_slug=slug,
        method_name=method_name,
        force=force,
        **kwargs,
    )


def _try_reuse_existing_backdoor(
    project_dir: Path,
    target_base: Path,
    dataset: str,
    seed: int,
) -> bool:
    """Attempts to copy an existing validated attacked FedAvg run to avoid redundant retraining."""
    target_dir = target_base / "fedavg_structural_backdoor"
    if (target_dir / "final_summary.json").is_file() and (target_dir / "best_model.pt").is_file():
        return True

    candidate_sources = [
        project_dir / "outputs" / "extended_experiments" / "ablation" / dataset / f"seed_{seed}" / "fedavg_structural_backdoor",
        project_dir / "outputs" / "extended_experiments" / "multiseed" / dataset / f"seed_{seed}" / "fedavg_structural_backdoor",
    ]
    if seed == 42:
        candidate_sources.append(
            project_dir / "outputs" / "final_multidataset" / f"federated_{dataset}" / "fedavg_structural_backdoor"
        )

    for src in candidate_sources:
        if (src / "final_summary.json").is_file() and (src / "best_model.pt").is_file():
            target_dir.mkdir(parents=True, exist_ok=True)
            for fname in ("final_summary.json", "best_model.pt", "training_history.csv", "experiment_manifest.json"):
                s_file = src / fname
                if s_file.is_file():
                    shutil.copy2(s_file, target_dir / fname)
            print(f"  Reused validated attacked checkpoint from {src.relative_to(project_dir)}")
            return True
    return False


def _try_reuse_existing_full(
    project_dir: Path,
    target_base: Path,
    dataset: str,
    seed: int,
) -> bool:
    """Attempts to copy an existing validated Full ETD-FGL run for exact paired baseline comparison."""
    target_dir = target_base / "etdfgl_full"
    if (target_dir / "final_summary.json").is_file() and (target_dir / "best_model.pt").is_file():
        return True

    candidate_sources = [
        project_dir / "outputs" / "extended_experiments" / "ablation" / dataset / f"seed_{seed}" / "etdfgl_full",
        project_dir / "outputs" / "extended_experiments" / "multiseed" / dataset / f"seed_{seed}" / "defended_etdfgl",
    ]
    if seed == 42:
        candidate_sources.append(
            project_dir / "outputs" / "final_multidataset" / f"federated_{dataset}" / "defended_etdfgl"
        )

    for src in candidate_sources:
        if (src / "final_summary.json").is_file() and (src / "best_model.pt").is_file():
            target_dir.mkdir(parents=True, exist_ok=True)
            for fname in ("final_summary.json", "best_model.pt", "training_history.csv", "experiment_manifest.json"):
                s_file = src / fname
                if s_file.is_file():
                    shutil.copy2(s_file, target_dir / fname)
            print(f"  Reused validated Full ETD-FGL baseline from {src.relative_to(project_dir)}")
            return True
    return False


def run_controlled_ablation(
    project_dir: Path,
    datasets: Sequence[str] = DATASETS,
    seeds: Sequence[int] = SEEDS,
    variants: Sequence[str] = DEFAULT_VARIANTS,
    force: bool = False,
    dry_run: bool = False,
    use_scaled_configurable: bool = False,
) -> dict[str, list[dict]]:
    """Executes or dry-runs the controlled ablation suite."""
    results: dict[str, list[dict]] = {}

    for dataset in datasets:
        results[dataset] = []
        for seed in seeds:
            print(f"\n========================================================")
            print(f"Controlled Ablation: Dataset={dataset.upper()} | Seed={seed}")
            print(f"========================================================")

            config = replace(get_config(dataset), seed=int(seed))
            base_output = (
                project_dir
                / "outputs"
                / "extended_experiments"
                / "controlled_ablation_v1"
                / dataset
                / f"seed_{seed}"
            )
            base_output.mkdir(parents=True, exist_ok=True)
            _write_condition_metadata(base_output, config, seed, variants)

            # Build experiment context under target base_output
            context = build_context(project_dir, config, base_output=base_output)

            if dry_run:
                print(f"  [DRY-RUN] Context built successfully.")
                print(f"  [DRY-RUN] Partition: {context.partition_metadata.get('strategy', 'unknown')}")
                print(f"  [DRY-RUN] Clients: {len(context.attacked_graphs_cpu)}")
                print(f"  [DRY-RUN] Output directory: {base_output.relative_to(project_dir)}")

                # Test aggregator construction and bounds for each requested variant
                for v_key in variants:
                    full_key = f"etdfgl_{v_key}" if not v_key.startswith("etdfgl_") else v_key
                    var_spec = CONTROLLED_VARIANTS[full_key]
                    print(f"  [DRY-RUN] Validating variant: {var_spec.display_name}")
                    print(f"            Formula: {var_spec.formula_str}")

                    agg = ControlledAblationETDFGLAggregator(
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                        topology_coeff=var_spec.topology_coeff,
                        update_coeff=var_spec.update_coeff,
                        trust_strength=var_spec.trust_strength,
                    )
                    assert len(agg.topology_risk) == len(context.attacked_graphs_cpu)
                    assert np.all(agg.topology_risk >= 0.0)

                    # Also validate the equivalent scaled ConfigurableETDFGLAggregator
                    agg_scaled = make_scaled_configurable_aggregator(
                        full_key,
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                    )
                    assert agg_scaled.use_trust_weighting is True
                print(f"  [DRY-RUN] Completed validation for {dataset} seed {seed}.")
                continue

            # Ensure shared attacked FedAvg model checkpoint is available
            reused = _try_reuse_existing_backdoor(project_dir, base_output, dataset, seed)
            if not reused:
                _execute(
                    context,
                    slug="fedavg_structural_backdoor",
                    method_name="Attacked FedAvg",
                    force=force,
                    client_graphs_cpu=context.attacked_graphs_cpu,
                    aggregate_fn=fedavg,
                )
            attacked_model = _load_checkpoint_model(context, "fedavg_structural_backdoor")

            # 1. Full ETD-FGL baseline (for paired comparison)
            if "full" in variants or "etdfgl_full" in variants:
                full_reused = _try_reuse_existing_full(project_dir, base_output, dataset, seed)
                if not full_reused:
                    full_var = CONTROLLED_VARIANTS["etdfgl_full"]
                    full_agg = ControlledAblationETDFGLAggregator(
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                        topology_coeff=full_var.topology_coeff,
                        update_coeff=full_var.update_coeff,
                        trust_strength=full_var.trust_strength,
                    )
                    res = _execute(
                        context,
                        slug="etdfgl_full",
                        method_name=full_var.display_name,
                        force=force,
                        client_graphs_cpu=context.attacked_graphs_cpu,
                        aggregate_fn=full_agg,
                        method_metadata={
                            "controlled_ablation": True,
                            "variant": "etdfgl_full",
                            "topology_coeff": full_var.topology_coeff,
                            "update_coeff": full_var.update_coeff,
                            "formula": "R = (9/13) * A_topo + (4/13) * A_upd",
                        },
                    )
                    results[dataset].append(res)

            # 2. Fixed-coefficient No Update
            if "fixed_no_update" in variants or "etdfgl_fixed_no_update" in variants:
                v_spec = CONTROLLED_VARIANTS["etdfgl_fixed_no_update"]
                if use_scaled_configurable:
                    aggregator = make_scaled_configurable_aggregator(
                        "etdfgl_fixed_no_update",
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                    )
                else:
                    aggregator = ControlledAblationETDFGLAggregator(
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                        topology_coeff=v_spec.topology_coeff,
                        update_coeff=v_spec.update_coeff,
                        trust_strength=v_spec.trust_strength,
                    )

                res = _execute(
                    context,
                    slug="etdfgl_fixed_no_update",
                    method_name=v_spec.display_name,
                    force=force,
                    client_graphs_cpu=context.attacked_graphs_cpu,
                    aggregate_fn=aggregator,
                    method_metadata={
                        "controlled_ablation": True,
                        "variant": "etdfgl_fixed_no_update",
                        "topology_coeff": v_spec.topology_coeff,
                        "update_coeff": v_spec.update_coeff,
                        "formula": "R = (9/13) * A_topo",
                        "description": v_spec.description,
                        "implementation": "scaled_configurable" if use_scaled_configurable else "controlled_unnormalized",
                    },
                )
                results[dataset].append(res)

            # 3. Fixed-coefficient No Topology
            if "fixed_no_topology" in variants or "etdfgl_fixed_no_topology" in variants:
                v_spec = CONTROLLED_VARIANTS["etdfgl_fixed_no_topology"]
                if use_scaled_configurable:
                    aggregator = make_scaled_configurable_aggregator(
                        "etdfgl_fixed_no_topology",
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                    )
                else:
                    aggregator = ControlledAblationETDFGLAggregator(
                        context.clean_graphs_cpu,
                        context.attacked_graphs_cpu,
                        topology_coeff=v_spec.topology_coeff,
                        update_coeff=v_spec.update_coeff,
                        trust_strength=v_spec.trust_strength,
                    )

                res = _execute(
                    context,
                    slug="etdfgl_fixed_no_topology",
                    method_name=v_spec.display_name,
                    force=force,
                    client_graphs_cpu=context.attacked_graphs_cpu,
                    aggregate_fn=aggregator,
                    method_metadata={
                        "controlled_ablation": True,
                        "variant": "etdfgl_fixed_no_topology",
                        "topology_coeff": v_spec.topology_coeff,
                        "update_coeff": v_spec.update_coeff,
                        "formula": "R = (4/13) * A_upd",
                        "description": v_spec.description,
                        "implementation": "scaled_configurable" if use_scaled_configurable else "controlled_unnormalized",
                    },
                )
                results[dataset].append(res)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run controlled scientific ablation of ETD-FGL without altering production code."
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=list(DATASETS),
        choices=list(DATASETS),
        help="Datasets to evaluate (default: cora pubmed reddit).",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=list(SEEDS),
        help="Random seeds to evaluate (default: 42 43 44).",
    )
    parser.add_argument(
        "--variants",
        nargs="+",
        default=list(DEFAULT_VARIANTS),
        choices=["fixed_no_update", "fixed_no_topology", "full"],
        help="Ablation variants to run (default: fixed_no_update fixed_no_topology full).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Authorize overwrite of existing completed runs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform offline configuration validation and test aggregator setup without training models.",
    )
    parser.add_argument(
        "--scaled-configurable",
        action="store_true",
        help="Use ConfigurableETDFGLAggregator with trust_strength scaling instead of ControlledAblationETDFGLAggregator.",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Root path of the repository.",
    )
    args = parser.parse_args()

    run_controlled_ablation(
        project_dir=args.project_dir,
        datasets=args.datasets,
        seeds=args.seeds,
        variants=args.variants,
        force=args.force,
        dry_run=args.dry_run,
        use_scaled_configurable=args.scaled_configurable,
    )


if __name__ == "__main__":
    main()
