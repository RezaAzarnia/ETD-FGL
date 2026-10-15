#!/usr/bin/env python3
"""ETD-FGL Publication-Quality Scientific Figures Generator.

Generates the complete suite of main and supplementary publication figures
for international journal submission (IEEE, Elsevier, Springer standards):
- Vector formats (PDF, SVG) + 600 DPI raster (PNG)
- Consistent, colorblind-safe academic palette
- Mathematically accurate labels and annotations
- Clear separation between single-seed baselines and multi-seed evaluations
- Negative values displayed cleanly with explicit zero reference lines
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Publication-grade academic typography and geometry
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
    "savefig.pad_inches": 0.05,
    "mathtext.fontset": "stix",
})

# Colorblind-safe, academically restrained color palette
PALETTE = {
    "Clean FedAvg": "#2c7bb6",       # Academic blue
    "Attacked FedAvg": "#d7191c",    # Vermilion red
    "PD-FL": "#1b9e77",              # Emerald green
    "GSP-FL": "#7570b3",             # Slate purple
    "FLPurifier-GNN": "#e7298a",     # Magenta rose
    "DMGNN-FL": "#d95f02",           # Amber brown
    "FedTGE": "#fdae61",             # Ochre / soft orange
    "ETD-FGL": "#202020",            # Pitch / dark charcoal
    "ETD-FGL (Full)": "#202020",
    "ETD-FGL (Full final)": "#202020",
    "Fixed No Update": "#2b83ba",    # Steel blue
    "Fixed No Topology": "#e66101",  # Deep orange
    "Old No Update": "#80b1d3",      # Muted light blue
    "Old No Topology": "#fdb462",    # Muted light orange
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


def save_publication_figure(fig, target_dir: Path, stem: str, caption: str) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_dir / f"{stem}.png", dpi=600)
    fig.savefig(target_dir / f"{stem}.pdf")
    fig.savefig(target_dir / f"{stem}.svg")
    (target_dir / f"{stem}_caption.txt").write_text(caption.strip() + "\n", encoding="utf-8")
    plt.close(fig)
    print(f"  Saved figure: {target_dir / stem} (.png, .pdf, .svg)")


# ==============================================================================
# MAIN FIGURES
# ==============================================================================

def generate_figure_1_overall_baselines(data_dir: Path, out_dir: Path) -> None:
    """Figure 1: Overall Performance Comparison across Cora, PubMed, and Reddit."""
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

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=False)
    x = np.arange(len(DATASET_ORDER))
    width = 0.10

    # Panel A: Clean Accuracy
    ax_acc = axes[0]
    for i, m_name in enumerate(methods_order):
        vals = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["method_name"] == m_name), None)
            vals.append(float(match["clean_test_accuracy"]) if match and match["clean_test_accuracy"] != "" else 0.0)

        offset = (i - len(methods_order) / 2 + 0.5) * width
        rects = ax_acc.bar(
            x + offset,
            vals,
            width,
            label=m_name,
            color=PALETTE.get(m_name, "#555555"),
            edgecolor="black",
            linewidth=0.6,
        )

    ax_acc.set_title("(a) Clean Test Accuracy", fontweight="bold", pad=8)
    ax_acc.set_ylabel("Clean Accuracy (%)")
    ax_acc.set_xticks(x)
    ax_acc.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_acc.set_ylim(0, 100)
    ax_acc.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_acc.spines["top"].set_visible(False)
    ax_acc.spines["right"].set_visible(False)

    # Panel B: Attack Success Rate (ASR)
    ax_asr = axes[1]
    # Clean FedAvg has no ASR by definition (unattacked)
    attacked_methods = [m for m in methods_order if m != "Clean FedAvg"]
    width_asr = 0.11

    for i, m_name in enumerate(attacked_methods):
        vals = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["method_name"] == m_name), None)
            vals.append(float(match["attack_success_rate"]) if match and match["attack_success_rate"] != "" else 0.0)

        offset = (i - len(attacked_methods) / 2 + 0.5) * width_asr
        ax_asr.bar(
            x + offset,
            vals,
            width_asr,
            label=m_name,
            color=PALETTE.get(m_name, "#555555"),
            edgecolor="black",
            linewidth=0.6,
        )

    ax_asr.set_title("(b) Backdoor Attack Success Rate (ASR)", fontweight="bold", pad=8)
    ax_asr.set_ylabel("Attack Success Rate (ASR %)")
    ax_asr.set_xticks(x)
    ax_asr.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_asr.set_ylim(0, 100)
    ax_asr.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_asr.spines["top"].set_visible(False)
    ax_asr.spines["right"].set_visible(False)

    # Unified Legend
    handles, labels = ax_acc.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.08),
        ncol=4,
        frameon=True,
        edgecolor="#cccccc",
    )

    caption = (
        "Figure 1: Overall performance comparison across Cora, PubMed, and Reddit benchmark datasets (evaluated on Seed 42). "
        "(a) Clean test accuracy across all eight methods, demonstrating that ETD-FGL preserves baseline classification accuracy. "
        "(b) Backdoor Attack Success Rate (ASR) under structural clique attacks; lower is better. "
        "ETD-FGL consistently suppresses backdoor penetration below 5% on Cora and 1% on PubMed."
    )
    save_publication_figure(fig, out_dir, "Fig_01_Overall_Performance_Baselines", caption)


def generate_figure_2_multiseed_robustness(data_dir: Path, out_dir: Path) -> None:
    """Figure 2: Multi-Seed Robustness: Attacked FedAvg vs ETD-FGL across Seeds 42, 43, 44."""
    csv_file = data_dir / "consolidated_experiments.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = [r for r in csv.DictReader(f) if r["suite"] == "multiseed"]

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    x = np.arange(len(DATASET_ORDER))
    width = 0.28

    for p_idx, (metric_key, title, ylabel) in enumerate([
        ("clean_test_accuracy", "(a) Clean Accuracy (Seeds 42, 43, 44)", "Clean Accuracy (%)"),
        ("attack_success_rate", "(b) Attack Success Rate (Seeds 42, 43, 44)", "Attack Success Rate (ASR %)"),
    ]):
        ax = axes[p_idx]
        for m_idx, (m_name, color, offset) in enumerate([
            ("Attacked FedAvg", PALETTE["Attacked FedAvg"], -width / 2),
            ("ETD-FGL", PALETTE["ETD-FGL"], width / 2),
        ]):
            means = []
            stds = []
            for ds_idx, ds in enumerate(DATASET_ORDER):
                runs = [r for r in records if r["dataset"] == ds and r["method_name"] == m_name]
                vals = [float(r[metric_key]) for r in runs if r[metric_key] != ""]
                m_val = float(np.mean(vals))
                s_val = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
                means.append(m_val)
                stds.append(s_val)

                # Overlay individual seed points (jittered)
                seed_x = x[ds_idx] + offset + np.array([-0.04, 0.0, 0.04])
                for pt_idx, r in enumerate(runs):
                    v = float(r[metric_key])
                    s = int(r["seed"])
                    # Highlight Reddit Seed 43 specifically
                    if ds == "Reddit" and s == 43 and m_name == "ETD-FGL" and metric_key == "attack_success_rate":
                        ax.scatter(
                            seed_x[pt_idx], v,
                            color="#b2182b",
                            s=55,
                            edgecolors="black",
                            linewidth=1.2,
                            zorder=5,
                            marker="^",
                            label="Reddit Seed 43" if m_idx == 0 and p_idx == 1 else None,
                        )
                        ax.annotate(
                            "Seed 43\n(34.8%)",
                            (seed_x[pt_idx], v),
                            xytext=(seed_x[pt_idx] + 0.08, v + 4),
                            fontsize=7.5,
                            fontweight="bold",
                            arrowprops=dict(arrowstyle="->", color="black", lw=0.7),
                        )
                    else:
                        ax.scatter(
                            seed_x[pt_idx], v,
                            color="white",
                            s=26,
                            edgecolors=color,
                            linewidth=1.0,
                            zorder=4,
                        )

            ax.bar(
                x + offset,
                means,
                width,
                yerr=stds,
                capsize=3.5,
                error_kw=dict(lw=0.9, capthick=0.9),
                label=m_name if p_idx == 0 else None,
                color=color,
                alpha=0.78,
                edgecolor="black",
                linewidth=0.8,
            )

        ax.set_title(title, fontweight="bold", pad=8)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(DATASET_ORDER, fontweight="semibold")
        ax.set_ylim(0, 100)
        ax.grid(True, axis="y", linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].legend(loc="lower left", frameon=True, edgecolor="#cccccc")

    caption = (
        "Figure 2: Multi-seed robustness evaluation comparing Attacked FedAvg against ETD-FGL across three random seeds (42, 43, 44). "
        "Bars indicate sample means; error bars denote sample standard deviations (ddof=1); overlaid circular markers show individual seed outcomes. "
        "(a) Clean classification accuracy is fully preserved across all random seeds. "
        "(b) Backdoor Attack Success Rate (ASR) is dramatically suppressed by ETD-FGL. "
        "Reddit Seed 43 is explicitly highlighted (annotated triangular marker) reflecting elevated backdoor vulnerability under high graph heterogeneity."
    )
    save_publication_figure(fig, out_dir, "Fig_02_MultiSeed_Robustness", caption)


def generate_figure_3_pareto_tradeoff(data_dir: Path, out_dir: Path) -> None:
    """Figure 3: Clean Accuracy vs Robustness (ASR) Trade-Off Pareto Plot."""
    b_csv = data_dir / "baseline_seed42.csv"
    with b_csv.open("r", encoding="utf-8") as f:
        b_records = list(csv.DictReader(f))

    ms_csv = data_dir / "multiseed_summary.csv"
    with ms_csv.open("r", encoding="utf-8") as f:
        ms_records = list(csv.DictReader(f))

    fig, ax = plt.subplots(figsize=(7.5, 5.0))

    # Plot single-seed baselines (Seed 42)
    for r in b_records:
        m = r["method_name"]
        if m == "Clean FedAvg" or r["attack_success_rate"] == "":
            continue
        acc = float(r["clean_test_accuracy"])
        asr = float(r["attack_success_rate"])
        ds = r["dataset"]

        ax.scatter(
            acc,
            asr,
            color=PALETTE.get(m, "#555555"),
            marker=METHOD_MARKERS.get(m, "o"),
            s=48,
            alpha=0.65,
            edgecolors="black",
            linewidth=0.6,
        )

    # Plot Multi-seed Centroids for ETD-FGL and Attacked FedAvg with Error Bars
    for r in ms_records:
        m = r["method"]
        if r["asr_mean"] == "":
            continue
        acc_m = float(r["clean_accuracy_mean"])
        acc_s = float(r["clean_accuracy_std"])
        asr_m = float(r["asr_mean"])
        asr_s = float(r["asr_std"])
        ds = r["dataset"]

        color = PALETTE.get(m, "#222222")
        marker = METHOD_MARKERS.get(m, "*")
        size = 110 if m == "ETD-FGL" else 75

        ax.errorbar(
            acc_m,
            asr_m,
            xerr=acc_s,
            yerr=asr_s,
            fmt=marker,
            color=color,
            ecolor=color,
            elinewidth=1.2,
            capsize=3.0,
            markersize=9 if m == "ETD-FGL" else 7,
            markeredgecolor="black",
            markeredgewidth=0.8,
            zorder=6,
        )
        ax.annotate(
            f"{m}\n({ds})",
            (acc_m, asr_m),
            xytext=(acc_m + 0.6, asr_m + 1.8),
            fontsize=7.8,
            fontweight="bold" if m == "ETD-FGL" else "normal",
        )

    # Ideal Frontier annotation
    ax.annotate(
        "Optimal Defense Region\n(High Accuracy, Near-Zero ASR)",
        xy=(84.5, 1.0),
        xytext=(72.0, 12.0),
        fontsize=8.5,
        fontstyle="italic",
        color="#006600",
        arrowprops=dict(arrowstyle="->", color="#006600", lw=1.0),
    )

    ax.set_title("Accuracy versus Robustness Trade-off (All Datasets)", fontweight="bold", pad=10)
    ax.set_xlabel("Clean Test Accuracy (%)  [Higher is better $\\rightarrow$]")
    ax.set_ylabel("Attack Success Rate (ASR %)  [Lower is better $\\leftarrow$]")
    ax.set_xlim(70, 90)
    ax.set_ylim(-2, 75)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    caption = (
        "Figure 3: Clean accuracy versus backdoor robustness trade-off across Cora, PubMed, and Reddit. "
        "Small semi-transparent markers represent individual baseline models evaluated on Seed 42. "
        "Prominent markers with cross-whiskers represent multi-seed distributions (mean ± standard deviation across seeds 42, 43, 44) "
        "for Attacked FedAvg (red X) and ETD-FGL (black star). "
        "ETD-FGL shifts the operating point into the optimal low-ASR, high-accuracy regime."
    )
    save_publication_figure(fig, out_dir, "Fig_03_Accuracy_Robustness_Tradeoff", caption)


def generate_figure_4_controlled_ablation(data_dir: Path, out_dir: Path) -> None:
    """Figure 4: Controlled Scientific Ablation: Fixed Coefficients and Paired Effects."""
    csv_file = data_dir / "controlled_ablation_summary.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    paired_csv = data_dir / "paired_differences.csv"
    with paired_csv.open("r", encoding="utf-8") as f:
        paired_records = list(csv.DictReader(f))

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    x = np.arange(len(DATASET_ORDER))
    width = 0.22

    # Panel A: ASR under Controlled Ablation
    ax_a = axes[0]
    variants = [
        ("etdfgl_full", "Full ETD-FGL (9/13 Topo + 4/13 Upd)", PALETTE["ETD-FGL"], -width),
        ("etdfgl_fixed_no_update", "Fixed No Update (9/13 Topo)", PALETTE["Fixed No Update"], 0.0),
        ("etdfgl_fixed_no_topology", "Fixed No Topology (4/13 Upd)", PALETTE["Fixed No Topology"], width),
    ]

    for slug, label, color, offset in variants:
        asrs = []
        errs = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["variant_slug"] == slug), None)
            if match and match["asr_display"] != "N/A":
                mean_str, std_str = match["asr_display"].split(" ± ")
                asrs.append(float(mean_str))
                errs.append(float(std_str))
            else:
                asrs.append(0.0)
                errs.append(0.0)

        ax_a.bar(
            x + offset,
            asrs,
            width,
            yerr=errs,
            capsize=3.0,
            label=label,
            color=color,
            edgecolor="black",
            linewidth=0.7,
        )

    ax_a.set_title("(a) Backdoor ASR across Controlled Variants", fontweight="bold", pad=8)
    ax_a.set_ylabel("Attack Success Rate (ASR %)")
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_a.set_ylim(0, 100)
    ax_a.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_a.spines["top"].set_visible(False)
    ax_a.spines["right"].set_visible(False)
    ax_a.legend(loc="upper left", frameon=True, edgecolor="#cccccc")

    # Panel B: Paired ASR Difference (Delta = Variant - Full)
    ax_b = axes[1]
    p_variants = [
        ("etdfgl_fixed_no_update", "Δ No Update (vs Full)", PALETTE["Fixed No Update"], -width / 2),
        ("etdfgl_fixed_no_topology", "Δ No Topology (vs Full)", PALETTE["Fixed No Topology"], width / 2),
    ]

    for slug, label, color, offset in p_variants:
        d_asrs = []
        d_errs = []
        for ds in DATASET_ORDER:
            match = next((r for r in paired_records if r["dataset"] == ds and r["variant_slug"] == slug), None)
            if match and match["delta_asr"] != "N/A":
                mean_str, std_str = match["delta_asr"].split(" ± ")
                d_asrs.append(float(mean_str))
                d_errs.append(float(std_str))
            else:
                d_asrs.append(0.0)
                d_errs.append(0.0)

        ax_b.bar(
            x + offset,
            d_asrs,
            width,
            yerr=d_errs,
            capsize=3.0,
            label=label,
            color=color,
            edgecolor="black",
            linewidth=0.7,
        )

    ax_b.axhline(0, color="black", linestyle="-", linewidth=0.8)
    ax_b.set_title("(b) Paired ASR Degradation (Δ = Variant − Full)", fontweight="bold", pad=8)
    ax_b.set_ylabel("Δ ASR (% points)  [Higher = Worse defense]")
    ax_b.set_xticks(x)
    ax_b.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_b.set_ylim(-5, 75)
    ax_b.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)
    ax_b.legend(loc="upper left", frameon=True, edgecolor="#cccccc")

    caption = (
        "Figure 4: Controlled scientific ablation isolating evidence channels with held-constant coefficients. "
        "(a) Backdoor ASR for Full ETD-FGL (9/13 topology + 4/13 update), Fixed No Update (9/13 topology), and Fixed No Topology (4/13 update). "
        "(b) Paired difference (Δ = Variant - Full ETD-FGL) computed per seed across seeds 42, 43, 44. "
        "Removing topology causes catastrophic defense failure (+37.3% on Cora, +52.2% on Reddit), "
        "while removing the model-update channel causes a statistically significant increase in backdoor penetration (+11.1% on Reddit)."
    )
    save_publication_figure(fig, out_dir, "Fig_04_Controlled_Ablation", caption)


def generate_figure_5_learning_dynamics(project_dir: Path, out_dir: Path) -> None:
    """Figure 5: Learning Dynamics over 50 Communication Rounds across Datasets."""
    fig, axes = plt.subplots(2, 3, figsize=(11.5, 6.0), sharex=True)

    methods = [
        ("Clean FedAvg", "fedavg_clean"),
        ("Attacked FedAvg", "fedavg_structural_backdoor"),
        ("FedTGE", "baseline_fedtge"),
        ("ETD-FGL", "defended_etdfgl"),
    ]

    for col_idx, ds in enumerate(["cora", "pubmed", "reddit"]):
        ds_display = DISPLAY_DATASETS[ds]
        base_dir = project_dir / "outputs" / "final_multidataset" / f"federated_{ds}"

        # Row 0: Clean Test Accuracy
        ax_acc = axes[0, col_idx]
        # Row 1: ASR
        ax_asr = axes[1, col_idx]

        for m_name, slug in methods:
            hist_path = base_dir / slug / "training_history.csv"
            if not hist_path.is_file():
                continue
            with hist_path.open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

            rounds = [int(r["round"]) for r in rows]
            accs = [float(r["test_accuracy"]) * 100.0 for r in rows]
            asrs = [
                float(r["attack_success_rate"]) * 100.0 if r.get("attack_success_rate", "") != "" else 0.0
                for r in rows
            ]

            color = PALETTE.get(m_name, "#333333")
            ls = METHOD_STYLES.get(m_name, "-")
            marker = METHOD_MARKERS.get(m_name, "o")

            ax_acc.plot(
                rounds,
                accs,
                label=m_name if col_idx == 0 else None,
                color=color,
                linestyle=ls,
                marker=marker,
                markevery=5,
                markersize=4.0,
            )

            if m_name != "Clean FedAvg":
                ax_asr.plot(
                    rounds,
                    asrs,
                    label=m_name if col_idx == 0 else None,
                    color=color,
                    linestyle=ls,
                    marker=marker,
                    markevery=5,
                    markersize=4.0,
                )

        ax_acc.set_title(f"{ds_display}: Clean Accuracy", fontweight="bold", pad=6)
        ax_acc.set_ylabel("Accuracy (%)" if col_idx == 0 else "")
        ax_acc.set_ylim(0, 100)
        ax_acc.grid(True, linestyle="--", alpha=0.3)
        ax_acc.spines["top"].set_visible(False)
        ax_acc.spines["right"].set_visible(False)

        ax_asr.set_title(f"{ds_display}: Backdoor ASR", fontweight="bold", pad=6)
        ax_asr.set_xlabel("Communication Round")
        ax_asr.set_ylabel("ASR (%)" if col_idx == 0 else "")
        ax_asr.set_ylim(-2, 100)
        ax_asr.grid(True, linestyle="--", alpha=0.3)
        ax_asr.spines["top"].set_visible(False)
        ax_asr.spines["right"].set_visible(False)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=4,
        frameon=True,
        edgecolor="#cccccc",
    )

    caption = (
        "Figure 5: Federated learning dynamics over 50 communication rounds on Cora, PubMed, and Reddit (Seed 42). "
        "Top row: Clean test accuracy convergence. "
        "Bottom row: Backdoor Attack Success Rate (ASR). "
        "While unmitigated Attacked FedAvg converges rapidly to high ASR (60–80%), "
        "ETD-FGL suppresses backdoor injection from early communication rounds without retarding clean convergence."
    )
    save_publication_figure(fig, out_dir, "Fig_05_Learning_Dynamics_Rounds", caption)


def generate_figure_6_attacker_weight_dynamics(project_dir: Path, out_dir: Path) -> None:
    """Figure 6: Attacker Aggregation Weight Suppression over Rounds in Controlled Ablation."""
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.8), sharey=True)

    ctrl_variants = [
        ("etdfgl_full", "Full ETD-FGL", PALETTE["ETD-FGL"], "-"),
        ("etdfgl_fixed_no_update", "Fixed No Update", PALETTE["Fixed No Update"], "--"),
        ("etdfgl_fixed_no_topology", "Fixed No Topology", PALETTE["Fixed No Topology"], ":"),
    ]

    for col_idx, ds in enumerate(["cora", "pubmed", "reddit"]):
        ax = axes[col_idx]
        ds_display = DISPLAY_DATASETS[ds]
        # Use Seed 42 for representative history curves
        base_dir = project_dir / "outputs" / "extended_experiments" / "controlled_ablation_v1" / ds / "seed_42"

        for slug, label, color, ls in ctrl_variants:
            hist_path = base_dir / slug / "training_history.csv"
            if not hist_path.is_file():
                continue
            with hist_path.open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

            rounds = [int(r["round"]) for r in rows]
            weights = [float(r["etdfgl_weight_client_0"]) * 100.0 for r in rows]

            ax.plot(
                rounds,
                weights,
                label=label if col_idx == 0 else None,
                color=color,
                linestyle=ls,
                linewidth=1.6,
            )

        # Baseline uniform weight line (20% for 5 clients)
        ax.axhline(20.0, color="gray", linestyle="-.", linewidth=0.9, alpha=0.7, label="Uniform Weight (20%)" if col_idx == 0 else None)

        ax.set_title(f"{ds_display}", fontweight="bold", pad=8)
        ax.set_xlabel("Communication Round")
        if col_idx == 0:
            ax.set_ylabel("Attacker Aggregation Weight (%)")
        ax.set_ylim(0, 25)
        ax.grid(True, linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.08),
        ncol=4,
        frameon=True,
        edgecolor="#cccccc",
    )

    caption = (
        "Figure 6: Dynamic suppression of malicious client aggregation weight ($w_0$) across 50 communication rounds (Seed 42). "
        "Horizontal dot-dashed line represents the uniform baseline share ($1/K = 20\%$ for 5 clients). "
        "Full ETD-FGL and Fixed No Update rapidly penalize attacker trust, compressing aggregation weight to $\\le 4.7\\%$. "
        "Without the topology channel (Fixed No Topology), attacker weight remains elevated at $13–19\\%$, permitting backdoor infiltration."
    )
    save_publication_figure(fig, out_dir, "Fig_06_Attacker_Weight_Dynamics", caption)


# ==============================================================================
# SUPPLEMENTARY FIGURES
# ==============================================================================

def generate_figure_s1_standard_vs_controlled(data_dir: Path, out_dir: Path) -> None:
    """Figure S1: Standard vs Controlled Ablation (Impact of Coefficient Shift)."""
    std_csv = data_dir / "standard_ablation_summary.csv"
    with std_csv.open("r", encoding="utf-8") as f:
        std_rows = list(csv.DictReader(f))

    ctrl_csv = data_dir / "controlled_ablation_summary.csv"
    with ctrl_csv.open("r", encoding="utf-8") as f:
        ctrl_rows = list(csv.DictReader(f))

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    x = np.arange(len(DATASET_ORDER))
    width = 0.18

    # Panel A: Topology Channel Comparison
    ax_topo = axes[0]
    for i, (suite_label, src_rows, query_key, col) in enumerate([
        ("Fixed No Update ($c_{topo}=9/13$)", ctrl_rows, "ETD-FGL Fixed No Update (9/13 Topo)", PALETTE["Fixed No Update"]),
        ("Old No Update ($c_{topo}=1.0$)", std_rows, "ETD-FGL Topology-only", PALETTE["Old No Update"]),
        ("Full ETD-FGL ($c_{topo}=9/13, c_{upd}=4/13$)", ctrl_rows, "ETD-FGL (Full final)", PALETTE["ETD-FGL"]),
    ]):
        vals, errs = [], []
        for ds in DATASET_ORDER:
            match = next((r for r in src_rows if r["dataset"] == ds and (r.get("variant_name") == query_key or r.get("variant") == query_key)), None)
            if match and match["asr_display"] != "N/A":
                m_str, s_str = match["asr_display"].split(" ± ")
                vals.append(float(m_str))
                errs.append(float(s_str))
            else:
                vals.append(0.0)
                errs.append(0.0)

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

    # Panel B: Update Channel Comparison
    ax_upd = axes[1]
    for i, (suite_label, src_rows, query_key, col) in enumerate([
        ("Fixed No Topology ($c_{upd}=4/13$)", ctrl_rows, "ETD-FGL Fixed No Topology (4/13 Update)", PALETTE["Fixed No Topology"]),
        ("Old No Topology ($c_{upd}=1.0$)", std_rows, "ETD-FGL Update-only", PALETTE["Old No Topology"]),
        ("Full ETD-FGL ($c_{topo}=9/13, c_{upd}=4/13$)", ctrl_rows, "ETD-FGL (Full final)", PALETTE["ETD-FGL"]),
    ]):
        vals, errs = [], []
        for ds in DATASET_ORDER:
            match = next((r for r in src_rows if r["dataset"] == ds and (r.get("variant_name") == query_key or r.get("variant") == query_key)), None)
            if match and match["asr_display"] != "N/A":
                m_str, s_str = match["asr_display"].split(" ± ")
                vals.append(float(m_str))
                errs.append(float(s_str))
            else:
                vals.append(0.0)
                errs.append(0.0)

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

    caption = (
        "Figure S1: Comparison between standard ablation (where ablated channel weights were normalized to 1.0) "
        "and controlled ablation (where coefficients were held constant at 9/13 and 4/13). "
        "(a) In Old No Update, inflating the topology coefficient from 9/13 to 1.0 (+44%) artificially strengthened trust suppression, "
        "yielding slightly lower ASR than Full ETD-FGL. The controlled comparison isolates channel removal under held-constant penalty. "
        "(b) In Update-only, holding the coefficient at 4/13 reveals that update anomaly alone is insufficient to prevent backdoor infiltration."
    )
    save_publication_figure(fig, out_dir, "Fig_S01_Standard_vs_Controlled_Ablation", caption)


def generate_figure_s2_attack_effect(data_dir: Path, out_dir: Path) -> None:
    """Figure S2: Trigger Attack Effect across All Datasets with Zero Reference Line."""
    csv_file = data_dir / "baseline_seed42.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    attacked_methods = [
        "Attacked FedAvg",
        "PD-FL",
        "GSP-FL",
        "FLPurifier-GNN",
        "DMGNN-FL",
        "FedTGE",
        "ETD-FGL",
    ]

    fig, ax = plt.subplots(figsize=(10.0, 4.4))
    x = np.arange(len(DATASET_ORDER))
    width = 0.11

    for i, m_name in enumerate(attacked_methods):
        vals = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["method_name"] == m_name), None)
            vals.append(float(match["attack_effect"]) if match and match["attack_effect"] != "" else 0.0)

        offset = (i - len(attacked_methods) / 2 + 0.5) * width
        ax.bar(
            x + offset,
            vals,
            width,
            label=m_name,
            color=PALETTE.get(m_name, "#555555"),
            edgecolor="black",
            linewidth=0.6,
        )

    # Prominent zero reference line
    ax.axhline(0.0, color="black", linestyle="-", linewidth=1.1, zorder=5)

    ax.set_title("Trigger Attack Effect (ASR − Clean Target Rate) [Seed 42]", fontweight="bold", pad=10)
    ax.set_ylabel("Attack Effect (% points)")
    ax.set_xticks(x)
    ax.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax.set_ylim(-15, 80)
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        ncol=4,
        frameon=True,
        edgecolor="#cccccc",
    )

    caption = (
        "Figure S2: Trigger Attack Effect (defined as ASR minus clean target class classification rate) across Cora, PubMed, and Reddit (Seed 42). "
        "The solid zero line indicates null trigger influence. Negative values demonstrate that target-class prediction on triggered test nodes "
        "is no higher (and often lower) than on clean nodes, proving that ETD-FGL completely neutralizes backdoor trigger activation."
    )
    save_publication_figure(fig, out_dir, "Fig_S02_Attack_Effect_All_Methods", caption)


def generate_figure_s3_runtime(data_dir: Path, out_dir: Path) -> None:
    """Figure S3: Timed Training-Loop Runtime Comparison (Explicitly Labeled)."""
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

    fig, ax = plt.subplots(figsize=(10.0, 4.4))
    x = np.arange(len(DATASET_ORDER))
    width = 0.10

    for i, m_name in enumerate(methods_order):
        vals = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["method_name"] == m_name), None)
            vals.append(float(match["elapsed_seconds"]) if match and match["elapsed_seconds"] != "" else 0.0)

        offset = (i - len(methods_order) / 2 + 0.5) * width
        ax.bar(
            x + offset,
            vals,
            width,
            label=m_name,
            color=PALETTE.get(m_name, "#555555"),
            edgecolor="black",
            linewidth=0.6,
        )

    ax.set_title("Federated Training Loop Runtime (50 Rounds, GPU Accelerated)", fontweight="bold", pad=10)
    ax.set_ylabel("Elapsed Time (seconds) [Training Loop]")
    ax.set_xticks(x)
    ax.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax.set_ylim(0, 110)
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        ncol=4,
        frameon=True,
        edgecolor="#cccccc",
    )

    caption = (
        "Figure S3: Timed 50-round federated training loop runtime across benchmark datasets (Seed 42). "
        "Important measurement note: Timings reflect the active federated training and aggregation loop on identical hardware; "
        "they do not measure initial client graph partitioning or offline descriptor precomputation. "
        "ETD-FGL adds minimal aggregation overhead relative to standard FedAvg."
    )
    save_publication_figure(fig, out_dir, "Fig_S03_Training_Runtime_Comparison", caption)


def generate_figure_s4_reddit_seed_breakdown(data_dir: Path, out_dir: Path) -> None:
    """Figure S4: Deep Dive into Reddit Seed 43 vs Seeds 42 and 44."""
    csv_file = data_dir / "consolidated_experiments.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = [r for r in csv.DictReader(f) if r["dataset"] == "Reddit" and r["suite"] == "controlled_ablation"]

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.8), sharey=True)
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
            match = next((r for r in records if int(r["seed"]) == s and r["output_slug"] == slug), None)
            vals.append(float(match["attack_success_rate"]) if match else 0.0)
            labels.append(label)
            colors.append(color)

        bars = ax.bar(
            range(len(labels)),
            vals,
            color=colors,
            edgecolor="black",
            linewidth=0.8,
        )

        # Highlight Seed 43 title
        title_suffix = " [Outlier Seed]" if s == 43 else ""
        ax.set_title(f"Reddit: Seed {s}{title_suffix}", fontweight="bold", pad=8, color="#990000" if s == 43 else "black")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(["Full", "No Upd", "No Topo"], fontweight="semibold")
        if idx == 0:
            ax.set_ylabel("Attack Success Rate (ASR %)")
        ax.set_ylim(0, 80)
        ax.grid(True, axis="y", linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Value annotations above bars
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.1f}%", (bar.get_x() + bar.get_width() / 2, h + 1.5), ha="center", fontsize=8.0)

    caption = (
        "Figure S4: Per-seed breakdown of Backdoor ASR on Reddit across controlled ablation variants (Seeds 42, 43, 44). "
        "Seed 43 acts as an outlier where ASR reaches 34.82% under Full ETD-FGL, rising to 43.52% without the update channel, "
        "and 70.59% without the topology channel. "
        "This highlights Reddit's structural heterogeneity and the essential role of dual-channel defense under difficult partitions."
    )
    save_publication_figure(fig, out_dir, "Fig_S04_Reddit_Seed_Heterogeneity_Analysis", caption)


def generate_figure_s5_benign_client_trust(data_dir: Path, out_dir: Path) -> None:
    """Figure S5: Benign Client Trust and Risk Preservation across Controlled Variants."""
    csv_file = data_dir / "controlled_ablation_summary.csv"
    with csv_file.open("r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0))
    x = np.arange(len(DATASET_ORDER))
    width = 0.22

    # Panel A: Benign Client Fused Risk
    ax_risk = axes[0]
    variants = [
        ("etdfgl_full", "Full ETD-FGL", PALETTE["ETD-FGL"], -width),
        ("etdfgl_fixed_no_update", "Fixed No Update", PALETTE["Fixed No Update"], 0.0),
        ("etdfgl_fixed_no_topology", "Fixed No Topology", PALETTE["Fixed No Topology"], width),
    ]

    for slug, label, color, offset in variants:
        risks = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["variant_slug"] == slug), None)
            if match and match["benign_risk_display"] != "N/A":
                mean_str, _ = match["benign_risk_display"].split(" ± ")
                risks.append(float(mean_str))
            else:
                risks.append(0.0)

        ax_risk.bar(
            x + offset,
            risks,
            width,
            label=label,
            color=color,
            edgecolor="black",
            linewidth=0.7,
        )

    ax_risk.set_title("(a) Benign-Client Fused Risk (Mean)", fontweight="bold", pad=8)
    ax_risk.set_ylabel("Fused Risk $R$  [Lower = Higher trust]")
    ax_risk.set_xticks(x)
    ax_risk.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_risk.set_ylim(0, 0.08)
    ax_risk.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_risk.spines["top"].set_visible(False)
    ax_risk.spines["right"].set_visible(False)
    ax_risk.legend(loc="upper right", frameon=True, edgecolor="#cccccc")

    # Panel B: Attacker Aggregation Weight
    ax_wt = axes[1]
    for slug, label, color, offset in variants:
        wts = []
        for ds in DATASET_ORDER:
            match = next((r for r in records if r["dataset"] == ds and r["variant_slug"] == slug), None)
            if match and match["attacker_weight_display"] != "N/A":
                mean_str, _ = match["attacker_weight_display"].split(" ± ")
                wts.append(float(mean_str))
            else:
                wts.append(0.0)

        ax_wt.bar(
            x + offset,
            wts,
            width,
            label=label,
            color=color,
            edgecolor="black",
            linewidth=0.7,
        )

    ax_wt.axhline(20.0, color="gray", linestyle="-.", linewidth=0.9, alpha=0.7, label="Uniform Share (20%)")
    ax_wt.set_title("(b) Attacker Aggregation Weight (Mean)", fontweight="bold", pad=8)
    ax_wt.set_ylabel("Aggregation Weight (%)  [Lower is better]")
    ax_wt.set_xticks(x)
    ax_wt.set_xticklabels(DATASET_ORDER, fontweight="semibold")
    ax_wt.set_ylim(0, 25)
    ax_wt.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax_wt.spines["top"].set_visible(False)
    ax_wt.spines["right"].set_visible(False)
    ax_wt.legend(loc="upper right", frameon=True, edgecolor="#cccccc")

    caption = (
        "Figure S5: Benign client risk and attacker aggregation weight across controlled ablation variants. "
        "(a) In Fixed No Update, benign risk is 0.0000 because benign clients experience zero graph modifications. "
        "In Full ETD-FGL, benign risk remains very small (<0.06), preserving over 85% trust. "
        "(b) Attacker weight is compressed from the uniform 20% down to 2.5–4.8% by Full ETD-FGL, "
        "whereas removing topology allows the attacker to maintain 13–18% aggregation weight."
    )
    save_publication_figure(fig, out_dir, "Fig_S05_Benign_Client_Trust_Preservation", caption)


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    data_dir = project_dir / "paper_artifacts" / "ETDFGL_Publication_Results_v1" / "consolidated_data"
    fig_base = project_dir / "paper_artifacts" / "ETDFGL_Publication_Results_v1" / "figures"
    main_fig_dir = fig_base / "main"
    supp_fig_dir = fig_base / "supplementary"

    main_fig_dir.mkdir(parents=True, exist_ok=True)
    supp_fig_dir.mkdir(parents=True, exist_ok=True)

    print("Generating Main Publication Figures...")
    generate_figure_1_overall_baselines(data_dir, main_fig_dir)
    generate_figure_2_multiseed_robustness(data_dir, main_fig_dir)
    generate_figure_3_pareto_tradeoff(data_dir, main_fig_dir)
    generate_figure_4_controlled_ablation(data_dir, main_fig_dir)
    generate_figure_5_learning_dynamics(project_dir, main_fig_dir)
    generate_figure_6_attacker_weight_dynamics(project_dir, main_fig_dir)

    print("Generating Supplementary Publication Figures...")
    generate_figure_s1_standard_vs_controlled(data_dir, supp_fig_dir)
    generate_figure_s2_attack_effect(data_dir, supp_fig_dir)
    generate_figure_s3_runtime(data_dir, supp_fig_dir)
    generate_figure_s4_reddit_seed_breakdown(data_dir, supp_fig_dir)
    generate_figure_s5_benign_client_trust(data_dir, supp_fig_dir)

    print("All 11 publication figures generated successfully in PDF, SVG, and 600 DPI PNG!")


if __name__ == "__main__":
    main()
