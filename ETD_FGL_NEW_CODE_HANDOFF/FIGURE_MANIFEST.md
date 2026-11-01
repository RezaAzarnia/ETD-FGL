# Figure manifest (code: branch HEAD `3084163`; results: raw runs produced under 80a3210)

| Slot | File | Script | Input | Seeds | Panels / units | Status | Caption guidance |
|---|---|---|---|---|---|---|---|
| 1 | `etdfgl_architecture_workflow.pdf` | `SCRIPTS/fig1_architecture_current.py` | none (schematic of the code) | – | pipeline boxes + equations | VERIFIED against code (minor: tight text in the R(.) box) | "ETD-FGL as implemented: static topology drift against an authenticated clean reference plus per-round median-update distance, fused 9/13 : 4/13 into exponential trust weights. The simulation assumes the server reads clean and current client graphs." |
| 2 | `overall_baselines.pdf` | `tools/raw_recompute/render_figures_from_tables.py` | `TABLES/R02` | 42 | (a) accuracy %, (b) ASR % | VERIFIED (single seed, no error bars) | "Seed-42 comparison of eight methods." |
| 3 | `accuracy_robustness_tradeoff.pdf` | same | R02 + R03a | 42; 42–44 mean ± SD | per-dataset accuracy (%) vs ASR (%); desirable region lower-right | VERIFIED | "Operating points per dataset; no cross-dataset frontier is claimed." |
| 4 | `multiseed_robustness.pdf` | same | R03a | 42, 43, 44 | accuracy, ASR; bars = mean, whiskers = sample SD, dots = seeds | VERIFIED (Reddit seed 43 annotated) | "Reddit seed 43 retains 34.82 % ASR (cause unexplained)." |
| 5 | `learning_dynamics_rounds.pdf` | same | R07 | 42 | per-round accuracy and ASR (Clean/Attacked FedAvg, FedTGE, ETD-FGL) | VERIFIED | "ETD-FGL's ASR is not near zero in early rounds on Cora/PubMed; unattacked FedAvg also shows high round-1 ASR." |
| 6 | `controlled_ablation.pdf` | same | R05a, R06a | 42–44 | ASR; paired ΔASR (pp) | VERIFIED | "n = 3 pairs; no significance test." |
| 7 | `attacker_weight_dynamics.pdf` | same | R08 | 42 | attacker weight % per round; 20 % uniform line | VERIFIED | "Full ETD-FGL stays within about 2–5.4 %; Fixed-No-Update is a constant 4.12 %." |
| 8 | `fig_s03_training_runtime_comparison.pdf` | same | R02 | 42 | seconds, log scale | VERIFIED WITH CAVEAT (single runs, unrecorded hardware, noisy) | Use descriptively or in the supplement only. |

Preview PNGs: `FIGURES/EXTRA/`. SHA-256: `README.md`. Old-manuscript figures are not reused. Not produced (no supporting data): graded-drift sensitivity, non-IID, multi-attacker, trigger-size sweep. Possible additions from existing logs: per-client A_topo/A_upd/trust over rounds (`TABLES/T14` summarizes them).
