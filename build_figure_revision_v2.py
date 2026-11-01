#!/usr/bin/env python3
"""ETD-FGL Scientific Figure Redesign Suite (Revision v2).

Produces publication-grade scientific figures meeting international journal
standards (IEEE, Elsevier, Springer, Nature portfolio):
- 600 DPI PNG outputs only (no PDFs, no temporary screenshots)
- Strictly verified experimental evidence from ETD-FGL repository
- Multi-panel scientific layouts (2x2, 1x3, 2x3) inspired by clean visual references
- Clear visual distinction between single-seed baselines and multi-seed evaluations
- Exact zero reference lines for Attack Effect and paired deltas
- No clipped bars, error bars, axes, annotations, or titles
- Dedicated fix for FedTGE runtime rendering
- Clear callouts for Reddit Seed 43 and the 5-client normalization invariant
"""

from __future__ import annotations

import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Publication-grade typography and geometry
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif", "serif"],
    "font.size": 10.0,
    "axes.titlesize": 11.0,
    "axes.labelsize": 10.5,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.0,
    "legend.fontsize": 8.5,
    "figure.titlesize": 12.0,
    "axes.linewidth": 0.8,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.4,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
    "mathtext.fontset": "stix",
})

# Harmonious, colorblind-safe academic palette
PALETTE = {
    "Clean FedAvg": "#2c7bb6",          # Academic blue
    "Attacked FedAvg": "#d7191c",       # Vermilion red
    "PD-FL": "#1b9e77",                 # Emerald green
    "GSP-FL": "#7570b3",                # Slate purple
    "FLPurifier-GNN": "#e7298a",        # Magenta rose
    "DMGNN-FL": "#d95f02",              # Amber orange
    "FedTGE": "#fdae61",                # Ochre / soft orange
    "ETD-FGL": "#202020",               # Charcoal black
    "ETD-FGL (Full)": "#202020",
    "ETD-FGL (Full final)": "#202020",
    "Fixed No Update": "#2b83ba",       # Steel blue
    "Fixed No Topology": "#e66101",     # Deep orange
    "Old No Update": "#80b1d3",         # Muted sky blue
    "Old No Topology": "#fdb462",       # Muted amber
    "Topology-only": "#2b83ba",
    "Update-only": "#e66101",
    "No Trust Weighting": "#999999",    # Neutral gray
    "Historical Three-Channel": "#8c564b", # Warm brown
}

METHOD_MARKERS = {
    "Clean FedAvg": "o",
    "Attacked FedAvg": "X",
    "PD-FL": "s",
    "GSP-FL": "^",
    "FLPurifier-GNN": "D",
    "DMGNN-FL": "v",
    "FedTGE": "P",
    "ETD-FGL": "*",
}

METHOD_STYLES = {
    "Clean FedAvg": "-",
    "Attacked FedAvg": "--",
    "PD-FL": "-.",
    "GSP-FL": ":",
    "FLPurifier-GNN": "-",
    "DMGNN-FL": "--",
    "FedTGE": "-.",
    "ETD-FGL": "-",
}

DATASET_ORDER = ["Cora", "PubMed", "Reddit"]
DISPLAY_DATASETS = {"cora": "Cora", "pubmed": "PubMed", "reddit": "Reddit"}


