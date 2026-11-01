# Missing and unverified items (no values were guessed)

## Blocking for specific manuscript claims
| Item | Status | Consequence |
|---|---|---|
| Explanation of Reddit seed-43 residual ASR (34.82 %) | MISSING. Logs show attacker topology anomaly 0.8483 in every seed; no clustering/community/degree statistics were logged. Old "community overlap" explanation CONTRADICTED/UNSUPPORTED. | State as unexplained. |
| Clean FedAvg over 3 seeds | MISSING (only seed 42 exists) | "close to clean FedAvg" can be claimed for seed 42 only; "within 0.5 %" false (PubMed +1.30 pp). |
| Isolated aggregation latency ("<5 ms") | MISSING | Claim must be removed. |
| Fair runtime comparison | UNVERIFIED: same run timed 44.6/18.7/50.7 s in different suites; device/hardware not recorded in run files; venv torch is a CPU-only build | Runtime ranking unreliable. |
| DMGNN-FL pruning counts on stored runs | MISSING (not logged); DMGNN is an edge-ablation heuristic, not GNNExplainer | "Zero edges pruned / diffuse masks" unverified. |
| Statistical tests / CIs for ablations and baseline differences | NOT RUN (n=3) | No "significant" wording. |
| First-draft code version | PREVIOUS IMPLEMENTATION FOR THE EARLIEST DRAFT NOT AVAILABLE; Git has only 3 commits; old manuscript numbers equal HEAD results | Historical comparisons limited to 05f070a→953e250→80a3210. |
| Non-IID/Dirichlet, M≥2 attackers, other trigger sizes/poison rates, other GNNs, F1/AUC | NOT RUN (code for Dirichlet exists; no results) | Limitations only. |
| Descriptor-only (privacy-preserving) reference exchange | NOT IMPLEMENTED | Do not claim server never sees edges. |
| Software/hardware versions of the original runs | UNVERIFIED | Report as unknown. |

## Inconsistencies found
1. Old `tab:paired_contributions` ΔClean-Acc SDs do not reproduce (R13 row 6).
2. Old text: attacker weight 4.76 % (table) vs ≤4.7 % (captions/conclusion/architecture figure).
3. Old Fig 5 caption vs trajectories (round-1 ASR 75.4 %/99.9 %).
4. Old "Seed-43 attacker share 2.45 %" vs recomputed 2.44 % (mean over rounds).
5. Seed-42 timings differ between suites for byte-identical histories.
6. Earlier AI fact sheets in `paper_artifacts/` state Cora 5,429 edges / Reddit 24,710 edges and "GPU"; the run logs contain 10,556 / 135,224 PyG directed entries and no device — those fact-sheet values were not used.
7. `../main.tex` / `../main.pdf` in the parent folder belong to a different (IoT routing) paper.
8. Fig 1 (architecture) still contains false/unsupported box text (see FIGURE_MANIFEST).
