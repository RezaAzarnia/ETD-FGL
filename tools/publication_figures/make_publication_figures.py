"""Publication figures for ETD-FGL, rendered ONLY from verified CSV tables (figures/publication/tables).

    python -I tools/publication_figures/make_publication_figures.py figures/publication/tables figures/publication

Outputs: <out>/Fig*.pdf (main), <out>/supplementary/*.pdf, 300-dpi PNG previews in <out>/previews/,
and <out>/plotted_data.json (every array handed to matplotlib; used by tests/test_publication_figures.py).
No value is altered for appearance; sample SD uses ddof=1. No training is run.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

TAB = Path(sys.argv[1])
OUT = Path(sys.argv[2])
(OUT / "supplementary").mkdir(parents=True, exist_ok=True)
(OUT / "previews").mkdir(parents=True, exist_ok=True)

W2 = 7.2  # double-column width (in)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8.5, "axes.labelsize": 7.8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7, "axes.linewidth": .7,
    "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": .22, "grid.linewidth": .5, "lines.linewidth": 1.1,
    "figure.dpi": 100, "savefig.dpi": 300,
})
DS = ["Cora", "PubMed", "Reddit"]
METHODS = ["Clean FedAvg", "Attacked FedAvg", "PD-FL", "GSP-FL", "FLPurifier-GNN", "DMGNN-FL", "FedTGE", "ETD-FGL"]
# Okabe-Ito (colour-blind safe) + marker + hatch so identity never relies on colour alone
COL = dict(zip(METHODS, ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#7F7F7F", "#E69F00", "#56B4E9", "#000000"]))
MK = dict(zip(METHODS, ["o", "X", "s", "^", "v", "D", "P", "*"]))
HT = dict(zip(METHODS, ["", "//", "..", "\\\\", "xx", "++", "--", ""]))
ADAPT = {"PD-FL", "GSP-FL", "FLPurifier-GNN", "DMGNN-FL", "FedTGE"}
LAB = {m: (m + "*" if m in ADAPT else m) for m in METHODS}
PLOTTED: dict = {}


def rec(key, **arrays):
    PLOTTED[key] = {k: [float(x) for x in np.ravel(v)] for k, v in arrays.items()}


def save(fig, name, supp=False):
    d = OUT / ("supplementary" if supp else "")
    fig.savefig(d / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / "previews" / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def panel(ax, s):
    ax.text(-0.02, 1.04, s, transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom", ha="right")


b = pd.read_csv(TAB / "R02_seed42_baselines_tab_seed42_baselines.csv")
ms = pd.read_csv(TAB / "R03a_multiseed_per_seed.csv")
ca = pd.read_csv(TAB / "R05a_controlled_ablation_per_seed.csv")
pp = pd.read_csv(TAB / "R06a_paired_differences_per_seed.csv")
tr = pd.read_csv(TAB / "R07_round_trajectories_seed42_baselines.csv")
aw = pd.read_csv(TAB / "R08_attacker_weight_trajectories_seed42_controlled.csv")
rt = pd.read_csv(TAB / "R11_runtime_same_method_across_suites.csv")


# ------------------------------------------------------------------ Fig 1 architecture
def fig1():
    fig, ax = plt.subplots(figsize=(W2, 3.9))
    ax.set_xlim(0, 184); ax.set_ylim(0, 100); ax.axis("off")
    FS = 5.2

    def box(x, y, w, h, title, lines, fc, ec):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5", fc=fc, ec=ec, lw=0.9))
        ax.text(x + w / 2, y + h - 2.0, title, ha="center", va="top", fontsize=FS + .4, fontweight="bold", color=ec)
        ax.text(x + w / 2, y + h - 9.0, "\n".join(lines), ha="center", va="top", fontsize=FS, linespacing=1.45)

    def arr(p, q, c="#333", ls="-"):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=c, lw=0.9, ls=ls, shrinkA=0, shrinkB=0))

    ax.text(92, 99.5, "ETD-FGL as implemented (simulation: K = 5 clients, M = 1 attacker, IID partition)", ha="center", va="top", fontsize=7.4, fontweight="bold")
    box(1, 58, 40, 34, "Clients 1-4 (benign)", ["train the global model on own", "graph G_i (3 Adam epochs);", "send u_i = theta_i - theta"], "#EEF3FA", "#2F5D9B")
    box(1, 14, 40, 40, "Client 0 (malicious, static)", ["poisoned graph G_0: K3 clique", "trigger on 20 % of non-target", "TRAIN nodes, label -> 0;", "otherwise honest training;", "sends u_0"], "#FBEEEE", "#B03A2E")
    box(47, 58, 46, 34, "Topology evidence (once)", ["clean references G_i^0 held by the", "server (SIMULATION ASSUMPTION);", "current graphs of ALL 5 clients;", "5-D label-free descriptor d(G);", "drift_i = ||(d(G_i)-d(G_i^0))/s||_2"], "#FFF6DD", "#9A6B00")
    box(47, 14, 46, 40, "Update evidence (per round)", ["u_i of ALL 5 clients;", "m = coordinate-wise median of u;", "dist_i = ||u_i - m||_2"], "#E8F5EA", "#2E7D32")
    box(96, 30, 44, 46, "Robust map A = R(v)", ["on drift (once) and dist", "(each round):", "z = max((v-med)/S, 0)", "S = max(1.4826 MAD, std, 1e-8)", "A = clip(2(sigmoid(z)-1/2),0,1)"], "#F3EAF7", "#6A1B9A")
    box(143, 58, 37, 34, "Fusion and trust", ["R_i = 9/13 A_topo + 4/13 A_upd", "T_i = clip(exp(-3 R_i), 0.02, 1)", "w_i = n_i T_i / sum_j n_j T_j", "(n_i: # local training nodes)"], "#F3EAF7", "#6A1B9A")
    box(143, 14, 37, 40, "Server", ["theta <- sum_i w_i theta_i;", "evaluate on global clean +", "triggered graph every round;", "keep best clean-VALIDATION", "round as the checkpoint"], "#E4F2FA", "#0277BD")
    arr((41, 75), (47, 75)); arr((41, 34), (47, 34))
    arr((93, 75), (96, 62)); arr((93, 34), (96, 44)); arr((140, 62), (143, 72)); arr((161.5, 58), (161.5, 54))
    ax.plot([161.5, 161.5, 21, 21], [14, 9, 9, 13.2], color="#0277BD", lw=0.9, ls=":")
    ax.annotate("", xy=(21, 14), xytext=(21, 9.2), arrowprops=dict(arrowstyle="-|>", color="#0277BD", lw=0.9))
    ax.text(92, 10.4, "theta broadcast to all clients for the next round", ha="center", fontsize=5.8, color="#0277BD", style="italic")
    ax.text(92, 3.0, "Logged per client and round: A_topo, A_upd, R, T, w.   Reported at the selected checkpoint: test accuracy, ASR, clean target rate, attack effect.", ha="center", fontsize=5.5, color="#444")
    save(fig, "Fig1_etdfgl_architecture_workflow")


# ------------------------------------------------------------------ Fig 2 baselines (seed 42, single run)
def fig2():
    fig, ax = plt.subplots(1, 2, figsize=(W2, 3.1))
    w = .1
    for k, (col, yl, t) in enumerate([("clean_accuracy_pct", "Clean test accuracy (%)", "(a) Clean accuracy"), ("asr_pct", "Backdoor ASR (%)", "(b) Backdoor attack success rate")]):
        for i, m in enumerate(METHODS):
            v = [b[(b.dataset == d) & (b.method == m)][col].iloc[0] for d in DS]
            rec(f"fig2_{col}_{m}", values=v)
            ax[k].bar(np.arange(3) + (i - 3.5) * w, v, w * .92, color=COL[m], hatch=HT[m], edgecolor="white" if m == "ETD-FGL" else "k", lw=.35, label=LAB[m])
        ax[k].set_xticks(range(3)); ax[k].set_xticklabels(DS); ax[k].set_ylabel(yl); ax[k].set_ylim(0, 100); ax[k].set_title(t, loc="left"); ax[k].grid(axis="x", visible=False)
    h, l = ax[0].get_legend_handles_labels()
    fig.legend(h, l, ncol=4, loc="lower center", bbox_to_anchor=(.5, -.13), frameon=False, columnspacing=1.2)
    fig.text(.5, -.19, "Seed 42, one run per bar (no uncertainty shown).  * adapted re-implementations, not exact reproductions of the original methods.", ha="center", fontsize=6.8, style="italic")
    fig.tight_layout(); save(fig, "Fig2_overall_baselines")


# ------------------------------------------------------------------ Fig 3 accuracy vs ASR
def fig3():
    fig, ax = plt.subplots(1, 3, figsize=(W2, 3.0))
    for j, d in enumerate(DS):
        for m in METHODS:
            r = b[(b.dataset == d) & (b.method == m)].iloc[0]
            rec(f"fig3_seed42_{d}_{m}", x=r.clean_accuracy_pct, y=r.asr_pct)
            ax[j].scatter(r.clean_accuracy_pct, r.asr_pct, marker=MK[m], s=34 if m != "ETD-FGL" else 70, facecolor="none" if m not in ("ETD-FGL",) else COL[m],
                          edgecolor=COL[m], linewidth=1.0, zorder=3)
        for m in ["Attacked FedAvg", "ETD-FGL"]:
            g = ms[(ms.dataset == d) & (ms.method == m)]
            x, y, sx, sy = g.clean_accuracy_pct.mean(), g.asr_pct.mean(), g.clean_accuracy_pct.std(ddof=1), g.asr_pct.std(ddof=1)
            rec(f"fig3_mean3_{d}_{m}", x=x, y=y, sx=sx, sy=sy)
            ax[j].errorbar(x, y, xerr=sx, yerr=sy, fmt=MK[m], color=COL[m], ms=9 if m != "ETD-FGL" else 12, mfc=COL[m], mec="k" if m != "ETD-FGL" else "white", mew=.6,
                           ecolor=COL[m], elinewidth=1.0, capsize=2.5, alpha=.55, zorder=4)
        ax[j].set_title(d, loc="left"); ax[j].set_xlabel("Clean accuracy (%)  higher is better"); ax[j].set_ylim(-6, 105)
        if j == 0: ax[j].set_ylabel("ASR (%)  lower is better")
        ax[j].text(.02, .02, "desirable region: lower right", transform=ax[j].transAxes, ha="left", fontsize=6.0, color="#555", style="italic")
    hs = [Line2D([], [], marker=MK[m], ls="", color=COL[m], mfc="none" if m != "ETD-FGL" else COL[m], ms=6, label=LAB[m] + " (seed 42, open)") for m in METHODS]
    hs += [Line2D([], [], marker=MK[m], ls="", color=COL[m], ms=8, alpha=.6, label=m + " (3-seed mean ± SD, filled)") for m in ["Attacked FedAvg", "ETD-FGL"]]
    fig.legend(handles=hs, ncol=3, loc="lower center", bbox_to_anchor=(.5, -.2), frameon=False, fontsize=6.6, columnspacing=1.0)
    fig.text(.5, -.265, "Per-dataset panels; no cross-dataset Pareto frontier is claimed. SD = sample SD (ddof = 1, n = 3). * adapted baselines.", ha="center", fontsize=6.6, style="italic")
    fig.tight_layout(); save(fig, "Fig3_accuracy_robustness_tradeoff")


# ------------------------------------------------------------------ Fig 4 multi-seed
def fig4():
    fig, ax = plt.subplots(2, 3, figsize=(W2, 4.6))
    off = {42: -.2, 43: 0, 44: .2}
    for j, d in enumerate(DS):
        for i, (col, yl) in enumerate([("clean_accuracy_pct", "Clean accuracy (%)"), ("asr_pct", "ASR (%)")]):
            a = ax[i, j]
            for k, m in enumerate(["Attacked FedAvg", "ETD-FGL"]):
                g = ms[(ms.dataset == d) & (ms.method == m)].sort_values("seed")
                mean, sd = g[col].mean(), g[col].std(ddof=1)
                rec(f"fig4_{col}_{d}_{m}", per_seed=g[col].values, mean=mean, sd=sd)
                a.bar(k, mean, .55, yerr=sd, capsize=3, color=COL[m], alpha=.28, edgecolor=COL[m], lw=.8, error_kw=dict(lw=.9))
                for _, r in g.iterrows():
                    a.scatter(k + off[int(r.seed)], r[col], s=20, color=COL[m], edgecolor="k", linewidth=.4, zorder=3)
                    if col == "asr_pct": a.text(k + off[int(r.seed)], r[col] + 2.2, str(int(r.seed)), ha="center", fontsize=5.8)
            a.set_xticks([0, 1]); a.set_xticklabels(["Attacked\nFedAvg", "ETD-FGL"]); a.set_ylabel(yl); a.grid(axis="x", visible=False)
            if i == 0: a.set_title(d, loc="left"); a.set_ylim(60 if d != "Cora" and False else 0, 100)
            if i == 1:
                a.set_ylim(0, 105)
                if d == "Reddit":
                    s43 = ms[(ms.dataset == d) & (ms.method == "ETD-FGL") & (ms.seed == 43)].asr_pct.iloc[0]
                    a.annotate(f"seed 43: {s43:.2f} %\n(cause not established)", (1 + off[43], s43), (.1, 47), fontsize=6.4, arrowprops=dict(arrowstyle="->", lw=.7))
    fig.text(.5, -.005, "Bars: mean; whiskers: sample SD (ddof = 1, n = 3); dots: individual seeds (labels 42/43/44). No significance test was performed.", ha="center", fontsize=6.6, style="italic")
    fig.tight_layout(rect=(0, .02, 1, 1)); save(fig, "Fig4_multiseed_robustness")


# ------------------------------------------------------------------ Fig 5 dynamics
def fig5():
    fig, ax = plt.subplots(2, 3, figsize=(W2, 4.6), sharex=True)
    show = ["Clean FedAvg", "Attacked FedAvg", "FedTGE", "ETD-FGL"]
    ls = {"Clean FedAvg": (0, (4, 1.5)), "Attacked FedAvg": "-", "FedTGE": (0, (1, 1)), "ETD-FGL": "-"}
    for j, d in enumerate(DS):
        for i, (col, yl) in enumerate([("clean_accuracy_pct", "Clean accuracy (%)"), ("asr_pct", "ASR (%)")]):
            a = ax[i, j]
            for m in show:
                g = tr[(tr.dataset == d) & (tr.method == m)].sort_values("round")
                rec(f"fig5_{col}_{d}_{m}", round=g["round"].values, y=g[col].values)
                a.plot(g["round"], g[col], color=COL[m], ls=ls[m], lw=1.5 if m == "ETD-FGL" else 0.95, label=LAB[m], marker=MK[m] if m == "ETD-FGL" else None, ms=2.2, markevery=5)
            if i == 1:
                a.set_xlabel("Communication round")
                a.set_ylim(-3, 103)
            a.set_xlim(1, 50); a.set_ylabel(yl)
            if i == 0: a.set_title(d, loc="left")
        a1 = ax[1, j]
        g = tr[(tr.dataset == d) & (tr.method == "ETD-FGL")].sort_values("round")
        a1.annotate(f"round 1: {g.asr_pct.iloc[0]:.1f} %", (1, g.asr_pct.iloc[0]), (8, 22 if g.asr_pct.iloc[0] < 10 else 70), fontsize=6.3, arrowprops=dict(arrowstyle="->", lw=.6))
    h, l = ax[0, 0].get_legend_handles_labels()
    fig.legend(h, l, ncol=4, loc="lower center", bbox_to_anchor=(.5, -.065), frameon=False)
    fig.text(.5, -.1, "Seed 42, all 50 rounds, unsmoothed. Reported table values use the best clean-validation round, not round 50. * adapted baseline.", ha="center", fontsize=6.6, style="italic")
    fig.tight_layout(); save(fig, "Fig5_learning_dynamics_rounds")


# ------------------------------------------------------------------ Fig 6 controlled ablation
def fig6():
    V = [("etdfgl_full", "Full\n9/13 + 4/13", "#000000"), ("etdfgl_fixed_no_update", "No update\n9/13 + 0", "#0072B2"), ("etdfgl_fixed_no_topology", "No topology\n0 + 4/13", "#D55E00")]
    sc = {42: "o", 43: "s", 44: "^"}
    fig, ax = plt.subplots(2, 3, figsize=(W2, 4.9))
    for j, d in enumerate(DS):
        a = ax[0, j]
        data = {s: ca[(ca.dataset == d) & (ca.slug == s)].sort_values("seed") for s, _, _ in V}
        for k, (s, lab, col) in enumerate(V):
            g = data[s]
            rec(f"fig6_asr_{d}_{s}", per_seed=g.asr_pct.values, mean=g.asr_pct.mean(), sd=g.asr_pct.std(ddof=1))
            a.bar(k, g.asr_pct.mean(), .58, yerr=g.asr_pct.std(ddof=1), capsize=3, color=col, alpha=.25, edgecolor=col, lw=.8)
            for _, r in g.iterrows(): a.scatter(k, r.asr_pct, marker=sc[int(r.seed)], s=22, color=col, edgecolor="k", linewidth=.4, zorder=3)
        for sd_ in (42, 43, 44):  # paired lines across variants
            ys = [data[s][data[s].seed == sd_].asr_pct.iloc[0] for s, _, _ in V]
            a.plot(range(3), ys, color="#888", lw=.6, zorder=2)
        a.set_xticks(range(3)); a.set_xticklabels([v[1] for v in V], fontsize=6.2); a.set_title(d, loc="left"); a.set_ylabel("ASR (%)"); a.grid(axis="x", visible=False)
        a2 = ax[1, j]
        for k, comp in enumerate(["Remove update channel (Fixed No Update minus Full)", "Remove topology channel (Fixed No Topology minus Full)"]):
            g = pp[(pp.dataset == d) & (pp.comparison == comp)].sort_values("seed")
            col = V[k + 1][2]
            rec(f"fig6_delta_{d}_{k}", per_seed=g.d_asr_pp.values, mean=g.d_asr_pp.mean(), sd=g.d_asr_pp.std(ddof=1))
            a2.bar(k, g.d_asr_pp.mean(), .58, yerr=g.d_asr_pp.std(ddof=1), capsize=3, color=col, alpha=.25, edgecolor=col, lw=.8)
            for _, r in g.iterrows(): a2.scatter(k, r.d_asr_pp, marker=sc[int(r.seed)], s=22, color=col, edgecolor="k", linewidth=.4, zorder=3)
        a2.axhline(0, color="k", lw=.7); a2.set_xticks([0, 1]); a2.set_xticklabels(["Remove\nupdate channel", "Remove\ntopology channel"], fontsize=6.4)
        a2.set_ylabel("Paired Δ ASR vs Full (pp)"); a2.grid(axis="x", visible=False)
    hs = [Line2D([], [], marker=sc[s], ls="", color="#555", mec="k", ms=5, label=f"seed {s}") for s in (42, 43, 44)]
    fig.legend(handles=hs, ncol=3, loc="lower center", bbox_to_anchor=(.5, -.015), frameon=False)
    fig.text(.5, -.06, "Fixed-coefficient (NOT renormalized) ablation. Bars: mean; whiskers: sample SD (ddof = 1); n = 3 paired seeds; no statistical test was run.\n"
             "Grey lines connect the same seed across variants (top row).", ha="center", fontsize=6.6, style="italic")
    fig.tight_layout(); save(fig, "Fig6_controlled_ablation")


# ------------------------------------------------------------------ Fig 7 attacker weight
def fig7():
    fig, ax = plt.subplots(1, 3, figsize=(W2, 2.9), sharey=True)
    V = [("Full", "Full ETD-FGL", "#000000", "-"), ("Fixed No Update", "No update (9/13 topo)", "#0072B2", (0, (4, 1.5))), ("Fixed No Topology", "No topology (4/13 upd)", "#D55E00", "-")]
    for j, d in enumerate(DS):
        for key, lab, col, ls in V:
            g = aw[(aw.dataset == d) & (aw.variant.str.startswith(key))].sort_values("round")
            rec(f"fig7_{d}_{key}", round=g["round"].values, w0=g.attacker_weight_pct.values)
            noisy = key == "Fixed No Topology"
            ax[j].plot(g["round"], g.attacker_weight_pct, color=col, ls=ls, lw=.7 if noisy else 1.4, alpha=.45 if noisy else 1, label=lab + (" (raw per round)" if noisy else ""))
            if noisy:
                sm = g.attacker_weight_pct.rolling(5, center=True, min_periods=3).mean()
                ax[j].plot(g["round"], sm, color=col, lw=1.8, label="5-round moving average (visual aid only)")
        ax[j].axhline(20, color="#777", ls="--", lw=.9); ax[j].set_title(d + " (seed 42)", loc="left"); ax[j].set_xlabel("Communication round"); ax[j].set_ylim(0, 27); ax[j].set_xlim(1, 50)
    ax[2].text(49, 20.7, "uniform share 20 %", ha="right", fontsize=6.3, color="#555")
    ax[0].set_ylabel("Attacker weight $w_0$ (%)")
    h, l = ax[0].get_legend_handles_labels()
    fig.legend(h, l, ncol=4, loc="lower center", bbox_to_anchor=(.5, -.2), frameon=False, fontsize=6.6)
    fig.tight_layout(); save(fig, "Fig7_attacker_weight_dynamics")


# ------------------------------------------------------------------ Fig 8 runtime (SUPPLEMENTARY, exploratory)
def fig8():
    fig, ax = plt.subplots(1, 2, figsize=(W2, 3.3))
    for i, m in enumerate(METHODS):
        v = [b[(b.dataset == d) & (b.method == m)].active_loop_seconds.iloc[0] for d in DS]
        rec(f"fig8_{m}", seconds=v)
        ax[0].bar(np.arange(3) + (i - 3.5) * .1, v, .092, color=COL[m], hatch=HT[m], edgecolor="k", lw=.3, label=LAB[m])
    ax[0].set_yscale("log"); ax[0].set_xticks(range(3)); ax[0].set_xticklabels(DS); ax[0].set_ylabel("50-round loop wall-clock (s, log)"); ax[0].set_title("(a) Seed-42 single runs", loc="left")
    ax[0].legend(ncol=4, fontsize=5.6, frameon=False, loc="upper center", bbox_to_anchor=(.5, -.1)); ax[0].set_ylim(2, 1500)
    g = rt[(rt.dataset == "Reddit") & (rt.slug == "fedavg_structural_backdoor")]
    ya = g.active_loop_seconds.values; xa = np.arange(len(ya))
    rec("fig8_reddit_attacked_fedavg_runs", seconds=ya)
    lab = [f"{r.suite.split('_')[0]}\nseed {int(r.seed)}" for r in g.itertuples()]
    ax[1].scatter(xa, ya, color=COL["Attacked FedAvg"], marker="X", s=36, edgecolor="k", linewidth=.4)
    ax[1].set_xticks(xa); ax[1].set_xticklabels([l.replace("\n", " ") for l in lab], fontsize=5.6, rotation=40, ha="right")
    ax[1].set_ylabel("seconds"); ax[1].set_title("(b) Attacked FedAvg on Reddit: same method, different runs", loc="left", fontsize=7.4)
    fig.suptitle("SUPPLEMENTARY / EXPLORATORY - not evidence of low overhead or speed advantage (single runs, hardware not recorded, 2.5x variation for identical seed-42 runs)",
                 fontsize=6.9, color="#B03A2E", y=1.03)
    fig.tight_layout(); save(fig, "FigS_runtime_exploratory", supp=True)


for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8):
    f()
(OUT / "plotted_data.json").write_text(json.dumps(PLOTTED), encoding="utf-8")
print("rendered", len(PLOTTED), "plotted series")