def save_figure(fig, out_dir: Path, stem: str) -> None:
    """Save 600 DPI publication PNG."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{stem}.png"
    fig.savefig(out_path, dpi=600)
    plt.close(fig)
    print(f"[SUCCESS] Saved 600 DPI figure: {out_path.name}")


# ==============================================================================
# FIGURE A: BASELINE COMPARISONS (OVERVIEW & DATASET-SPECIFIC 2x2 PANELS)
# ==============================================================================

def generate_figure_a_overview(data_dir: Path, out_dir: Path) -> None:
    """Figure A Overview: 2x2 multi-panel baseline comparison across 3 datasets."""
    csv_file = data_dir / "baseline_seed42.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    methods = [
        "Clean FedAvg",
        "Attacked FedAvg",
        "PD-FL",
        "GSP-FL",
        "FLPurifier-GNN",
        "DMGNN-FL",
        "FedTGE",
        "ETD-FGL",
    ]

    fig, axes = plt.subplots(2, 2, figsize=(13.0, 9.2))
    plt.subplots_adjust(hspace=0.28, wspace=0.18)
    x = np.arange(len(DATASET_ORDER))
    width = 0.105

    # (a) Clean Test Accuracy
    ax_acc = axes[0, 0]
    for i, m in enumerate(methods):
        vals = [float(next(r for r in records if r["dataset"] == ds and r["method_name"] == m)["clean_test_accuracy"]) for ds in DATASET_ORDER]
        offset = (i - len(methods)/2 + 0.5) * width
        ax_acc.bar(x + offset, vals, width, label=m, color=PALETTE[m], edgecolor="black", linewidth=0.5)
    ax_acc.set_title("(a) Clean Test Accuracy (Single Seed 42)", fontweight="bold", pad=8)
    ax_acc.set_ylabel("Clean Accuracy (%)")
    ax_acc.set_xticks(x)
    ax_acc.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_acc.set_ylim(0, 100)
    ax_acc.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_acc.spines["top"].set_visible(False)
    ax_acc.spines["right"].set_visible(False)

    # (b) Backdoor Attack Success Rate (ASR)
    ax_asr = axes[0, 1]
    attacked_methods = [m for m in methods if m != "Clean FedAvg"]
    w_asr = 0.115
    for i, m in enumerate(attacked_methods):
        vals = [float(next(r for r in records if r["dataset"] == ds and r["method_name"] == m)["attack_success_rate"]) for ds in DATASET_ORDER]
        offset = (i - len(attacked_methods)/2 + 0.5) * w_asr
        ax_asr.bar(x + offset, vals, w_asr, label=m, color=PALETTE[m], edgecolor="black", linewidth=0.5)
    ax_asr.set_title("(b) Backdoor Attack Success Rate (ASR) [Lower is better]", fontweight="bold", pad=8)
    ax_asr.set_ylabel("Attack Success Rate (ASR %)")
    ax_asr.set_xticks(x)
    ax_asr.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_asr.set_ylim(0, 100)
    ax_asr.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_asr.spines["top"].set_visible(False)
    ax_asr.spines["right"].set_visible(False)

    # (c) Trigger Attack Effect (ASR - Clean Target Rate)
    ax_ae = axes[1, 0]
    for i, m in enumerate(attacked_methods):
        vals = [float(next(r for r in records if r["dataset"] == ds and r["method_name"] == m)["attack_effect"]) for ds in DATASET_ORDER]
        offset = (i - len(attacked_methods)/2 + 0.5) * w_asr
        ax_ae.bar(x + offset, vals, w_asr, label=m, color=PALETTE[m], edgecolor="black", linewidth=0.5)
    ax_ae.axhline(0.0, color="black", linestyle="-", linewidth=1.0, zorder=5)
    ax_ae.set_title("(c) Trigger Attack Effect (ASR − Clean Target Rate)", fontweight="bold", pad=8)
    ax_ae.set_ylabel("Attack Effect (% points)")
    ax_ae.set_xticks(x)
    ax_ae.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_ae.set_ylim(-15, 80)
    ax_ae.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_ae.spines["top"].set_visible(False)
    ax_ae.spines["right"].set_visible(False)

    # (d) Training Loop Runtime (Log-scale accommodating FedTGE)
    ax_rt = axes[1, 1]
    for i, m in enumerate(methods):
        vals = [float(next(r for r in records if r["dataset"] == ds and r["method_name"] == m)["elapsed_seconds"]) for ds in DATASET_ORDER]
        offset = (i - len(methods)/2 + 0.5) * width
        rects = ax_rt.bar(x + offset, vals, width, label=m, color=PALETTE[m], edgecolor="black", linewidth=0.5)
        # Add numeric label atop FedTGE bars so high runtime is explicit
        if m == "FedTGE":
            for rect, val in zip(rects, vals):
                ax_rt.annotate(f"{val:.0f}s", (rect.get_x() + rect.get_width()/2, val * 1.15),
                                ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#b25900", rotation=0)

    ax_rt.set_yscale("log")
    ax_rt.set_ylim(1.0, 2500)
    ax_rt.set_title("(d) Recorded Training Loop Runtime (50 Rounds, GPU)", fontweight="bold", pad=8)
    ax_rt.set_ylabel("Elapsed Time (seconds, log scale)")
    ax_rt.set_xticks(x)
    ax_rt.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_rt.grid(True, axis="y", linestyle="--", alpha=0.35, which="both")
    ax_rt.spines["top"].set_visible(False)
    ax_rt.spines["right"].set_visible(False)

    # Shared Legend
    handles, labels = ax_acc.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.985), ncol=4, frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure A: Comprehensive Baseline Comparison across Cora, PubMed, and Reddit (Seed 42)",
                 fontweight="bold", fontsize=12.5, y=1.015)

    save_figure(fig, out_dir, "Fig_A_Baseline_Comparison_Overview")


def generate_figure_a_per_dataset(data_dir: Path, out_dir: Path, dataset_name: str, fig_id: str) -> None:
    """Generate clean 2x2 baseline figure for a single dataset, inspired by fig3/fig5."""
    csv_file = data_dir / "baseline_seed42.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = [r for r in csv.DictReader(f) if r["dataset"].lower() == dataset_name.lower()]

    methods = [
        "Clean FedAvg",
        "Attacked FedAvg",
        "PD-FL",
        "GSP-FL",
        "FLPurifier-GNN",
        "DMGNN-FL",
        "FedTGE",
        "ETD-FGL",
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
    plt.subplots_adjust(hspace=0.36, wspace=0.24)

    # Panel (a): Clean Accuracy
    ax_a = axes[0, 0]
    vals_a = [float(next(r for r in records if r["method_name"] == m)["clean_test_accuracy"]) for m in methods]
    bars_a = ax_a.bar(range(len(methods)), vals_a, color=[PALETTE[m] for m in methods], edgecolor="black", linewidth=0.6)
    for b in bars_a:
        h = b.get_height()
        ax_a.annotate(f"{h:.1f}%", (b.get_x() + b.get_width()/2, h + 1.2), ha="center", fontsize=7.8)
    ax_a.set_title(f"(a) Clean Test Accuracy — {dataset_name}", fontweight="bold", pad=8)
    ax_a.set_ylabel("Clean Accuracy (%)")
    ax_a.set_xticks(range(len(methods)))
    ax_a.set_xticklabels(methods, rotation=35, ha="right", fontsize=8.0)
    ax_a.set_ylim(0, 105)
    ax_a.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_a.spines["top"].set_visible(False)
    ax_a.spines["right"].set_visible(False)

    # Panel (b): Backdoor ASR
    ax_b = axes[0, 1]
    att_methods = [m for m in methods if m != "Clean FedAvg"]
    vals_b = [float(next(r for r in records if r["method_name"] == m)["attack_success_rate"]) for m in att_methods]
    bars_b = ax_b.bar(range(len(att_methods)), vals_b, color=[PALETTE[m] for m in att_methods], edgecolor="black", linewidth=0.6)
    for b in bars_b:
        h = b.get_height()
        ax_b.annotate(f"{h:.1f}%", (b.get_x() + b.get_width()/2, h + 1.2), ha="center", fontsize=7.8)
    ax_b.set_title(f"(b) Backdoor ASR — {dataset_name} [Lower is better]", fontweight="bold", pad=8)
    ax_b.set_ylabel("Attack Success Rate (ASR %)")
    ax_b.set_xticks(range(len(att_methods)))
    ax_b.set_xticklabels(att_methods, rotation=35, ha="right", fontsize=8.0)
    ax_b.set_ylim(0, 105)
    ax_b.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)

    # Panel (c): Trigger Attack Effect
    ax_c = axes[1, 0]
    vals_c = [float(next(r for r in records if r["method_name"] == m)["attack_effect"]) for m in att_methods]
    bars_c = ax_c.bar(range(len(att_methods)), vals_c, color=[PALETTE[m] for m in att_methods], edgecolor="black", linewidth=0.6)
    ax_c.axhline(0.0, color="black", linestyle="-", linewidth=1.0, zorder=5)
    for b, val in zip(bars_c, vals_c):
        va = "bottom" if val >= 0 else "top"
        y_pos = val + 1.2 if val >= 0 else val - 3.2
        ax_c.annotate(f"{val:.1f}", (b.get_x() + b.get_width()/2, y_pos), ha="center", va=va, fontsize=7.8)
    ax_c.set_title(f"(c) Trigger Attack Effect — {dataset_name}", fontweight="bold", pad=8)
    ax_c.set_ylabel("Attack Effect (% points)")
    ax_c.set_xticks(range(len(att_methods)))
    ax_c.set_xticklabels(att_methods, rotation=35, ha="right", fontsize=8.0)
    min_c = min(-15, min(vals_c) - 8)
    max_c = max(80, max(vals_c) + 12)
    ax_c.set_ylim(min_c, max_c)
    ax_c.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_c.spines["top"].set_visible(False)
    ax_c.spines["right"].set_visible(False)

    # Panel (d): Training Loop Runtime (Log-scale or unclipped linear)
    ax_d = axes[1, 1]
    vals_d = [float(next(r for r in records if r["method_name"] == m)["elapsed_seconds"]) for m in methods]
    bars_d = ax_d.bar(range(len(methods)), vals_d, color=[PALETTE[m] for m in methods], edgecolor="black", linewidth=0.6)
    for b, val in zip(bars_d, vals_d):
        ax_d.annotate(f"{val:.1f}s", (b.get_x() + b.get_width()/2, val * 1.15), ha="center", fontsize=7.6, rotation=0)
    ax_d.set_yscale("log")
    ax_d.set_ylim(1.0, max(vals_d) * 3.5)
    ax_d.set_title(f"(d) Recorded Runtime (50 Rounds) — {dataset_name}", fontweight="bold", pad=8)
    ax_d.set_ylabel("Elapsed Time (seconds, log scale)")
    ax_d.set_xticks(range(len(methods)))
    ax_d.set_xticklabels(methods, rotation=35, ha="right", fontsize=8.0)
    ax_d.grid(True, axis="y", linestyle="--", alpha=0.35, which="both")
    ax_d.spines["top"].set_visible(False)
    ax_d.spines["right"].set_visible(False)

    fig.suptitle(f"Figure A{fig_id}: Baseline Method Evaluation on {dataset_name} (Seed 42)",
                 fontweight="bold", fontsize=12.5, y=0.995)

    save_figure(fig, out_dir, f"Fig_A{fig_id}_Baseline_Comparison_{dataset_name}")


# ==============================================================================
# FIGURE B: STANDARD ABLATION (PRIORITY: 6 ORIGINAL VARIANTS, MULTI-SEED)
# ==============================================================================

def generate_figure_b_standard_ablation(data_dir: Path, out_dir: Path) -> None:
    """Figure B: Standard Ablation of 6 original variants across Cora, PubMed, Reddit."""
    csv_file = data_dir / "consolidated_experiments.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = [r for r in csv.DictReader(f) if r["suite"] == "standard_ablation"]

    variants = [
        ("ETD-FGL (Full final)", "Full ETD-FGL", PALETTE["ETD-FGL"]),
        ("ETD-FGL Topology-only", "Topology-only", PALETTE["Old No Update"]),
        ("ETD-FGL Update-only", "Update-only", PALETTE["Old No Topology"]),
        ("ETD-FGL w/o Trust Weighting", "No Trust Weighting", PALETTE["No Trust Weighting"]),
        ("Historical Three-Channel Variant (0.45/0.35/0.20)", "Hist. 3-Channel", PALETTE["Historical Three-Channel"]),
        ("Attacked FedAvg", "Attacked FedAvg", PALETTE["Attacked FedAvg"]),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(13.0, 9.2))
    plt.subplots_adjust(hspace=0.28, wspace=0.18)
    x = np.arange(len(DATASET_ORDER))
    width = 0.125

    metrics = [
        (axes[0, 0], "clean_test_accuracy", "(a) Clean Test Accuracy (Seeds 42, 43, 44)", "Clean Accuracy (%)", (0, 100), False),
        (axes[0, 1], "attack_success_rate", "(b) Backdoor Attack Success Rate (ASR)", "Attack Success Rate (ASR %)", (0, 100), False),
        (axes[1, 0], "attack_effect", "(c) Trigger Attack Effect (ASR − Clean Target Rate)", "Attack Effect (% points)", (-15, 85), True),
        (axes[1, 1], "attacker_weight_mean", "(d) Attacker Aggregation Weight Share", "Attacker Weight (%)", (0, 25), False),
    ]

    for ax, metric_key, title, ylabel, ylim, zero_line in metrics:
        if zero_line:
            ax.axhline(0.0, color="black", linestyle="-", linewidth=1.0, zorder=5)
        if metric_key == "attacker_weight_mean":
            ax.axhline(20.0, color="gray", linestyle="-.", linewidth=0.9, alpha=0.7, label="Uniform Share (20%)")

        for v_idx, (v_name, v_label, color) in enumerate(variants):
            means, stds = [], []
            for ds_idx, ds in enumerate(DATASET_ORDER):
                runs = [r for r in records if r["dataset"] == ds and r["method_name"] == v_name]
                if metric_key == "attacker_weight_mean" and v_name == "Attacked FedAvg":
                    # Implicit uniform share 20% for unweighted FedAvg (5 clients)
                    vals = [20.0, 20.0, 20.0]
                else:
                    vals = [float(r[metric_key]) for r in runs if r[metric_key] != ""]

                m_val = float(np.mean(vals)) if vals else 0.0
                s_val = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
                means.append(m_val)
                stds.append(s_val)

                # Overlay individual seed points
                offset = (v_idx - len(variants)/2 + 0.5) * width
                jitter = np.array([-0.025, 0.0, 0.025])
                for pt_idx, v in enumerate(vals):
                    ax.scatter(
                        x[ds_idx] + offset + (jitter[pt_idx] if len(vals) == 3 else 0),
                        v,
                        color="white",
                        s=18,
                        edgecolors=color,
                        linewidth=0.9,
                        zorder=6,
                    )

            offset = (v_idx - len(variants)/2 + 0.5) * width
            ax.bar(
                x + offset,
                means,
                width,
                yerr=stds,
                capsize=2.8,
                error_kw=dict(lw=0.8, capthick=0.8),
                label=v_label,
                color=color,
                edgecolor="black",
                linewidth=0.6,
                alpha=0.85,
            )

        ax.set_title(title, fontweight="bold", pad=8)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(DATASET_ORDER, fontweight="semibold")
        ax.set_ylim(ylim)
        ax.grid(True, axis="y", linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.985), ncol=6, frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure B: Standard Multi-Seed Ablation Study across Cora, PubMed, and Reddit (Seeds 42, 43, 44)",
                 fontweight="bold", fontsize=12.5, y=1.015)

    save_figure(fig, out_dir, "Fig_B_Standard_Ablation")


# ==============================================================================
# FIGURE C: CONTROLLED ABLATION (FIXED COEFFICIENTS & PAIRED DELTAS)
# ==============================================================================

def generate_figure_c_controlled_ablation(data_dir: Path, out_dir: Path) -> None:
    """Figure C: Controlled scientific ablation isolating channels with held-constant coefficients."""
    csv_file = data_dir / "controlled_ablation_summary.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    paired_csv = data_dir / "paired_differences.csv"
    with paired_csv.open("r", encoding="utf-8") as f:
        paired_records = list(csv.DictReader(f))

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.8))
    plt.subplots_adjust(hspace=0.28, wspace=0.20)
    x = np.arange(len(DATASET_ORDER))
    width = 0.22

    ctrl_variants = [
        ("etdfgl_full", "Full ETD-FGL (9/13 Topo + 4/13 Upd)", PALETTE["ETD-FGL"], -width),
        ("etdfgl_fixed_no_update", "Fixed No Update (9/13 Topo)", PALETTE["Fixed No Update"], 0.0),
        ("etdfgl_fixed_no_topology", "Fixed No Topology (4/13 Upd)", PALETTE["Fixed No Topology"], width),
    ]

    # (a) Backdoor ASR
    ax_asr = axes[0, 0]
    for slug, label, color, offset in ctrl_variants:
        asrs, errs = [], []
        for ds in DATASET_ORDER:
            m = next(r for r in records if r["dataset"] == ds and r["variant_slug"] == slug)
            mean_str, std_str = m["asr_display"].split(" ± ")
            asrs.append(float(mean_str))
            errs.append(float(std_str))
        ax_asr.bar(x + offset, asrs, width, yerr=errs, capsize=3.0, label=label, color=color, edgecolor="black", linewidth=0.7)
    ax_asr.set_title("(a) Backdoor ASR under Held-Constant Coefficients", fontweight="bold", pad=8)
    ax_asr.set_ylabel("Attack Success Rate (ASR %)")
    ax_asr.set_xticks(x)
    ax_asr.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_asr.set_ylim(0, 100)
    ax_asr.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_asr.spines["top"].set_visible(False)
    ax_asr.spines["right"].set_visible(False)

    # (b) Paired ASR Degradation (Delta = Variant - Full)
    ax_dasr = axes[0, 1]
    p_variants = [
        ("etdfgl_fixed_no_update", "Δ No Update (vs Full)", PALETTE["Fixed No Update"], -width/2),
        ("etdfgl_fixed_no_topology", "Δ No Topology (vs Full)", PALETTE["Fixed No Topology"], width/2),
    ]
    ax_dasr.axhline(0.0, color="black", linestyle="-", linewidth=1.0, zorder=5)
    for slug, label, color, offset in p_variants:
        dasrs, d_errs = [], []
        for ds in DATASET_ORDER:
            m = next(r for r in paired_records if r["dataset"] == ds and r["variant_slug"] == slug)
            mean_str, std_str = m["delta_asr"].split(" ± ")
            dasrs.append(float(mean_str))
            d_errs.append(float(std_str))
        bars = ax_dasr.bar(x + offset, dasrs, width, yerr=d_errs, capsize=3.0, label=label, color=color, edgecolor="black", linewidth=0.7)
        for b, v in zip(bars, dasrs):
            ax_dasr.annotate(f"+{v:.1f}%", (b.get_x() + b.get_width()/2, v + 2.5), ha="center", fontsize=8.0, fontweight="bold")
    ax_dasr.set_title("(b) Paired ASR Degradation (Δ = Variant − Full ETD-FGL)", fontweight="bold", pad=8)
    ax_dasr.set_ylabel("Δ ASR (% points)  [Higher = Worse defense]")
    ax_dasr.set_xticks(x)
    ax_dasr.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_dasr.set_ylim(-5, 75)
    ax_dasr.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_dasr.spines["top"].set_visible(False)
    ax_dasr.spines["right"].set_visible(False)

    # (c) Clean Accuracy
    ax_acc = axes[1, 0]
    for slug, label, color, offset in ctrl_variants:
        accs, a_errs = [], []
        for ds in DATASET_ORDER:
            m = next(r for r in records if r["dataset"] == ds and r["variant_slug"] == slug)
            mean_str, std_str = m["clean_accuracy_display"].split(" ± ")
            accs.append(float(mean_str))
            a_errs.append(float(std_str))
        ax_acc.bar(x + offset, accs, width, yerr=a_errs, capsize=3.0, label=label, color=color, edgecolor="black", linewidth=0.7)
    ax_acc.set_title("(c) Clean Test Accuracy across Controlled Variants", fontweight="bold", pad=8)
    ax_acc.set_ylabel("Clean Accuracy (%)")
    ax_acc.set_xticks(x)
    ax_acc.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_acc.set_ylim(0, 100)
    ax_acc.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_acc.spines["top"].set_visible(False)
    ax_acc.spines["right"].set_visible(False)

    # (d) Paired Clean Accuracy Difference
    ax_dacc = axes[1, 1]
    ax_dacc.axhline(0.0, color="black", linestyle="-", linewidth=1.0, zorder=5)
    for slug, label, color, offset in p_variants:
        daccs, da_errs = [], []
        for ds in DATASET_ORDER:
            m = next(r for r in paired_records if r["dataset"] == ds and r["variant_slug"] == slug)
            mean_str, std_str = m["delta_clean_accuracy"].split(" ± ")
            daccs.append(float(mean_str))
            da_errs.append(float(std_str))
        ax_dacc.bar(x + offset, daccs, width, yerr=da_errs, capsize=3.0, label=label, color=color, edgecolor="black", linewidth=0.7)
    ax_dacc.set_title("(d) Paired Clean Accuracy Difference (Δ = Variant − Full)", fontweight="bold", pad=8)
    ax_dacc.set_ylabel("Δ Clean Accuracy (% points)")
    ax_dacc.set_xticks(x)
    ax_dacc.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_dacc.set_ylim(-4, 4)
    ax_dacc.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_dacc.spines["top"].set_visible(False)
    ax_dacc.spines["right"].set_visible(False)

    handles, labels = ax_asr.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.985), ncol=3, frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure C: Controlled Ablation with Held-Constant Coefficients (Seeds 42, 43, 44)",
                 fontweight="bold", fontsize=12.5, y=1.015)

    save_figure(fig, out_dir, "Fig_C_Controlled_Ablation")


# ==============================================================================
# FIGURE D: MULTI-SEED PERFORMANCE (WITH PROMINENT REDDIT SEED 43 CALLOUT)
# ==============================================================================

def generate_figure_d_multiseed_robustness(data_dir: Path, out_dir: Path) -> None:
    """Figure D: Multi-Seed Robustness comparing Attacked FedAvg vs Full ETD-FGL."""
    csv_file = data_dir / "consolidated_experiments.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = [r for r in csv.DictReader(f) if r["suite"] == "multiseed"]

    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.8))
    plt.subplots_adjust(wspace=0.22)
    x = np.arange(len(DATASET_ORDER))
    width = 0.28

    panels = [
        (axes[0], "clean_test_accuracy", "(a) Clean Test Accuracy", "Clean Accuracy (%)", (65, 95), False),
        (axes[1], "attack_success_rate", "(b) Backdoor Attack Success Rate (ASR)", "Attack Success Rate (ASR %)", (-2, 100), False),
        (axes[2], "attack_effect", "(c) Trigger Attack Effect", "Attack Effect (% points)", (-15, 85), True),
    ]

    for ax, metric_key, title, ylabel, ylim, zero_line in panels:
        if zero_line:
            ax.axhline(0.0, color="black", linestyle="-", linewidth=1.0, zorder=5)

        for m_idx, (m_name, color, offset) in enumerate([
            ("Attacked FedAvg", PALETTE["Attacked FedAvg"], -width/2),
            ("ETD-FGL", PALETTE["ETD-FGL"], width/2),
        ]):
            means, stds = [], []
            for ds_idx, ds in enumerate(DATASET_ORDER):
                runs = [r for r in records if r["dataset"] == ds and r["method_name"] == m_name]
                vals = [float(r[metric_key]) for r in runs]
                m_val = float(np.mean(vals))
                s_val = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
                means.append(m_val)
                stds.append(s_val)

                # Overlay individual seeds with jitter
                seed_x = x[ds_idx] + offset + np.array([-0.04, 0.0, 0.04])
                for pt_idx, r in enumerate(runs):
                    v = float(r[metric_key])
                    s = int(r["seed"])
                    # PROMINENT CALLOUT FOR REDDIT SEED 43
                    if ds == "Reddit" and s == 43 and m_name == "ETD-FGL" and metric_key == "attack_success_rate":
                        ax.scatter(seed_x[pt_idx], v, color="#b2182b", s=65, edgecolors="black", linewidth=1.2, zorder=7, marker="^")
                        ax.annotate("Reddit Seed 43\n(ASR: 34.8%)", (seed_x[pt_idx], v),
                                    xytext=(seed_x[pt_idx] + 0.08, v + 9.0),
                                    fontsize=8.0, fontweight="bold", color="#990000",
                                    arrowprops=dict(arrowstyle="->", color="#990000", lw=1.0))
                    elif ds == "Reddit" and s == 43 and m_name == "ETD-FGL" and metric_key == "attack_effect":
                        ax.scatter(seed_x[pt_idx], v, color="#b2182b", s=65, edgecolors="black", linewidth=1.2, zorder=7, marker="^")
                        ax.annotate("Reddit Seed 43\n(Effect: 34.4%)", (seed_x[pt_idx], v),
                                    xytext=(seed_x[pt_idx] + 0.08, v + 9.0),
                                    fontsize=8.0, fontweight="bold", color="#990000",
                                    arrowprops=dict(arrowstyle="->", color="#990000", lw=1.0))
                    else:
                        ax.scatter(seed_x[pt_idx], v, color="white", s=28, edgecolors=color, linewidth=1.0, zorder=6)

            ax.bar(x + offset, means, width, yerr=stds, capsize=3.5,
                   error_kw=dict(lw=0.9, capthick=0.9),
                   label=m_name if ax == axes[0] else None,
                   color=color, alpha=0.82, edgecolor="black", linewidth=0.7)

        ax.set_title(title, fontweight="bold", pad=8)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(DATASET_ORDER, fontweight="semibold")
        ax.set_ylim(ylim)
        ax.grid(True, axis="y", linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].legend(loc="lower left", frameon=True, edgecolor="#cccccc")
    fig.suptitle("Figure D: Multi-Seed Performance Comparison (Seeds 42, 43, 44)",
                 fontweight="bold", fontsize=12.5, y=1.01)

    save_figure(fig, out_dir, "Fig_D_MultiSeed_Robustness")


# ==============================================================================
# FIGURE E: FEDERATED LEARNING DYNAMICS (50 COMMUNICATION ROUNDS)
# ==============================================================================

def generate_figure_e_learning_dynamics(project_dir: Path, out_dir: Path) -> None:
    """Figure E: 50-round training dynamics across Cora, PubMed, and Reddit."""
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 7.2), sharex=True)
    plt.subplots_adjust(hspace=0.24, wspace=0.20)

    methods = [
        ("Clean FedAvg", "fedavg_clean"),
        ("Attacked FedAvg", "fedavg_structural_backdoor"),
        ("FedTGE", "baseline_fedtge"),
        ("ETD-FGL", "defended_etdfgl"),
    ]

    for col_idx, ds in enumerate(["cora", "pubmed", "reddit"]):
        ds_display = DISPLAY_DATASETS[ds]
        base_dir = project_dir / "outputs" / "final_multidataset" / f"federated_{ds}"

        ax_acc = axes[0, col_idx]
        ax_asr = axes[1, col_idx]

        for m_name, slug in methods:
            hist_path = base_dir / slug / "training_history.csv"
            if not hist_path.is_file():
                continue
            with hist_path.open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

            rounds = [int(r["round"]) for r in rows]
            accs = [float(r["test_accuracy"]) * 100.0 for r in rows]
            asrs = [float(r["attack_success_rate"]) * 100.0 if r.get("attack_success_rate", "") != "" else 0.0 for r in rows]

            color = PALETTE[m_name]
            ls = METHOD_STYLES[m_name]
            marker = METHOD_MARKERS[m_name]

            ax_acc.plot(rounds, accs, label=m_name if col_idx == 0 else None,
                        color=color, linestyle=ls, marker=marker, markevery=5, markersize=4.2, linewidth=1.5)

            if m_name != "Clean FedAvg":
                ax_asr.plot(rounds, asrs, label=m_name if col_idx == 0 else None,
                            color=color, linestyle=ls, marker=marker, markevery=5, markersize=4.2, linewidth=1.5)

        ax_acc.set_title(f"{ds_display}: Clean Accuracy", fontweight="bold", pad=6)
        if col_idx == 0:
            ax_acc.set_ylabel("Accuracy (%)")
        ax_acc.set_ylim(0, 100)
        ax_acc.grid(True, linestyle="--", alpha=0.3)
        ax_acc.spines["top"].set_visible(False)
        ax_acc.spines["right"].set_visible(False)

        ax_asr.set_title(f"{ds_display}: Backdoor ASR", fontweight="bold", pad=6)
        ax_asr.set_xlabel("Communication Round")
        if col_idx == 0:
            ax_asr.set_ylabel("ASR (%)")
        ax_asr.set_ylim(-2, 100)
        ax_asr.grid(True, linestyle="--", alpha=0.3)
        ax_asr.spines["top"].set_visible(False)
        ax_asr.spines["right"].set_visible(False)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.985), ncol=4, frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure E: Federated Learning Dynamics over 50 Communication Rounds (Seed 42)",
                 fontweight="bold", fontsize=12.5, y=1.015)

    save_figure(fig, out_dir, "Fig_E_Learning_Dynamics")


# ==============================================================================
# FIGURE F: TRUST AND DEFENSE MECHANISM (RISK DYNAMICS & AGGREGATION SUPPRESSION)
# ==============================================================================

def generate_figure_f_trust_defense(project_dir: Path, out_dir: Path) -> None:
    """Figure F: Dynamic client risk decomposition, attacker weight suppression, and benign trust."""
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.8))
    plt.subplots_adjust(hspace=0.28, wspace=0.20)

    # Load Cora defended_etdfgl history (representative)
    cora_hist = project_dir / "outputs" / "final_multidataset" / "federated_cora" / "defended_etdfgl" / "training_history.csv"
    with cora_hist.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rounds = [int(r["round"]) for r in rows]

    # Panel (a): Attacker Aggregation Weight Suppression across Datasets
    ax_wt = axes[0, 0]
    for ds, color, ls in [("cora", "#2c7bb6", "-"), ("pubmed", "#1b9e77", "--"), ("reddit", "#d95f02", "-.")]:
        h_path = project_dir / "outputs" / "final_multidataset" / f"federated_{ds}" / "defended_etdfgl" / "training_history.csv"
        if h_path.is_file():
            with h_path.open("r", encoding="utf-8") as f:
                d_rows = list(csv.DictReader(f))
            d_rounds = [int(r["round"]) for r in d_rows]
            d_wts = [float(r["etdfgl_weight_client_0"]) * 100.0 for r in d_rows]
            ax_wt.plot(d_rounds, d_wts, label=DISPLAY_DATASETS[ds], color=color, linestyle=ls, linewidth=1.6)

    ax_wt.axhline(20.0, color="gray", linestyle=":", linewidth=1.1, label="Uniform Weight (20%)")
    ax_wt.set_title("(a) Dynamic Attacker Aggregation Weight ($w_0$)", fontweight="bold", pad=8)
    ax_wt.set_xlabel("Communication Round")
    ax_wt.set_ylabel("Attacker Weight Share (%)")
    ax_wt.set_ylim(0, 25)
    ax_wt.grid(True, linestyle="--", alpha=0.35)
    ax_wt.spines["top"].set_visible(False)
    ax_wt.spines["right"].set_visible(False)
    ax_wt.legend(loc="center right", frameon=True, edgecolor="#cccccc")

    # Panel (b): Risk Decomposition for Malicious Client 0 (Cora)
    ax_risk = axes[0, 1]
    topo_risk = [float(r["etdfgl_topology_risk_client_0"]) for r in rows]
    upd_risk = [float(r["etdfgl_update_risk_client_0"]) for r in rows]
    fused_risk = [float(r["etdfgl_fused_risk_client_0"]) for r in rows]

    ax_risk.plot(rounds, topo_risk, label="Topology Anomaly ($A_0^{\\mathrm{topo}}$)", color="#2b83ba", linestyle="-", linewidth=1.5)
    ax_risk.plot(rounds, upd_risk, label="Update Anomaly ($A_0^{\\mathrm{upd}}$)", color="#e66101", linestyle="--", linewidth=1.5)
    ax_risk.plot(rounds, fused_risk, label="Fused Risk ($R_0$)", color="#202020", linestyle="-", linewidth=1.8)

    ax_risk.set_title("(b) Attacker Risk Decomposition (Cora)", fontweight="bold", pad=8)
    ax_risk.set_xlabel("Communication Round")
    ax_risk.set_ylabel("Anomaly / Risk Score")
    ax_risk.set_ylim(0, 1.05)
    ax_risk.grid(True, linestyle="--", alpha=0.35)
    ax_risk.spines["top"].set_visible(False)
    ax_risk.spines["right"].set_visible(False)
    ax_risk.legend(loc="center right", frameon=True, edgecolor="#cccccc")

    # Panel (c): Benign vs Malicious Client Trust Factor
    ax_trust = axes[1, 0]
    mal_trust = [float(r["etdfgl_trust_client_0"]) for r in rows]
    benign_trust_avg = [
        np.mean([float(r[f"etdfgl_trust_client_{k}"]) for k in range(1, 5)])
        for r in rows
    ]

    ax_trust.plot(rounds, benign_trust_avg, label="Benign Clients (Mean $T_{1..4}$)", color="#1b9e77", linestyle="-", linewidth=1.8)
    ax_trust.plot(rounds, mal_trust, label="Attacker Client ($T_0$)", color="#d7191c", linestyle="--", linewidth=1.8)

    ax_trust.set_title("(c) Client Trust Trajectory ($T_k = \\exp(-3 R_k)$)", fontweight="bold", pad=8)
    ax_trust.set_xlabel("Communication Round")
    ax_trust.set_ylabel("Trust Factor $T_k \\in (0, 1]$")
    ax_trust.set_ylim(0, 1.05)
    ax_trust.grid(True, linestyle="--", alpha=0.35)
    ax_trust.spines["top"].set_visible(False)
    ax_trust.spines["right"].set_visible(False)
    ax_trust.legend(loc="center right", frameon=True, edgecolor="#cccccc")

    # Panel (d): 5-Client Normalization Invariant Demonstration
    ax_inv = axes[1, 1]
    # Under _robust_positive([d, 0, 0, 0, 0]), z0 = d / (0.4 d) = 2.5
    # Anomaly = 2*(sigmoid(2.5) - 0.5) = 0.8483 for any drift d > 0!
    drifts = np.linspace(0.01, 2.0, 100)
    # Computed robust anomaly
    z_scores = drifts / (0.4 * drifts) # = 2.5 exactly
    anomalies = 2.0 * (1.0 / (1.0 + np.exp(-z_scores)) - 0.5) # = 0.8483
    # Weight share under fixed No Update: R = 9/13 * 0.8483 = 0.5873, T = exp(-3*0.5873)=0.1717
    # w0 = 0.1717 / (0.1717 + 4) = 4.12%
    weights_fixed = np.full_like(drifts, (np.exp(-3.0 * (9.0/13.0) * 0.84828) / (np.exp(-3.0 * (9.0/13.0) * 0.84828) + 4.0)) * 100.0)

    ax_inv.plot(drifts, anomalies, label="Topology Anomaly $A_0^{\\mathrm{topo}} \\equiv 0.8483$", color="#2b83ba", linewidth=2.0)
    ax_inv.axhline(0.84828, color="#2b83ba", linestyle=":", linewidth=1.0)
    ax_inv.plot(drifts, weights_fixed / 100.0, label="Fixed No Update Weight $w_0 \\equiv 4.12\\%$", color="#d7191c", linewidth=2.0, linestyle="--")

    ax_inv.annotate("5-Client Constant Invariant:\n$z_0 = d / (0.4 d) \\equiv 2.5$\n$A_0^{\\mathrm{topo}} = 2(\\sigma(2.5) - 0.5) \\approx 0.8483$",
                    xy=(1.0, 0.8483), xytext=(0.4, 0.55),
                    fontsize=8.2, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color="black", lw=0.9),
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f0f0", edgecolor="#aaaaaa"))

    ax_inv.set_title("(d) Topological Drift Scale-Invariance Property", fontweight="bold", pad=8)
    ax_inv.set_xlabel("Topological Drift Magnitude $d > 0$")
    ax_inv.set_ylabel("Metric Value")
    ax_inv.set_ylim(0, 1.05)
    ax_inv.grid(True, linestyle="--", alpha=0.35)
    ax_inv.spines["top"].set_visible(False)
    ax_inv.spines["right"].set_visible(False)
    ax_inv.legend(loc="upper right", frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure F: ETD-FGL Defense Mechanism Dynamics and Mathematical Invariants",
                 fontweight="bold", fontsize=12.5, y=0.995)

    save_figure(fig, out_dir, "Fig_F_Trust_Defense_Mechanisms")


# ==============================================================================
# FIGURE G: ATTACK EFFECT & RELATIVE DEFENSE IMPROVEMENT
# ==============================================================================

def generate_figure_g_attack_effect_gain(data_dir: Path, out_dir: Path) -> None:
    """Figure G: Trigger Attack Effect and relative backdoor defense improvement."""
    b_csv = data_dir / "baseline_seed42.csv"
    with b_csv.open("r", encoding="utf-8") as f:
        b_records = list(csv.DictReader(f))

    ms_csv = data_dir / "multiseed_summary.csv"
    with ms_csv.open("r", encoding="utf-8") as f:
        ms_records = list(csv.DictReader(f))

    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.6))
    plt.subplots_adjust(wspace=0.22)
    x = np.arange(len(DATASET_ORDER))

    # Panel (a): Trigger Attack Effect across Baselines (Seed 42)
    ax_a = axes[0]
    attacked_methods = ["Attacked FedAvg", "PD-FL", "GSP-FL", "FLPurifier-GNN", "DMGNN-FL", "FedTGE", "ETD-FGL"]
    w = 0.115
    ax_a.axhline(0.0, color="black", linestyle="-", linewidth=1.1, zorder=5)
    for i, m in enumerate(attacked_methods):
        vals = [float(next(r for r in b_records if r["dataset"] == ds and r["method_name"] == m)["attack_effect"]) for ds in DATASET_ORDER]
        offset = (i - len(attacked_methods)/2 + 0.5) * w
        ax_a.bar(x + offset, vals, w, label=m, color=PALETTE[m], edgecolor="black", linewidth=0.5)
    ax_a.set_title("(a) Trigger Attack Effect (Seed 42)", fontweight="bold", pad=8)
    ax_a.set_ylabel("Attack Effect (% points)")
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_a.set_ylim(-15, 80)
    ax_a.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_a.spines["top"].set_visible(False)
    ax_a.spines["right"].set_visible(False)
    ax_a.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=4, frameon=True, edgecolor="#cccccc")

    # Panel (b): Absolute ASR Reduction (FedAvg - ETD-FGL) across Seeds 42, 43, 44
    ax_b = axes[1]
    abs_reductions = []
    abs_errs = []
    for ds in DATASET_ORDER:
        fa_m = float(next(r for r in ms_records if r["dataset"] == ds and r["method"] == "Attacked FedAvg")["asr_mean"])
        fa_s = float(next(r for r in ms_records if r["dataset"] == ds and r["method"] == "Attacked FedAvg")["asr_std"])
        et_m = float(next(r for r in ms_records if r["dataset"] == ds and r["method"] == "ETD-FGL")["asr_mean"])
        et_s = float(next(r for r in ms_records if r["dataset"] == ds and r["method"] == "ETD-FGL")["asr_std"])
        # Pooled sample standard deviation
        delta_m = fa_m - et_m
        delta_s = np.sqrt(fa_s**2 + et_s**2)
        abs_reductions.append(delta_m)
        abs_errs.append(delta_s)

    bars_b = ax_b.bar(x, abs_reductions, 0.45, yerr=abs_errs, capsize=4.0, color="#2c7bb6", edgecolor="black", linewidth=0.8)
    for b, val in zip(bars_b, abs_reductions):
        ax_b.annotate(f"−{val:.1f}%", (b.get_x() + b.get_width()/2, val + 2.5), ha="center", fontsize=8.5, fontweight="bold")
    ax_b.set_title("(b) Absolute ASR Reduction (FedAvg − ETD-FGL)", fontweight="bold", pad=8)
    ax_b.set_ylabel("Absolute Reduction (% points)")
    ax_b.set_xticks(x)
    ax_b.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_b.set_ylim(0, 85)
    ax_b.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)

    # Panel (c): Relative Backdoor Reduction Percentage
    ax_c = axes[2]
    rel_reductions = []
    for ds in DATASET_ORDER:
        fa_m = float(next(r for r in ms_records if r["dataset"] == ds and r["method"] == "Attacked FedAvg")["asr_mean"])
        et_m = float(next(r for r in ms_records if r["dataset"] == ds and r["method"] == "ETD-FGL")["asr_mean"])
        rel = ((fa_m - et_m) / fa_m) * 100.0 if fa_m > 0 else 0.0
        rel_reductions.append(rel)

    bars_c = ax_c.bar(x, rel_reductions, 0.45, color="#1b9e77", edgecolor="black", linewidth=0.8)
    for b, val in zip(bars_c, rel_reductions):
        ax_c.annotate(f"{val:.1f}%", (b.get_x() + b.get_width()/2, val + 2.0), ha="center", fontsize=8.5, fontweight="bold")
    ax_c.set_title("(c) Relative Backdoor Reduction Rate (%)", fontweight="bold", pad=8)
    ax_c.set_ylabel("Relative Reduction ($\\%$)")
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_c.set_ylim(0, 115)
    ax_c.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_c.spines["top"].set_visible(False)
    ax_c.spines["right"].set_visible(False)

    fig.suptitle("Figure G: Trigger Attack Effect and Relative Defense Improvements",
                 fontweight="bold", fontsize=12.5, y=1.05)

    save_figure(fig, out_dir, "Fig_G_Attack_Effect_and_Defense_Gain")


# ==============================================================================
# FIGURE H: ACCURACY-ROBUSTNESS TRADE-OFF (DATASET-SEPARATED PANELS)
# ==============================================================================

def generate_figure_h_tradeoff(data_dir: Path, out_dir: Path) -> None:
    """Figure H: Dataset-separated accuracy vs backdoor robustness trade-off."""
    b_csv = data_dir / "baseline_seed42.csv"
    with b_csv.open("r", encoding="utf-8") as f:
        b_records = list(csv.DictReader(f))

    ms_csv = data_dir / "multiseed_summary.csv"
    with ms_csv.open("r", encoding="utf-8") as f:
        ms_records = list(csv.DictReader(f))

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.8))
    plt.subplots_adjust(wspace=0.22)

    for idx, ds in enumerate(DATASET_ORDER):
        ax = axes[idx]
        ds_b = [r for r in b_records if r["dataset"] == ds and r["method_name"] != "Clean FedAvg"]

        # Plot single-seed baselines
        for r in ds_b:
            m = r["method_name"]
            acc = float(r["clean_test_accuracy"])
            asr = float(r["attack_success_rate"])
            ax.scatter(acc, asr, color=PALETTE.get(m, "#555555"),
                       marker=METHOD_MARKERS.get(m, "o"), s=55, alpha=0.75,
                       edgecolors="black", linewidth=0.7, label=m if idx == 0 else None)
            # Annotate baselines cleanly
            if m in ["PD-FL", "FedTGE", "FLPurifier-GNN", "DMGNN-FL", "GSP-FL"]:
                ax.annotate(m, (acc, asr), xytext=(acc + 0.3, asr + 1.8), fontsize=7.2, alpha=0.85)

        # Plot multi-seed centroids with whiskers for Attacked FedAvg and ETD-FGL
        for m in ["Attacked FedAvg", "ETD-FGL"]:
            ms_row = next(r for r in ms_records if r["dataset"] == ds and r["method"] == m)
            acc_m = float(ms_row["clean_accuracy_mean"])
            acc_s = float(ms_row["clean_accuracy_std"])
            asr_m = float(ms_row["asr_mean"])
            asr_s = float(ms_row["asr_std"])

            color = PALETTE[m]
            marker = METHOD_MARKERS[m]
            size = 120 if m == "ETD-FGL" else 85

            ax.errorbar(acc_m, asr_m, xerr=acc_s, yerr=asr_s, fmt=marker,
                        color=color, ecolor=color, elinewidth=1.4, capsize=3.5,
                        markersize=9 if m == "ETD-FGL" else 7,
                        markeredgecolor="black", markeredgewidth=0.9, zorder=6,
                        label=f"{m} (Mean ± SD)" if idx == 0 else None)

            ax.annotate(f"{m}\n({acc_m:.1f}%, {asr_m:.1f}%)", (acc_m, asr_m),
                        xytext=(acc_m + 0.5, asr_m + (3.0 if m == "ETD-FGL" else -5.5)),
                        fontsize=7.8, fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=color, alpha=0.85))

        # Directional arrow indicating desirable region
        ax.annotate("Desirable Defense Region\n(High Acc, Low ASR)",
                    xy=(ax.get_xlim()[1] if idx != 2 else 86.5, 0.5),
                    xytext=(ax.get_xlim()[1] - 4.5 if idx != 2 else 81.5, 18.0),
                    fontsize=7.6, fontstyle="italic", color="#006600",
                    arrowprops=dict(arrowstyle="->", color="#006600", lw=1.1))

        ax.set_title(f"{ds}: Accuracy vs Backdoor Robustness", fontweight="bold", pad=8)
        ax.set_xlabel("Clean Test Accuracy (%)  [Higher is better $\\rightarrow$]")
        if idx == 0:
            ax.set_ylabel("Attack Success Rate (ASR %)  [Lower is better $\\leftarrow$]")
        ax.set_ylim(-3, 85)
        ax.grid(True, linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].legend(loc="upper left", bbox_to_anchor=(-0.05, 1.25), ncol=5, frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure H: Clean Accuracy versus Robustness (ASR) Trade-Off by Dataset",
                 fontweight="bold", fontsize=12.5, y=1.06)

    save_figure(fig, out_dir, "Fig_H_Accuracy_ASR_Tradeoff")


# ==============================================================================
# FIGURE I: RUNTIME COMPARISON (CRITICAL DEFECT FIX: FedTGE FULLY RENDERED)
# ==============================================================================

def generate_figure_i_runtime(data_dir: Path, out_dir: Path) -> None:
    """Figure I: Federated training runtime comparison with complete FedTGE bars rendered."""
    csv_file = data_dir / "baseline_seed42.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    methods_order = [
        "Clean FedAvg",
        "Attacked FedAvg",
        "PD-FL",
        "GSP-FL",
        "FLPurifier-GNN",
        "DMGNN-FL",
        "FedTGE",
        "ETD-FGL",
    ]

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.0), gridspec_kw={"width_ratios": [1.4, 1.0]})
    plt.subplots_adjust(wspace=0.24)

    # Panel (a): Log-scale grouped comparison across datasets
    ax_log = axes[0]
    x = np.arange(len(DATASET_ORDER))
    width = 0.105

    for i, m in enumerate(methods_order):
        vals = [float(next(r for r in records if r["dataset"] == ds and r["method_name"] == m)["elapsed_seconds"]) for ds in DATASET_ORDER]
        offset = (i - len(methods_order)/2 + 0.5) * width
        rects = ax_log.bar(x + offset, vals, width, label=m, color=PALETTE[m], edgecolor="black", linewidth=0.5)

        # Callout FedTGE values explicitly
        if m == "FedTGE":
            for rect, val in zip(rects, vals):
                ax_log.annotate(f"{val:.0f}s", (rect.get_x() + rect.get_width()/2, val * 1.18),
                                ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#b25900")

    ax_log.set_yscale("log")
    ax_log.set_ylim(1.0, 3000)
    ax_log.set_title("(a) Multi-Dataset Runtime Comparison (Logarithmic Scale)", fontweight="bold", pad=8)
    ax_log.set_ylabel("Elapsed Time (seconds, log scale)")
    ax_log.set_xticks(x)
    ax_log.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_log.grid(True, axis="y", linestyle="--", alpha=0.35, which="both")
    ax_log.spines["top"].set_visible(False)
    ax_log.spines["right"].set_visible(False)

    # Panel (b): Detailed breakdown of FedTGE vs ETD-FGL vs Baselines on PubMed
    ax_pm = axes[1]
    pm_records = [r for r in records if r["dataset"] == "PubMed"]
    pm_vals = [float(next(r for r in pm_records if r["method_name"] == m)["elapsed_seconds"]) for m in methods_order]
    bars_pm = ax_pm.bar(range(len(methods_order)), pm_vals, color=[PALETTE[m] for m in methods_order], edgecolor="black", linewidth=0.6)

    for b, val in zip(bars_pm, pm_vals):
        ax_pm.annotate(f"{val:.1f}s", (b.get_x() + b.get_width()/2, val + 15),
                       ha="center", fontsize=7.5, fontweight="bold" if val > 100 else "normal",
                       color="#b25900" if val > 100 else "black")

    ax_pm.set_title("(b) PubMed Training Loop Runtime (Linear Scale)", fontweight="bold", pad=8)
    ax_pm.set_ylabel("Elapsed Time (seconds)")
    ax_pm.set_xticks(range(len(methods_order)))
    ax_pm.set_xticklabels(methods_order, rotation=35, ha="right", fontsize=8.0)
    ax_pm.set_ylim(0, 900) # Full scale ensuring FedTGE (773.3s) is unclipped
    ax_pm.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_pm.spines["top"].set_visible(False)
    ax_pm.spines["right"].set_visible(False)

    # Shared Legend cleanly placed above plots without title overlap
    handles, labels = ax_log.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=4, frameon=True, edgecolor="#cccccc")

    fig.suptitle("Figure I: Federated Training Loop Runtime Comparison (50 Rounds, GPU-Accelerated)",
                 fontweight="bold", fontsize=12.5, y=1.11)

    save_figure(fig, out_dir, "Fig_I_Training_Runtime_Comparison")


# ==============================================================================
# SUPPLEMENTARY FIGURES: REDDIT HETEROGENEITY & STANDARD VS CONTROLLED ABLATION
# ==============================================================================

def generate_figure_s_reddit_seeds(data_dir: Path, out_dir: Path) -> None:
    """Supplementary Figure: Reddit Per-Seed Breakdown (Seeds 42, 43, 44)."""
    csv_file = data_dir / "consolidated_experiments.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = [r for r in csv.DictReader(f) if r["dataset"] == "Reddit" and r["suite"] == "controlled_ablation"]

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0), sharey=True)
    plt.subplots_adjust(wspace=0.18)
    seeds = [42, 43, 44]
    variants = [
        ("etdfgl_full", "Full ETD-FGL", PALETTE["ETD-FGL"]),
        ("etdfgl_fixed_no_update", "Fixed No Update", PALETTE["Fixed No Update"]),
        ("etdfgl_fixed_no_topology", "Fixed No Topology", PALETTE["Fixed No Topology"]),
    ]

    for idx, s in enumerate(seeds):
        ax = axes[idx]
        vals = []
        labels = []
        colors = []
        for slug, label, color in variants:
            m = next(r for r in records if int(r["seed"]) == s and r["output_slug"] == slug)
            vals.append(float(m["attack_success_rate"]))
            labels.append(label)
            colors.append(color)

        bars = ax.bar(range(len(labels)), vals, color=colors, edgecolor="black", linewidth=0.8)
        title_suffix = " [Vulnerable Seed]" if s == 43 else ""
        ax.set_title(f"Reddit: Seed {s}{title_suffix}", fontweight="bold", pad=8, color="#990000" if s == 43 else "black")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(["Full", "No Upd", "No Topo"], fontweight="semibold")
        if idx == 0:
            ax.set_ylabel("Attack Success Rate (ASR %)")
        ax.set_ylim(0, 85)
        ax.grid(True, axis="y", linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.1f}%", (bar.get_x() + bar.get_width()/2, h + 1.5), ha="center", fontsize=8.0, fontweight="bold")

    fig.suptitle("Supplementary Figure S1: Reddit Per-Seed Backdoor ASR across Controlled Variants",
                 fontweight="bold", fontsize=12.0, y=1.01)

    save_figure(fig, out_dir, "Fig_S_Reddit_Seed_Heterogeneity")


def generate_figure_s_standard_vs_controlled(data_dir: Path, out_dir: Path) -> None:
    """Supplementary Figure: Direct comparison of Standard vs Controlled Ablation."""
    std_csv = data_dir / "standard_ablation_summary.csv"
    with std_csv.open("r", encoding="utf-8") as f:
        std_rows = list(csv.DictReader(f))

    ctrl_csv = data_dir / "controlled_ablation_summary.csv"
    with ctrl_csv.open("r", encoding="utf-8") as f:
        ctrl_rows = list(csv.DictReader(f))

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    plt.subplots_adjust(wspace=0.22)
    x = np.arange(len(DATASET_ORDER))
    width = 0.22

    # Panel (a): Topology Channel (Fixed 9/13 vs Normalized 1.0 vs Full)
    ax_topo = axes[0]
    for i, (suite_label, src_rows, query_key, col) in enumerate([
        ("Fixed No Update ($c_{topo}=9/13$)", ctrl_rows, "ETD-FGL Fixed No Update (9/13 Topo)", PALETTE["Fixed No Update"]),
        ("Old No Update ($c_{topo}=1.0$)", std_rows, "ETD-FGL Topology-only", PALETTE["Old No Update"]),
        ("Full ETD-FGL ($c_{topo}=9/13, c_{upd}=4/13$)", ctrl_rows, "ETD-FGL (Full final)", PALETTE["ETD-FGL"]),
    ]):
        vals, errs = [], []
        for ds in DATASET_ORDER:
            m = next(r for r in src_rows if r["dataset"] == ds and (r.get("variant_name") == query_key or r.get("variant") == query_key))
            m_str, s_str = m["asr_display"].split(" ± ")
            vals.append(float(m_str))
            errs.append(float(s_str))
        offset = (i - 1) * width
        ax_topo.bar(x + offset, vals, width, yerr=errs, capsize=3.0, label=suite_label, color=col, edgecolor="black", linewidth=0.7)

    ax_topo.set_title("(a) Topology Channel: Fixed (9/13) vs Normalized (1.0)", fontweight="bold", pad=8)
    ax_topo.set_ylabel("Attack Success Rate (ASR %)")
    ax_topo.set_xticks(x)
    ax_topo.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_topo.set_ylim(0, 45)
    ax_topo.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_topo.spines["top"].set_visible(False)
    ax_topo.spines["right"].set_visible(False)
    ax_topo.legend(loc="upper left", frameon=True, edgecolor="#cccccc")

    # Panel (b): Update Channel (Fixed 4/13 vs Normalized 1.0 vs Full)
    ax_upd = axes[1]
    for i, (suite_label, src_rows, query_key, col) in enumerate([
        ("Fixed No Topology ($c_{upd}=4/13$)", ctrl_rows, "ETD-FGL Fixed No Topology (4/13 Update)", PALETTE["Fixed No Topology"]),
        ("Old No Topology ($c_{upd}=1.0$)", std_rows, "ETD-FGL Update-only", PALETTE["Old No Topology"]),
        ("Full ETD-FGL ($c_{topo}=9/13, c_{upd}=4/13$)", ctrl_rows, "ETD-FGL (Full final)", PALETTE["ETD-FGL"]),
    ]):
        vals, errs = [], []
        for ds in DATASET_ORDER:
            m = next(r for r in src_rows if r["dataset"] == ds and (r.get("variant_name") == query_key or r.get("variant") == query_key))
            m_str, s_str = m["asr_display"].split(" ± ")
            vals.append(float(m_str))
            errs.append(float(s_str))
        offset = (i - 1) * width
        ax_upd.bar(x + offset, vals, width, yerr=errs, capsize=3.0, label=suite_label, color=col, edgecolor="black", linewidth=0.7)

    ax_upd.set_title("(b) Update Channel: Fixed (4/13) vs Normalized (1.0)", fontweight="bold", pad=8)
    ax_upd.set_ylabel("Attack Success Rate (ASR %)")
    ax_upd.set_xticks(x)
    ax_upd.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_upd.set_ylim(0, 80)
    ax_upd.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_upd.spines["top"].set_visible(False)
    ax_upd.spines["right"].set_visible(False)
    ax_upd.legend(loc="upper left", frameon=True, edgecolor="#cccccc")

    fig.suptitle("Supplementary Figure S2: Standard vs Controlled Ablation (Impact of Coefficient Normalization)",
                 fontweight="bold", fontsize=12.0, y=1.01)

    save_figure(fig, out_dir, "Fig_S_Standard_vs_Controlled_Comparison")


# ==============================================================================
# MAIN EXECUTION DISPATCHER
# ==============================================================================

def main() -> None:
    project_dir = Path(__file__).resolve().parent
    data_dir = project_dir / "paper_artifacts" / "ETDFGL_Publication_Results_v1" / "consolidated_data"
    out_dir = project_dir / "paper_artifacts" / "ETDFGL_Figure_Revision_v2" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================================")
    print("ETD-FGL Scientific Figure Redesign Suite (Revision v2)")
    print(f"Target Output Directory: {out_dir}")
    print("==================================================================")

    # 1. Figure A: Baseline Comparisons (Overview + per-dataset 2x2)
    print("\n[1/9] Generating Figure A: Baseline Comparisons...")
    generate_figure_a_overview(data_dir, out_dir)
    generate_figure_a_per_dataset(data_dir, out_dir, "Cora", "1")
    generate_figure_a_per_dataset(data_dir, out_dir, "PubMed", "2")
    generate_figure_a_per_dataset(data_dir, out_dir, "Reddit", "3")

    # 2. Figure B: Standard Ablation (All 6 variants, 3 datasets, 3 seeds)
    print("\n[2/9] Generating Figure B: Standard Ablation (6 Variants)...")
    generate_figure_b_standard_ablation(data_dir, out_dir)

    # 3. Figure C: Controlled Ablation (Fixed coefficients, paired deltas)
    print("\n[3/9] Generating Figure C: Controlled Scientific Ablation...")
    generate_figure_c_controlled_ablation(data_dir, out_dir)

    # 4. Figure D: Multi-Seed Robustness (With Reddit Seed 43 Callout)
    print("\n[4/9] Generating Figure D: Multi-Seed Performance...")
    generate_figure_d_multiseed_robustness(data_dir, out_dir)

    # 5. Figure E: Federated Learning Dynamics (50 communication rounds)
    print("\n[5/9] Generating Figure E: Learning Dynamics...")
    generate_figure_e_learning_dynamics(project_dir, out_dir)

    # 6. Figure F: Trust and Defense Mechanisms (Risk dynamics, 5-client normalization)
    print("\n[6/9] Generating Figure F: Trust and Defense Mechanisms...")
    generate_figure_f_trust_defense(project_dir, out_dir)

    # 7. Figure G: Trigger Attack Effect and Relative Defense Improvements
    print("\n[7/9] Generating Figure G: Attack Effect and Defense Gain...")
    generate_figure_g_attack_effect_gain(data_dir, out_dir)

    # 8. Figure H: Accuracy-ASR Trade-Off (Dataset-separated panels)
    print("\n[8/9] Generating Figure H: Accuracy-Robustness Trade-Off...")
    generate_figure_h_tradeoff(data_dir, out_dir)

    # 9. Figure I: Training Runtime Comparison (FedTGE clipping fixed)
    print("\n[9/9] Generating Figure I: Training Runtime Comparison (Fixed FedTGE)...")
    generate_figure_i_runtime(data_dir, out_dir)

    # Supplementary Figures
    print("\n[Supp] Generating Supplementary Figures...")
    generate_figure_s_reddit_seeds(data_dir, out_dir)
    generate_figure_s_standard_vs_controlled(data_dir, out_dir)

    print("\n==================================================================")
    print("[ALL COMPLETE] 14 publication-grade figures generated at 600 DPI PNG!")
    print("==================================================================")


if __name__ == "__main__":
    main()
