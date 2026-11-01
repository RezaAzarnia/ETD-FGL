"""Fig 1: schematic of the ETD-FGL pipeline exactly as implemented at commit 80a3210
(multidata_suite/defenses.py ETDFGLAggregator; core.py run_method). No data, no performance claims."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

out = sys.argv[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42})
fig, ax = plt.subplots(figsize=(12, 5.6))
ax.set_xlim(0, 120)
ax.set_ylim(0, 56)
ax.axis("off")


def box(x, y, w, h, lines, fc, ec, fs=8.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center", fontsize=fs, linespacing=1.35)


def arr(x1, y1, x2, y2, c="#333", ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3, ls=ls))


box(1, 36, 24, 15, ["Clients 1-4 (benign)", "local GCN training", "(3 Adam epochs / round)", "graph unchanged"], "#eef3fa", "#4a6fa5")
box(1, 16, 24, 17, ["Client 0 (malicious, static)", "20% of non-target train nodes:", "label -> 0, K3 clique trigger", "(16 sparse features)", "otherwise honest training"], "#fbeeee", "#c0392b")
box(1, 1, 24, 11, ["Authenticated clean", "reference graphs G_i^0", "(simulation: read in memory)"], "#fff8e1", "#b7791f")
box(30, 36, 31, 15, ["Topology evidence (computed once)", "5-D label-free descriptor d(G): density,", "mean degree, norm. degree var.,", "avg clustering, triangles/node", "drift_i = ||(d(G_i)-d(G_i^0))/s||_2"], "#fff8e1", "#b7791f", 7.6)
box(30, 16, 31, 17, ["Update evidence (every round t)", "u_i = theta_i - theta_global", "dist_i = ||u_i - coord-wise median(u)||_2"], "#eaf6ec", "#2e7d32", 7.8)
box(30, 1, 31, 11, ["R(.) one-sided robust map:", "z = max((v-med)/max(1.4826 MAD, std, 1e-8), 0)", "A = clip(2(sigmoid(z)-0.5), 0, 1)"], "#f4ecf7", "#7b1fa2", 7.2)
box(64, 25, 27, 22, ["Risk fusion + trust", "R_i = 9/13 A_topo + 4/13 A_upd", "T_i = clip(exp(-3 R_i), 0.02, 1)", "w_i = n_i T_i / sum_j n_j T_j", "(n_i = # local train nodes)"], "#f4ecf7", "#7b1fa2", 7.6)
box(64, 4, 27, 16, ["Server model, then broadcast", "theta <- sum_i w_i theta_i", "evaluate each round on global", "clean + triggered graph;", "keep best clean-VALIDATION round"], "#e6f4fb", "#0288d1", 7.6)
box(96, 25, 23, 22, ["Logged per round", "(client 0 = attacker):", "A_topo, A_upd, R, T, w", "", "Table metrics: test acc,", "ASR, clean target rate,", "attack effect = ASR - CTR"], "#f7f7f7", "#666", 7.6)
arr(25, 43, 30, 43)
arr(25, 24, 30, 26)
arr(25, 8, 30, 38, "#b7791f", "--")
arr(45, 36, 45, 33.5, "#b7791f")
arr(45, 16, 45, 12.5, "#2e7d32")
arr(61, 6.5, 64, 33, "#7b1fa2")
arr(61, 41, 64, 41, "#b7791f")
arr(91, 36, 96, 36)
arr(77, 25, 77, 20.5)
ax.text(60, 54.6, "Simulation assumptions: K=5, M=1 attacker, IID class-stratified partition, server reads clean AND current client graphs; "
        "not a privacy-preserving deployment", fontsize=7.4, ha="center", style="italic", color="#444")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", "_preview.png"), dpi=140, bbox_inches="tight")
