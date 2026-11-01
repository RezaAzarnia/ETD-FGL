"""Re-render handoff figures 2-8 from RESULTS/*.csv (derived from raw outputs). No training.
python -I make_figures.py <results_dir> <figures_dir>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = Path(sys.argv[1]); F = Path(sys.argv[2])
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
                     "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
DS = ["Cora", "PubMed", "Reddit"]
M = ["Clean FedAvg", "Attacked FedAvg", "PD-FL", "GSP-FL", "FLPurifier-GNN", "DMGNN-FL", "FedTGE", "ETD-FGL"]
COL = dict(zip(M, ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#999999", "#E69F00", "#56B4E9", "#000000"]))
b = pd.read_csv(R / "R02_seed42_baselines_tab_seed42_baselines.csv")
ms = pd.read_csv(R / "R03a_multiseed_per_seed.csv")

# ---- Fig 2 overall baselines (seed 42)
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
w = .1
for k, (col, ttl, yl) in enumerate([("clean_accuracy_pct", "(a) Clean test accuracy, seed 42", "Clean accuracy (%)"), ("asr_pct", "(b) Backdoor ASR, seed 42", "ASR (%)")]):
    for i, m in enumerate(M):
        v = [b[(b.dataset == d) & (b.method == m)][col].iloc[0] for d in DS]
        ax[k].bar(np.arange(3) + (i - 3.5) * w, v, w, color=COL[m], label=m, edgecolor="k", linewidth=.3)
    ax[k].set_xticks(range(3)); ax[k].set_xticklabels(DS); ax[k].set_title(ttl); ax[k].set_ylabel(yl); ax[k].set_ylim(0, 100)
ax[0].legend(ncol=4, loc="lower center", bbox_to_anchor=(1.1, 1.12), frameon=False)
fig.tight_layout(); fig.savefig(F / "overall_baselines.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/overall_baselines_preview.png", dpi=130, bbox_inches="tight"); plt.close()

# ---- Fig 3 tradeoff (per dataset panel; no cross-dataset frontier)
fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.9))
mk = dict(zip(M, ["o", "X", "s", "^", "v", "D", "P", "*"]))
for j, d in enumerate(DS):
    for m in M:
        r = b[(b.dataset == d) & (b.method == m)].iloc[0]
        ax[j].scatter(r.clean_accuracy_pct, r.asr_pct, c=COL[m], marker=mk[m], s=70 if m != "ETD-FGL" else 130, edgecolor="k", linewidth=.4, alpha=.55, zorder=3, label=m + " (seed 42)")
    for m in ["Attacked FedAvg", "ETD-FGL"]:
        g = ms[(ms.dataset == d) & (ms.method == m)]
        ax[j].errorbar(g.clean_accuracy_pct.mean(), g.asr_pct.mean(), xerr=g.clean_accuracy_pct.std(ddof=1), yerr=g.asr_pct.std(ddof=1), fmt=mk[m], color=COL[m],
                       ms=11, mec="k", capsize=3, zorder=4, label=m + " (3-seed mean ± SD)")
    ax[j].set_title(d); ax[j].set_xlabel("Clean accuracy (%)  → higher is better"); ax[j].set_ylabel("ASR (%)  ↓ lower is better")
    ax[j].set_ylim(-5, 105)
h, l = ax[0].get_legend_handles_labels()
fig.legend(h, l, ncol=5, loc="lower center", bbox_to_anchor=(.5, -.2), frameon=False, fontsize=7)
fig.suptitle("Accuracy-ASR operating points per dataset (desirable region: lower-right; no cross-dataset frontier is claimed)", y=1.02, fontsize=10)
fig.tight_layout(); fig.savefig(F / "accuracy_robustness_tradeoff.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/accuracy_robustness_tradeoff_preview.png", dpi=130, bbox_inches="tight"); plt.close()

# ---- Fig 4 multiseed
fig, ax = plt.subplots(2, 3, figsize=(10.5, 5.6))
for j, d in enumerate(DS):
    for i, (col, yl) in enumerate([("clean_accuracy_pct", "Clean accuracy (%)"), ("asr_pct", "ASR (%)")]):
        for k, m in enumerate(["Attacked FedAvg", "ETD-FGL"]):
            g = ms[(ms.dataset == d) & (ms.method == m)].sort_values("seed")
            ax[i, j].bar(k, g[col].mean(), .55, yerr=g[col].std(ddof=1), capsize=4, color=COL[m], alpha=.35, edgecolor="k")
            ax[i, j].scatter(np.full(3, k) + np.array([-.15, 0, .15]), g[col], c=COL[m], edgecolor="k", zorder=3, s=28)
            if d == "Reddit" and col == "asr_pct" and m == "ETD-FGL":
                s43 = g[g.seed == 43][col].iloc[0]; ax[i, j].annotate(f"seed 43: {s43:.2f}%", (k, s43), (k - .95, s43 + 12), arrowprops=dict(arrowstyle="->"), fontsize=8)
        ax[i, j].set_xticks([0, 1]); ax[i, j].set_xticklabels(["Attacked\nFedAvg", "ETD-FGL"]); ax[i, j].set_ylabel(yl)
        if i == 0: ax[i, j].set_title(d); ax[i, j].set_ylim(60, 90 if d == "Reddit" else 85) if False else None
        if i == 1: ax[i, j].set_ylim(0, 100)
fig.suptitle("Seeds 42/43/44: bars = mean, whiskers = sample SD (ddof=1), dots = individual seeds (left→right: 42, 43, 44)", fontsize=9.5)
fig.tight_layout(); fig.savefig(F / "multiseed_robustness.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/multiseed_robustness_preview.png", dpi=130, bbox_inches="tight"); plt.close()

# ---- Fig 5 learning dynamics (seed 42)
t = pd.read_csv(R / "R07_round_trajectories_seed42_baselines.csv")
fig, ax = plt.subplots(2, 3, figsize=(11, 5.6), sharex=True)
for j, d in enumerate(DS):
    for i, (col, yl) in enumerate([("clean_accuracy_pct", "Clean accuracy (%)"), ("asr_pct", "ASR (%)")]):
        for m in ["Clean FedAvg", "Attacked FedAvg", "FedTGE", "ETD-FGL"]:
            g = t[(t.dataset == d) & (t.method == m)]
            ax[i, j].plot(g["round"], g[col], color=COL[m], lw=1.6 if m == "ETD-FGL" else 1.1, label=m)
        ax[i, j].set_ylabel(yl)
        if i == 0: ax[i, j].set_title(d)
        else: ax[i, j].set_xlabel("Communication round")
ax[0, 0].legend(frameon=False)
fig.suptitle("Seed 42, per-round global-model evaluation (final reported metrics use the best-validation round, not round 50)", fontsize=9.5)
fig.tight_layout(); fig.savefig(F / "learning_dynamics_rounds.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/learning_dynamics_rounds_preview.png", dpi=130, bbox_inches="tight"); plt.close()

# ---- Fig 6 controlled ablation
c = pd.read_csv(R / "R05a_controlled_ablation_per_seed.csv"); pp = pd.read_csv(R / "R06a_paired_differences_per_seed.csv")
V = [("etdfgl_full", "Full\n(9/13+4/13)", "#000000"), ("etdfgl_fixed_no_update", "Fixed no-update\n(9/13 topo)", "#0072B2"), ("etdfgl_fixed_no_topology", "Fixed no-topology\n(4/13 upd)", "#D55E00")]
fig, ax = plt.subplots(2, 3, figsize=(11, 6))
for j, d in enumerate(DS):
    for k, (s, lab, col) in enumerate(V):
        g = c[(c.dataset == d) & (c.slug == s)].sort_values("seed")
        ax[0, j].bar(k, g.asr_pct.mean(), .6, yerr=g.asr_pct.std(ddof=1), capsize=4, color=col, alpha=.4, edgecolor="k")
        ax[0, j].scatter(np.full(3, k) + np.array([-.15, 0, .15]), g.asr_pct, c=col, edgecolor="k", s=26, zorder=3)
    ax[0, j].set_xticks(range(3)); ax[0, j].set_xticklabels([v[1] for v in V], fontsize=7); ax[0, j].set_title(d); ax[0, j].set_ylabel("ASR (%)")
    for k, comp in enumerate(["Remove update channel (Fixed No Update minus Full)", "Remove topology channel (Fixed No Topology minus Full)"]):
        g = pp[(pp.dataset == d) & (pp.comparison == comp)].sort_values("seed")
        ax[1, j].bar(k, g.d_asr_pp.mean(), .6, yerr=g.d_asr_pp.std(ddof=1), capsize=4, color=V[k + 1][2], alpha=.4, edgecolor="k")
        ax[1, j].scatter(np.full(3, k) + np.array([-.15, 0, .15]), g.d_asr_pp, c=V[k + 1][2], edgecolor="k", s=26, zorder=3)
    ax[1, j].axhline(0, c="k", lw=.8); ax[1, j].set_xticks([0, 1]); ax[1, j].set_xticklabels(["Remove update", "Remove topology"]); ax[1, j].set_ylabel("Paired ΔASR vs Full (pp)")
fig.suptitle("Controlled fixed-coefficient ablation, seeds 42/43/44 (dots: seeds, left→right). n=3 pairs; no significance test was run", fontsize=9.5)
fig.tight_layout(); fig.savefig(F / "controlled_ablation.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/controlled_ablation_preview.png", dpi=130, bbox_inches="tight"); plt.close()

# ---- Fig 7 attacker weight
a = pd.read_csv(R / "R08_attacker_weight_trajectories_seed42_controlled.csv")
fig, ax = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
for j, d in enumerate(DS):
    for (s, lab, col), nm in zip(V, ["Full ETD-FGL", "Fixed no-update", "Fixed no-topology"]):
        g = a[(a.dataset == d) & (a.variant.str.startswith({"Full ETD-FGL": "Full", "Fixed no-update": "Fixed No Update", "Fixed no-topology": "Fixed No Topology"}[nm]))]
        ax[j].plot(g["round"], g.attacker_weight_pct, color=col, label=nm, lw=1.5)
    ax[j].axhline(20, color="gray", ls="--", lw=1); ax[j].set_title(d + " (seed 42)"); ax[j].set_xlabel("Communication round")
ax[0].set_ylabel("Attacker aggregation weight $w_0$ (%)"); ax[0].legend(frameon=False, loc="upper center", bbox_to_anchor=(1.7, -.2), ncol=4); ax[2].text(33, 21, "uniform 20% share", fontsize=7, color="gray"); ax[0].set_ylim(0, 27)
fig.tight_layout(); fig.savefig(F / "attacker_weight_dynamics.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/attacker_weight_dynamics_preview.png", dpi=130, bbox_inches="tight"); plt.close()

# ---- Fig 8 runtime
fig, ax = plt.subplots(1, 1, figsize=(7.5, 3.8))
for i, m in enumerate(M):
    v = [b[(b.dataset == d) & (b.method == m)].active_loop_seconds.iloc[0] for d in DS]
    ax.bar(np.arange(3) + (i - 3.5) * .1, v, .1, color=COL[m], label=m, edgecolor="k", linewidth=.3)
ax.set_yscale("log"); ax.set_xticks(range(3)); ax.set_xticklabels(DS); ax.set_ylabel("50-round training-loop wall-clock (s, log)")
ax.legend(ncol=2, fontsize=7, frameon=False)
ax.set_title("Seed 42, single run each; same-method Reddit time varies 7-51 s across suites (see R11)", fontsize=8.5)
fig.tight_layout(); fig.savefig(F / "fig_s03_training_runtime_comparison.pdf", bbox_inches="tight"); fig.savefig(F / "EXTRA/fig_s03_training_runtime_comparison_preview.png", dpi=130, bbox_inches="tight"); plt.close()
print("done")
