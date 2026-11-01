"""Publication figures for ETD-FGL (design v3, formal journal style), rendered ONLY from verified CSV tables.

    python -I tools/publication_figures/make_publication_figures.py figures/publication/tables <out_dir>

Outputs: <out>/Fig*.pdf (main), <out>/supplementary/*.pdf, 300-dpi PNG previews in <out>/previews/,
and <out>/plotted_data.json (every array handed to matplotlib; used by test_publication_figures.py).
Captions and methodological caveats live in figures/publication/FIGURE_CAPTIONS.md, not inside the figures.
Design v3 changes presentation only; no plotted value, SD convention (sample SD, ddof=1) or axis meaning changes.
All figures are 7.2 in wide (double column). No training is run.
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
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

TAB = Path(sys.argv[1])
OUT = Path(sys.argv[2])
(OUT / "supplementary").mkdir(parents=True, exist_ok=True)
(OUT / "previews").mkdir(parents=True, exist_ok=True)

W2 = 7.2  # double-column width (in)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.8, "axes.titlesize": 8.6, "axes.labelsize": 7.8, "legend.fontsize": 7.4,
    "xtick.labelsize": 7.4, "ytick.labelsize": 7.4, "axes.linewidth": 0.7, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.22, "grid.linewidth": 0.45,
    "lines.linewidth": 1.2, "figure.dpi": 100, "savefig.dpi": 300,
})
DS = ["Cora", "PubMed", "Reddit"]
METHODS = ["Clean FedAvg", "Attacked FedAvg", "PD-FL", "GSP-FL", "FLPurifier-GNN", "DMGNN-FL", "FedTGE", "ETD-FGL"]
COL = dict(zip(METHODS, ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#7F7F7F", "#E69F00", "#56B4E9", "#000000"]))
MK = dict(zip(METHODS, ["o", "X", "s", "^", "v", "D", "P", "*"]))
ADAPT = {"PD-FL", "GSP-FL", "FLPurifier-GNN", "DMGNN-FL", "FedTGE"}
LAB = {m: (m + "*" if m in ADAPT else m) for m in METHODS}
RED = "#B03A2E"
PLOTTED: dict = {}


def rec(key, **arrays):
    PLOTTED[key] = {k: [float(x) for x in np.ravel(v)] for k, v in arrays.items()}


def save(fig, name, supp=False):
    d = OUT / ("supplementary" if supp else "")
    fig.savefig(d / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / "previews" / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def letter(ax, s, dx=-0.18, dy=1.05):
    ax.text(dx, dy, s, transform=ax.transAxes, fontweight="bold", fontsize=9.5, va="bottom", ha="left")


b = pd.read_csv(TAB / "R02_seed42_baselines_tab_seed42_baselines.csv")
ms = pd.read_csv(TAB / "R03a_multiseed_per_seed.csv")
ca = pd.read_csv(TAB / "R05a_controlled_ablation_per_seed.csv")
pp = pd.read_csv(TAB / "R06a_paired_differences_per_seed.csv")
tr = pd.read_csv(TAB / "R07_round_trajectories_seed42_baselines.csv")
aw = pd.read_csv(TAB / "R08_attacker_weight_trajectories_seed42_controlled.csv")
rt = pd.read_csv(TAB / "R11_runtime_same_method_across_suites.csv")


# ====================================================================== Fig 1: architecture
def fig1():
    fig, ax = plt.subplots(figsize=(W2, 4.3))
    ax.set_xlim(0, 144); ax.set_ylim(-6, 82); ax.axis("off"); ax.set_position([0, 0, 1, 1])
    FS = 6.7
    GREY, ORG, GRN, PUR, BLU = "#F3F3F3", "#FFF1D6", "#E6F3E8", "#EFE7F5", "#E3F0FA"
    EO, EG, EP, EB = "#9A6B00", "#2E7D32", "#6A1B9A", "#0277BD"

    def box(x, y, w, h, fc, ec, lw=1.0, ls="-"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.0", fc=fc, ec=ec, lw=lw, ls=ls))

    def txt(x, y, s, fs=FS, ha="center", va="center", **kw):
        ax.text(x, y, s, fontsize=fs, ha=ha, va=va, linespacing=1.35, **kw)

    def arr(p, q, c="#222", ls="-", lw=1.0):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, ls=ls, shrinkA=0, shrinkB=0, mutation_scale=8))

    # --- clients (left)
    for k, y in enumerate([69, 57, 45, 33]):
        box(1, y, 26, 9, "#F2F6FB", "#2F5D9B", lw=0.9)
        txt(14, y + 6.3, f"Client {k + 1} (benign)", fontweight="bold", color="#2F5D9B")
        txt(14, y + 2.7, "graph $G_{%d}$,  update $u_{%d}^{t}$" % (k + 1, k + 1), fs=6.4)
    box(1, 3, 26, 27, "#FBEEEE", RED, lw=1.2)
    txt(14, 27.0, "Client 0 (malicious)", fontweight="bold", color=RED)
    # trigger illustration: victim node v with K3 attached
    vx, vy = 6.5, 15.5
    tri = [(14.5, 21.0), (19.5, 15.5), (14.5, 10.0)]
    for (x_, y_) in tri:
        ax.plot([vx, x_], [vy, y_], color="#555", lw=0.9, zorder=2)
    for i in range(3):
        for j in range(i + 1, 3):
            ax.plot([tri[i][0], tri[j][0]], [tri[i][1], tri[j][1]], color=RED, lw=1.1, zorder=2)
    ax.add_patch(Circle((vx, vy), 1.6, fc="#2F5D9B", ec="white", lw=0.6, zorder=3))
    for (x_, y_) in tri:
        ax.add_patch(Circle((x_, y_), 1.3, fc=RED, ec="white", lw=0.6, zorder=3))
    txt(vx, vy - 3.6, "victim $v$", fs=6.0)
    txt(21.5, 23.3, "K3 trigger", fs=6.0, color=RED)
    txt(14, 6.2, "label($v$) $\\to$ target class;  $G_0$ poisoned", fs=6.0)
    # --- collector bracket: all five clients feed both channels
    bx = 30.5
    ax.plot([27.2, bx, bx, 27.2], [73.5, 73.5, 16.5, 16.5], color="#222", lw=0.9)
    for y_ in (73.5, 61.5, 49.5, 37.5, 16.5):
        ax.plot([27.2, bx], [y_, y_], color="#222", lw=0.9)
    arr((bx, 62), (39.5, 62)); arr((bx, 28), (39.5, 28))
    txt(35, 66.3, "$G_i$\n$i=1..5$", fs=6.2); txt(35, 32.5, "$u_i^{t}$\n$i=1..5$", fs=6.2)

    # --- static topology profiling
    box(40, 46, 49, 33, ORG, EO, lw=1.1)
    txt(64.5, 76.2, "Static topology profiling (once)", fontweight="bold", color=EO, fs=6.9)
    txt(64.5, 69.0, "$d(G)$: 5-D label-free descriptor", fs=FS)
    txt(64.5, 62.4, "drift$_i$ = $\\|(d(G_i) - d(G_i^{0}))\\,/\\,s\\|_2$", fs=FS)
    txt(64.5, 55.8, "$A^{topo}_i = \\mathcal{R}$(drift$_i$)", fs=FS)
    box(44, 47.2, 41, 5.6, "white", EO, lw=0.9, ls="--")
    txt(64.5, 50.0, "clean references $G_i^{0}$: simulation assumption", fs=6.2, color="#7A5200")
    # --- per-round update analysis
    box(40, 3, 49, 40, GRN, EG, lw=1.1)
    txt(64.5, 39.9, "Per-round update analysis (every round $t$)", fontweight="bold", color=EG, fs=6.9)
    txt(64.5, 32.0, "$m^{t}$ = coordinate-wise median of $\\{u_j^{t}\\}$", fs=FS)
    txt(64.5, 24.4, "dist$_i^{t}$ = $\\|u_i^{t} - m^{t}\\|_2$", fs=FS)
    txt(64.5, 17.0, "$A^{upd}_{i,t} = \\mathcal{R}$(dist$_i^{t}$)", fs=FS)
    txt(64.5, 8.4, "$\\mathcal{R}$: one-sided robust score in [0, 1]\n(median/MAD, std)", fs=6.0, color="#333")
    # --- fusion and aggregation
    box(96, 46, 47, 33, PUR, EP, lw=1.1)
    txt(119.5, 76.2, "Risk fusion and trust", fontweight="bold", color=EP, fs=6.9)
    txt(119.5, 67.0, "$R_i^{t} = \\frac{9}{13}A^{topo}_i + \\frac{4}{13}A^{upd}_{i,t}$", fs=FS + 0.4)
    txt(119.5, 57.0, "$T_i^{t} = \\mathrm{clip}(e^{-3R_i^{t}},\\,0.02,\\,1)$", fs=FS + 0.4)
    box(96, 3, 47, 40, BLU, EB, lw=1.1)
    txt(119.5, 39.9, "Weighted aggregation", fontweight="bold", color=EB, fs=6.9)
    txt(119.5, 31.0, "$w_i^{t} = n_i T_i^{t}\\,/\\,\\sum_j n_j T_j^{t}$", fs=FS + 0.4)
    txt(119.5, 22.5, "$\\theta^{t} = \\sum_i w_i^{t}\\,\\theta_i^{t}$", fs=FS + 0.4)
    txt(119.5, 11.5, "checkpoint: round with best\nclean validation accuracy", fs=6.2)
    arr((89, 62), (96, 66)); arr((89, 24), (96, 56)); arr((119.5, 46), (119.5, 43))
    # --- broadcast
    ax.plot([143.5, 143.5], [20, -2.0], color=EB, lw=0.9, ls=":")
    ax.plot([143.5, 14], [-2.0, -2.0], color=EB, lw=0.9, ls=":")
    arr((14, -2.0), (14, 2.7), EB, ":")
    txt(80, -4.2, "global model $\\theta^{t}$ broadcast to all clients", fs=6.0, color=EB)
    save(fig, "Fig1_etdfgl_architecture_workflow")


# ====================================================================== Fig 2: baselines (horizontal bars)
def fig2():
    fig, axs = plt.subplots(2, 3, figsize=(W2, 5.0), sharey=True)
    fig.subplots_adjust(top=0.95, bottom=0.17, hspace=0.50, wspace=0.12, left=0.16, right=0.985)
    order = METHODS[::-1]
    for r, (col, xl, t) in enumerate([("asr_pct", "ASR (%)", "ASR"), ("clean_accuracy_pct", "Clean accuracy (%)", "Accuracy")]):
        for j, d in enumerate(DS):
            a = axs[r, j]
            vals = [b[(b.dataset == d) & (b.method == m)][col].iloc[0] for m in order]
            for m, v in zip(order, vals):
                rec(f"fig2_{col}_{d}_{m}", value=v)
            cols = [COL[m] if m in ("ETD-FGL", "Attacked FedAvg", "Clean FedAvg") else "#C9C9C9" for m in order]
            yy = np.arange(len(order))
            a.barh(yy, vals, height=0.72, color=cols, edgecolor=["black" if m == "ETD-FGL" else "none" for m in order], linewidth=1.0)
            for y_, v in zip(yy, vals):
                a.text(v + 1.2, y_, f"{v:.1f}", va="center", fontsize=6.6, fontweight="bold" if order[y_] == "ETD-FGL" else "normal")
            a.set_xlim(0, 112); a.set_yticks(yy); a.set_yticklabels([LAB[m] for m in order], fontsize=7.4)
            [t_.set_fontweight("bold") for t_ in a.get_yticklabels() if t_.get_text() == "ETD-FGL"]
            a.grid(axis="y", visible=False); a.set_xlabel(xl, fontsize=7.6)
            a.set_title(d, fontweight="bold", fontsize=8.8) if r == 0 else None
        letter(axs[r, 0], f"({'ab'[r]})", dx=-0.95, dy=1.08)
    save(fig, "Fig2_overall_baselines")


# ====================================================================== Fig S2: accuracy vs ASR (supplementary)
def fig3():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.9))
    fig.subplots_adjust(top=0.92, bottom=0.36, wspace=0.28, left=0.07, right=0.99)
    key = ["Clean FedAvg", "Attacked FedAvg", "ETD-FGL"]
    for j, d in enumerate(DS):
        a = axs[j]
        for m in METHODS:
            r = b[(b.dataset == d) & (b.method == m)].iloc[0]
            rec(f"fig3_seed42_{d}_{m}", x=r.clean_accuracy_pct, y=r.asr_pct)
            if m in key:
                a.scatter(r.clean_accuracy_pct, r.asr_pct, marker=MK[m], s=48 if m != "ETD-FGL" else 80, facecolor="none", edgecolor=COL[m], linewidth=1.3, zorder=4)
            else:
                a.scatter(r.clean_accuracy_pct, r.asr_pct, marker=MK[m], s=28, facecolor="none", edgecolor="#8C8C8C", linewidth=0.9, zorder=3)
        for m in ["Attacked FedAvg", "ETD-FGL"]:
            g = ms[(ms.dataset == d) & (ms.method == m)]
            x, y, sx, sy = g.clean_accuracy_pct.mean(), g.asr_pct.mean(), g.clean_accuracy_pct.std(ddof=1), g.asr_pct.std(ddof=1)
            rec(f"fig3_mean3_{d}_{m}", x=x, y=y, sx=sx, sy=sy)
            a.errorbar(x, y, xerr=sx, yerr=sy, fmt="s" if m != "ETD-FGL" else "D", color=COL[m], ms=4.5, mfc=COL[m], mec="white", mew=0.6, ecolor=COL[m],
                       elinewidth=1.0, capsize=2.5, alpha=0.75, zorder=5)
        a.set_ylim(-6, 106); a.set_title(d, loc="left", fontweight="bold", fontsize=8.8)
        a.set_xlabel("Clean accuracy (%)")
        if j == 0: a.set_ylabel("ASR (%)")
    hs = [Line2D([], [], marker=MK[m], ls="", mfc="none", mec=COL[m], mew=1.3, ms=6, label=LAB[m] + ", seed 42") for m in key]
    hs += [Line2D([], [], marker="o", ls="", mfc="none", mec="#8C8C8C", mew=0.9, ms=5, label="other baselines*, seed 42")]
    hs += [Line2D([], [], marker="s", ls="-", color="#444", mfc="#444", mec="white", ms=5, label="3-seed mean ± sample SD (filled)")]
    fig.legend(handles=hs, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=7.2, columnspacing=1.2)
    save(fig, "FigS2_accuracy_asr_scatter", supp=True)


# ====================================================================== Fig 4: multi-seed (strip plots)
def fig4():
    fig, axs = plt.subplots(2, 3, figsize=(W2, 4.6))
    fig.subplots_adjust(top=0.93, bottom=0.17, hspace=0.40, wspace=0.34, left=0.09, right=0.99)
    sm = {42: "o", 43: "s", 44: "^"}
    for j, d in enumerate(DS):
        for i, (col, yl) in enumerate([("clean_accuracy_pct", "Clean accuracy (%)"), ("asr_pct", "ASR (%)")]):
            a = axs[i, j]
            for k, m in enumerate(["Attacked FedAvg", "ETD-FGL"]):
                g = ms[(ms.dataset == d) & (ms.method == m)].sort_values("seed")
                mean, sd = g[col].mean(), g[col].std(ddof=1)
                rec(f"fig4_{col}_{d}_{m}", per_seed=g[col].values, mean=mean, sd=sd)
                a.errorbar(k, mean, yerr=sd, fmt="none", ecolor=COL[m], elinewidth=1.5, capsize=4.5, capthick=1.5, zorder=2, alpha=0.85)
                a.hlines(mean, k - 0.24, k + 0.24, color=COL[m], lw=2.2, zorder=3)
                for _, r in g.iterrows():
                    out = (d == "Reddit" and col == "asr_pct" and m == "ETD-FGL" and int(r.seed) == 43)
                    a.scatter(k + {42: -0.17, 43: 0.0, 44: 0.17}[int(r.seed)], r[col], marker=sm[int(r.seed)], s=44 if out else 30, color=COL[m],
                              edgecolor=RED if out else "white", linewidth=1.8 if out else 0.7, zorder=5)
            a.set_xlim(-0.6, 1.6); a.set_xticks([0, 1]); a.set_xticklabels(["Attacked\nFedAvg", "ETD-FGL"], fontsize=7.4); a.grid(axis="x", visible=False)
            a.set_ylabel(yl)
            if i == 0: a.set_title(d, fontweight="bold", fontsize=8.8)
            if i == 1:
                a.set_ylim(-4, 104)
                if d == "Reddit":
                    s43 = ms[(ms.dataset == d) & (ms.method == "ETD-FGL") & (ms.seed == 43)].asr_pct.iloc[0]
                    a.annotate(f"seed 43: {s43:.2f} %", (0.93, s43), (-0.5, 50), fontsize=6.8, color=RED, fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9))
    letter(axs[0, 0], "(a)", dx=-0.32); letter(axs[1, 0], "(b)", dx=-0.32)
    hs = [Line2D([], [], marker=sm[s], ls="", color="#555", mec="white", ms=6, label=f"seed {s}") for s in (42, 43, 44)]
    hs += [Line2D([], [], color="#555", lw=2.2, label="mean"), Line2D([], [], color="#555", lw=1.5, marker="_", ms=7, label="± sample SD")]
    fig.legend(handles=hs, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=7.4)
    save(fig, "Fig4_multiseed_robustness")


# ====================================================================== Fig 5: dynamics
def fig5():
    fig, axs = plt.subplots(2, 3, figsize=(W2, 4.7))
    fig.subplots_adjust(top=0.93, bottom=0.14, hspace=0.38, wspace=0.28, left=0.09, right=0.99)
    sty = {"Clean FedAvg": dict(color=COL["Clean FedAvg"], ls=(0, (4, 1.6)), lw=1.3), "Attacked FedAvg": dict(color=COL["Attacked FedAvg"], ls="-", lw=1.4),
           "ETD-FGL": dict(color="#000000", ls="-", lw=1.9)}
    for j, d in enumerate(DS):
        for i, (col, yl) in enumerate([("clean_accuracy_pct", "Clean accuracy (%)"), ("asr_pct", "ASR (%)")]):
            a = axs[i, j]
            for m, s in sty.items():
                g = tr[(tr.dataset == d) & (tr.method == m)].sort_values("round")
                rec(f"fig5_{col}_{d}_{m}", round=g["round"].values, y=g[col].values)
                a.plot(g["round"], g[col], color=s["color"], ls=s["ls"], lw=s["lw"], label=m, zorder=5 if m == "ETD-FGL" else 3)
            a.set_xlim(1, 50); a.set_ylabel(yl)
            if i == 0: a.set_title(d, fontweight="bold", fontsize=8.8)
            if i == 1:
                a.set_xlabel("Communication round"); a.set_ylim(-3, 103)
                g = tr[(tr.dataset == d) & (tr.method == "ETD-FGL")].sort_values("round")
                v1 = g.asr_pct.iloc[0]
                a.scatter([1], [v1], s=55, facecolor="none", edgecolor=RED, linewidth=1.5, zorder=7, clip_on=False)
                a.text(0.5, 1.03, f"ETD-FGL, round 1: {v1:.1f} %", transform=a.transAxes, ha="center", va="bottom", fontsize=6.9, color=RED, fontweight="bold")
    letter(axs[0, 0], "(a)", dx=-0.32); letter(axs[1, 0], "(b)", dx=-0.32, dy=1.14)
    h, l = axs[0, 0].get_legend_handles_labels()
    fig.legend(h, l, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=7.6)
    save(fig, "Fig5_learning_dynamics_rounds")


# ====================================================================== Fig 6: controlled ablation
def fig6():
    V = [("etdfgl_full", "Full\n(9/13, 4/13)", "#000000"), ("etdfgl_fixed_no_update", "No update\n(9/13, 0)", "#0072B2"), ("etdfgl_fixed_no_topology", "No topology\n(0, 4/13)", "#D55E00")]
    sc = {42: "o", 43: "s", 44: "^"}
    fig, axs = plt.subplots(2, 3, figsize=(W2, 4.9))
    fig.subplots_adjust(top=0.94, bottom=0.16, hspace=0.50, wspace=0.34, left=0.09, right=0.99)
    for j, d in enumerate(DS):
        a = axs[0, j]
        data = {s: ca[(ca.dataset == d) & (ca.slug == s)].sort_values("seed") for s, _, _ in V}
        for k, (s, lab, col) in enumerate(V):
            g = data[s]
            rec(f"fig6_asr_{d}_{s}", per_seed=g.asr_pct.values, mean=g.asr_pct.mean(), sd=g.asr_pct.std(ddof=1))
            a.errorbar(k, g.asr_pct.mean(), yerr=g.asr_pct.std(ddof=1), fmt="none", ecolor=col, elinewidth=1.5, capsize=4.5, capthick=1.5, alpha=0.85, zorder=2)
            a.hlines(g.asr_pct.mean(), k - 0.27, k + 0.27, color=col, lw=2.2, zorder=3)
            for _, r in g.iterrows(): a.scatter(k, r.asr_pct, marker=sc[int(r.seed)], s=32, color=col, edgecolor="white", linewidth=0.7, zorder=5)
        for sd_ in (42, 43, 44):
            a.plot(range(3), [data[s][data[s].seed == sd_].asr_pct.iloc[0] for s, _, _ in V], color="#999", lw=0.7, zorder=1)
        a.set_xticks(range(3)); a.set_xticklabels([v[1] for v in V], fontsize=6.9); a.set_xlim(-0.5, 2.5)
        a.set_title(d, fontweight="bold", fontsize=8.8); a.set_ylabel("ASR (%)"); a.grid(axis="x", visible=False)
        a2 = axs[1, j]
        for k, comp in enumerate(["Remove update channel (Fixed No Update minus Full)", "Remove topology channel (Fixed No Topology minus Full)"]):
            g = pp[(pp.dataset == d) & (pp.comparison == comp)].sort_values("seed")
            col = V[k + 1][2]
            rec(f"fig6_delta_{d}_{k}", per_seed=g.d_asr_pp.values, mean=g.d_asr_pp.mean(), sd=g.d_asr_pp.std(ddof=1))
            a2.bar(k, g.d_asr_pp.mean(), 0.5, color=col, alpha=0.25, edgecolor=col, lw=0.9, zorder=1)
            a2.errorbar(k, g.d_asr_pp.mean(), yerr=g.d_asr_pp.std(ddof=1), fmt="none", ecolor=col, elinewidth=1.5, capsize=4.5, capthick=1.5, zorder=3)
            for _, r in g.iterrows(): a2.scatter(k, r.d_asr_pp, marker=sc[int(r.seed)], s=32, color=col, edgecolor="white", linewidth=0.7, zorder=5)
            a2.text(k + 0.3, g.d_asr_pp.mean(), f"{g.d_asr_pp.mean():+.1f}", va="center", fontsize=7.0, fontweight="bold", color=col)
        a2.axhline(0, color="k", lw=0.8); a2.set_xlim(-0.55, 1.75)
        a2.set_xticks([0, 1]); a2.set_xticklabels(["no update\nvs Full", "no topology\nvs Full"], fontsize=7.0)
        a2.set_ylabel("Paired $\\Delta$ASR (pp)"); a2.grid(axis="x", visible=False)
    letter(axs[0, 0], "(a)", dx=-0.32); letter(axs[1, 0], "(b)", dx=-0.32)
    hs = [Line2D([], [], marker=sc[s], ls="", color="#555", mec="white", ms=6, label=f"seed {s}") for s in (42, 43, 44)]
    fig.legend(handles=hs, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=7.4)
    save(fig, "Fig6_controlled_ablation")


# ====================================================================== Fig 7: attacker weight
def fig7():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 3.0), sharey=True)
    fig.subplots_adjust(top=0.91, bottom=0.34, wspace=0.08, left=0.075, right=0.99)
    V = [("Full", "Full ETD-FGL", "#000000", "-", 1.5), ("Fixed No Update", "No update channel", "#0072B2", (0, (4, 1.6)), 1.4), ("Fixed No Topology", "No topology channel", "#D55E00", "-", 0.8)]
    for j, d in enumerate(DS):
        a = axs[j]
        a.axhline(20, color="#555", ls=":", lw=1.1, zorder=1)
        for key, lab, col, ls, lw in V:
            g = aw[(aw.dataset == d) & (aw.variant.str.startswith(key))].sort_values("round")
            rec(f"fig7_{d}_{key}", round=g["round"].values, w0=g.attacker_weight_pct.values)
            noisy = key == "Fixed No Topology"
            a.plot(g["round"], g.attacker_weight_pct, color=col, ls=ls, lw=lw, alpha=0.45 if noisy else 1, zorder=3)
            if noisy:
                a.plot(g["round"], g.attacker_weight_pct.rolling(5, center=True, min_periods=3).mean(), color=col, lw=1.9, zorder=4)
        a.set_ylim(0, 27); a.set_xlim(1, 50); a.set_title(d, loc="left", fontweight="bold", fontsize=8.8); a.set_xlabel("Communication round")
    axs[0].set_ylabel("Attacker weight $w_0$ (%)")
    hs = [Line2D([], [], color=c, ls=l, lw=1.6, label=lab) for _, lab, c, l, _ in V[:2]]
    hs += [Line2D([], [], color="#555", ls=":", lw=1.1, label="uniform share (20 %)"), Line2D([], [], color="#D55E00", lw=0.8, alpha=0.5, label="no topology: raw trace"), Line2D([], [], color="#D55E00", lw=1.9, label="no topology: 5-round moving average")]
    fig.legend(handles=hs, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=7.0, columnspacing=1.0)
    save(fig, "Fig7_attacker_weight_dynamics")


# ====================================================================== Fig S1: runtime (supplementary, exploratory)
def fig8():
    fig, axs = plt.subplots(1, 2, figsize=(W2, 3.6))
    fig.subplots_adjust(top=0.86, bottom=0.33, wspace=0.28, left=0.09, right=0.99)
    fig.text(0.5, 0.985, "Exploratory timing: single runs, hardware not recorded; not a basis for overhead or speed comparisons", ha="center", va="top", fontsize=7.4, color=RED, fontweight="bold")
    a = axs[0]
    for i, m in enumerate(METHODS):
        v = [b[(b.dataset == d) & (b.method == m)].active_loop_seconds.iloc[0] for d in DS]
        rec(f"fig8_{m}", seconds=v)
        a.bar(np.arange(3) + (i - 3.5) * 0.1, v, 0.092, color=COL[m], edgecolor="white", lw=0.4, label=LAB[m])
    a.set_yscale("log"); a.set_xticks(range(3)); a.set_xticklabels(DS); a.set_ylim(2, 1500); a.set_ylabel("50-round loop wall-clock (s)"); a.grid(axis="x", visible=False)
    a.set_title("(a) Seed-42 single runs", loc="left", fontweight="bold", fontsize=8.4)
    a.legend(ncol=3, fontsize=6.2, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    a = axs[1]
    g = rt[(rt.dataset == "Reddit") & (rt.slug == "fedavg_structural_backdoor")]
    ya = g.active_loop_seconds.values; xa = np.arange(len(ya))
    rec("fig8_reddit_attacked_fedavg_runs", seconds=ya)
    lab = [f"{r.suite.split('_')[0]} s{int(r.seed)}" for r in g.itertuples()]
    a.scatter(xa, ya, color=COL["Attacked FedAvg"], marker="X", s=34, edgecolor="white", linewidth=0.6)
    a.set_xticks(xa); a.set_xticklabels(lab, fontsize=6.4, rotation=40, ha="right"); a.set_ylabel("seconds")
    a.set_title("(b) Attacked FedAvg, Reddit: all stored runs", loc="left", fontweight="bold", fontsize=8.4)
    save(fig, "FigS1_runtime_exploratory", supp=True)


for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8):
    f()
(OUT / "plotted_data.json").write_text(json.dumps(PLOTTED), encoding="utf-8")
print("rendered", len(PLOTTED), "plotted series")
