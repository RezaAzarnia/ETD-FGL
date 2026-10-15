from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from torch_geometric.data import Data

from multidata_suite.config import DatasetConfig
from multidata_suite.defenses import (
    ConfigurableETDFGLAggregator,
    _flatten_delta,
    _graph_descriptor,
    _robust_positive,
    _weighted_average,
)
from multidata_suite.model import GCN, StateDict


@dataclass(frozen=True)
class ControlledAblationVariant:
    """Specification of an ETD-FGL controlled ablation variant."""

    slug: str
    display_name: str
    topology_coeff: float
    update_coeff: float
    trust_strength: float = 3.0
    use_trust_weighting: bool = True
    description: str = ""

    @property
    def formula_str(self) -> str:
        parts = []
        if self.topology_coeff > 0:
            parts.append(f"({self.topology_coeff:.4f}) * A_topo")
        if self.update_coeff > 0:
            parts.append(f"({self.update_coeff:.4f}) * A_upd")
        formula = " + ".join(parts) if parts else "0.0"
        return f"R = {formula}, T = clip(exp(-{self.trust_strength:.1f} * R), 0.02, 1.0)"


CONTROLLED_VARIANTS: dict[str, ControlledAblationVariant] = {
    "etdfgl_fixed_no_update": ControlledAblationVariant(
        slug="etdfgl_fixed_no_update",
        display_name="ETD-FGL Fixed No Update (9/13 Topo)",
        topology_coeff=9.0 / 13.0,
        update_coeff=0.0,
        trust_strength=3.0,
        use_trust_weighting=True,
        description="Fixed-coefficient ablation with R = (9/13) * A_topology, holding the topology coefficient fixed while removing the update channel.",
    ),
    "etdfgl_fixed_no_topology": ControlledAblationVariant(
        slug="etdfgl_fixed_no_topology",
        display_name="ETD-FGL Fixed No Topology (4/13 Update)",
        topology_coeff=0.0,
        update_coeff=4.0 / 13.0,
        trust_strength=3.0,
        use_trust_weighting=True,
        description="Fixed-coefficient ablation with R = (4/13) * A_update, holding the update coefficient fixed while removing the topology channel.",
    ),
    "etdfgl_full": ControlledAblationVariant(
        slug="etdfgl_full",
        display_name="ETD-FGL (Full final)",
        topology_coeff=9.0 / 13.0,
        update_coeff=4.0 / 13.0,
        trust_strength=3.0,
        use_trust_weighting=True,
        description="Full production ETD-FGL with R = (9/13) * A_topology + (4/13) * A_update.",
    ),
}


def get_equivalent_configurable_params(
    topology_coeff: float,
    update_coeff: float,
    trust_strength: float = 3.0,
) -> tuple[float, float, float]:
    """Calculate equivalent parameters for ConfigurableETDFGLAggregator.

    Because ConfigurableETDFGLAggregator normalizes component weights to sum to 1.0,
    scaling trust_strength by (topology_coeff + update_coeff) produces the exact same
    trust values and client aggregation weights:

        exp(-trust_strength * (c_topo * A_topo + c_upd * A_upd))
        = exp(-(trust_strength * S) * ((c_topo / S) * A_topo + (c_upd / S) * A_upd))
        where S = c_topo + c_upd.

    Returns:
        tuple (topology_weight, update_weight, scaled_trust_strength)
    """
    total = float(topology_coeff + update_coeff)
    if total <= 0:
        raise ValueError("Sum of coefficients must be positive.")
    norm_topo = float(topology_coeff) / total
    norm_upd = float(update_coeff) / total
    scaled_trust = float(trust_strength) * total
    return norm_topo, norm_upd, scaled_trust


