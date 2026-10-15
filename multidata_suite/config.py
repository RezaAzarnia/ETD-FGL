from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetConfig:
    key: str
    display_name: str
    num_clients: int = 5
    rounds: int = 50
    local_epochs: int = 3
    hidden_channels: int = 32
    learning_rate: float = 0.01
    weight_decay: float = 5e-4
    dropout: float = 0.5
    seed: int = 42
    malicious_client_id: int = 0
    target_class: int = 0
    poison_rate: float = 0.20
    trigger_size: int = 3
    reddit_sample_size: int = 8000
    reddit_sample_seed: int = 42
    explainer_epochs: int = 15
    explanation_probes: int = 2


DATASET_CONFIGS = {
    "cora": DatasetConfig(
        key="cora",
        display_name="Cora",
        rounds=50,
        local_epochs=3,
        hidden_channels=32,
    ),
    "pubmed": DatasetConfig(
        key="pubmed",
        display_name="PubMed",
        rounds=50,
        local_epochs=3,
        hidden_channels=32,
    ),
    "reddit": DatasetConfig(
        key="reddit",
        display_name="Reddit",
        rounds=50,
        local_epochs=3,
        hidden_channels=32,
        learning_rate=0.005,
        reddit_sample_size=8000,
        explainer_epochs=10,
        explanation_probes=2,
    ),
}


def get_config(dataset: str) -> DatasetConfig:
    key = dataset.strip().lower()
    if key not in DATASET_CONFIGS:
        raise ValueError(
            f"Unsupported dataset {dataset!r}. "
            f"Choose one of: {', '.join(DATASET_CONFIGS)}"
        )
    return DATASET_CONFIGS[key]


# Central Canonical Method Registry: (Display Name, Output Slug)
BENCHMARK_METHODS: list[tuple[str, str]] = [
    ("Clean FedAvg", "fedavg_clean"),
    ("Attacked FedAvg", "fedavg_structural_backdoor"),
    ("PD-FL", "baseline_pdfl"),
    ("GSP-FL", "baseline_gsp"),
    ("FLPurifier-GNN", "baseline_flpurifier"),
    ("DMGNN-FL", "baseline_dmgnn"),
    ("FedTGE", "baseline_fedtge"),
    ("ETD-FGL", "defended_etdfgl"),
]

# Canonical Method-to-Color Mapping for Consistent Scientific Visualizations across Subplots
METHOD_COLORS: dict[str, str] = {
    "Clean FedAvg": "#1f77b4",          # tab:blue
    "Attacked FedAvg": "#ff7f0e",       # tab:orange
    "PD-FL": "#2ca02c",                 # tab:green
    "GSP-FL": "#d62728",                # tab:red
    "FLPurifier-GNN": "#9467bd",        # tab:purple
    "DMGNN-FL": "#8c564b",              # tab:brown
    "FedTGE": "#e377c2",                # tab:pink
    "ETD-FGL": "#7f7f7f",               # tab:gray
}
