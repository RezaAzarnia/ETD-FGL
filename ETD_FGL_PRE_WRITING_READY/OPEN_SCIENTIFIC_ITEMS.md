# Open scientific items (need experiments, new code, or author decisions)

Mandatory before strong claims (priority order)
| # | Item | Why | Smallest resolving step | Type |
|---|---|---|---|---|
| 1 | Reference-graph assumption | server reads exact clean graphs | author decision: keep as "oracle reference" limitation, or implement a reference-free drift (cross-client median / temporal) and rerun | decision + experiment |
| 2 | Degenerate topology evidence | attacker 0.848284 / benign 0 | add a benign-heterogeneity setting (Dirichlet non-IID exists in `data.py`) and a multi-attacker or graded-trigger test | experiment |
| 3 | Statistical support | n=3, no tests | ≥10 seeds for baseline, ETD-FGL, controlled ablation; report paired CIs | experiment |
| 4 | Reddit seed 43 | unexplained 34.82 % | log descriptor-level and partition statistics for Reddit seeds (inference only) or state as unexplained | analysis |
| 5 | Timing | not comparable | controlled repeated timing in one session with device logged (now recorded) and CUDA sync; otherwise drop runtime claims | experiment |
| 6 | Clean FedAvg multi-seed | only seed 42 | 6 short runs | experiment |
| 7 | Baseline fairness | untuned adapted baselines; clean-reference asymmetry | tune per-baseline or give each the same reference; label as adaptations | experiment/decision |
| 8 | Partition/evaluation protocol | label-aware partition; full-graph evaluation | label-blind partition variant; evaluate on induced client graphs or disclose | experiment/decision |
| 9 | DMGNN-FL pruning counts on stored runs | not logged | inference-only pass on stored checkpoints, or rerun with new logging | analysis |

Optional: trigger-size/poison-rate sweeps; other GNN backbones; adaptive attacker; privacy-preserving descriptor exchange; coefficient (9/13, 4/13, β=3, floor 0.02) sensitivity.
Unverifiable inputs: seeds 45/46 and the 5-seed bootstrap bundle (supply raw per-seed JSON/CSV if they should be used); an authentic referee letter (supply if one exists).
Already collected: everything in `TABLES/`; not collected: items 1–9 above.