class ControlledAblationETDFGLAggregator:
    """ETD-FGL aggregator with explicit fixed unnormalized evidence coefficients.

    Unlike ConfigurableETDFGLAggregator which normalizes weights to sum to 1.0,
    this aggregator preserves the exact specified coefficient for each channel:

        R_i = topology_coeff * A_topology,i + update_coeff * A_update,i
        T_i = clip(exp(-trust_strength * R_i), 0.02, 1.0)
        w_i = T_i * count_i / sum_j(T_j * count_j)

    This guarantees that the logged benign-client risk (`etdfgl_fused_risk_client_i`)
    reflects the actual unnormalized risk R rather than being artificially inflated
    by weight normalization.
    """

    def __init__(
        self,
        clean_graphs: list[Data],
        current_graphs: list[Data],
        attacked_model: GCN | None = None,
        config: DatasetConfig | None = None,
        *,
        topology_coeff: float = 9.0 / 13.0,
        update_coeff: float = 4.0 / 13.0,
        trust_strength: float = 3.0,
        use_trust_weighting: bool = True,
        compute_explanation_diagnostic: bool = False,
    ) -> None:
        del attacked_model, config, compute_explanation_diagnostic
        if topology_coeff < 0 or update_coeff < 0:
            raise ValueError("ETD-FGL evidence coefficients must be non-negative.")
        if topology_coeff + update_coeff <= 0 and use_trust_weighting:
            raise ValueError("At least one ETD-FGL evidence coefficient must be positive.")

        self.topology_coeff = float(topology_coeff)
        self.update_coeff = float(update_coeff)
        self.trust_strength = float(trust_strength)
        self.use_trust_weighting = bool(use_trust_weighting)

        clean = np.stack([_graph_descriptor(graph) for graph in clean_graphs])
        current = np.stack([_graph_descriptor(graph) for graph in current_graphs])
        scale = np.std(clean, axis=0)
        scale[scale < 1e-8] = 1.0
        drift = np.linalg.norm((current - clean) / scale, axis=1)
        self.topology_risk = _robust_positive(drift)
        self.explanation_risk = np.zeros(len(current_graphs), dtype=np.float64)

    def __call__(
        self,
        local_states: list[StateDict],
        counts: list[int],
        global_state: StateDict,
        round_number: int,
    ) -> tuple[StateDict, dict[str, float]]:
        del round_number
        updates = torch.stack([
            _flatten_delta(state, global_state)
            for state in local_states
        ])
        median = updates.median(dim=0).values
        distances = np.asarray([
            float((update - median).norm().item())
            for update in updates
        ])
        update_risk = _robust_positive(distances)

        # Explicit unnormalized risk fusion:
        risk = (
            self.topology_coeff * self.topology_risk
            + self.update_coeff * update_risk
        )

        if self.use_trust_weighting:
            trust = np.clip(
                np.exp(-self.trust_strength * risk),
                0.02,
                1.0,
            )
        else:
            trust = np.ones(len(counts), dtype=np.float64)

        weights = trust * np.asarray(counts, dtype=np.float64)
        weights /= weights.sum()

        diagnostics: dict[str, float] = {
            "etdfgl_topology_coeff": float(self.topology_coeff),
            "etdfgl_update_coeff": float(self.update_coeff),
            "etdfgl_trust_strength": float(self.trust_strength),
            "etdfgl_use_trust_weighting": float(self.use_trust_weighting),
            "etdfgl_controlled_ablation": 1.0,
        }
        for client_id in range(len(local_states)):
            diagnostics[f"etdfgl_topology_risk_client_{client_id}"] = float(self.topology_risk[client_id])
            diagnostics[f"etdfgl_explanation_risk_client_{client_id}"] = float(self.explanation_risk[client_id])
            diagnostics[f"etdfgl_update_risk_client_{client_id}"] = float(update_risk[client_id])
            diagnostics[f"etdfgl_fused_risk_client_{client_id}"] = float(risk[client_id])
            diagnostics[f"etdfgl_trust_client_{client_id}"] = float(trust[client_id])
            diagnostics[f"etdfgl_weight_client_{client_id}"] = float(weights[client_id])

        return _weighted_average(local_states, weights), diagnostics


def make_scaled_configurable_aggregator(
    variant_key: str,
    clean_graphs: list[Data],
    current_graphs: list[Data],
    attacked_model: GCN | None = None,
    config: DatasetConfig | None = None,
) -> ConfigurableETDFGLAggregator:
    """Alternative implementation using ConfigurableETDFGLAggregator with trust_strength scaling.

    Demonstrates mathematical equivalence to ControlledAblationETDFGLAggregator.
    """
    if variant_key not in CONTROLLED_VARIANTS:
        raise ValueError(f"Unknown controlled variant: {variant_key}")
    variant = CONTROLLED_VARIANTS[variant_key]
    norm_topo, norm_upd, scaled_trust = get_equivalent_configurable_params(
        variant.topology_coeff,
        variant.update_coeff,
        variant.trust_strength,
    )
    return ConfigurableETDFGLAggregator(
        clean_graphs,
        current_graphs,
        attacked_model,
        config,
        topology_weight=norm_topo,
        explanation_weight=0.0,
        update_weight=norm_upd,
        trust_strength=scaled_trust,
        use_trust_weighting=variant.use_trust_weighting,
    )
