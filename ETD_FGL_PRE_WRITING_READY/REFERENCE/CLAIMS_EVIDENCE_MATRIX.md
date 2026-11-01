# Claims–evidence matrix

Class: CODE FACT / EMPIRICAL (measured, raw logs) / INTERP (not isolated) / UNSUPPORTED. "Use" = may appear in the new manuscript. Code lines = branch HEAD 3084163.

| ID | Claim (proposed wording) | Class | Evidence (code; raw/table) | Use |
|---|---|---|---|---|
| C01 | The defense is a trust-weighted aggregation rule fusing topology drift and median-update distance | CODE FACT | `defenses.py:498-567` | yes |
| C02 | Descriptor is 5-D, label-free, computed on simplified undirected graphs | CODE FACT | `defenses.py:344-393`; tests | yes |
| C03 | R = 9/13 A_topo + 4/13 A_upd; T = clip(exp(−3R), 0.02, 1); w ∝ n_i T_i | CODE FACT | `:555-567`; logs reproduce (diff 1e-16) | yes |
| C04 | MAD term is max(1.4826·MAD, std, 1e-8); scale s_j = ddof-0 std with floor→1 | CODE FACT | `:450-454, :530-534` | yes |
| C05 | A_topo is computed once from exact clean reference graphs (simulation) | CODE FACT | `:518-533` | yes, with limitation |
| C06 | Attacker A_topo = 0.848284 in every run; benign A_topo = 0 | EMPIRICAL | `TABLES/T14` (84 runs) | yes (as limitation) |
| C07 | Topology evidence is therefore a binary reference-mismatch signal here | INTERP (follows from formula) | `EQUATIONS…` degenerate identity | yes, labelled |
| C08 | ETD-FGL reduces mean ASR: Cora 62.03→5.21, PubMed 9.23→0.89, Reddit 74.42→14.08 (±SD n=3) | EMPIRICAL | `R03b` | yes |
| C09 | Reddit seed 43 ASR = 34.82 % (effect 34.39 pp; attacker share 2.44 %); cause unknown | EMPIRICAL / cause UNSUPPORTED | `R03a`, `T14` | yes (no cause) |
| C10 | Community overlap/clustering explains seed 43 | UNSUPPORTED (contradicted: A_topo identical) | `T14` | **no** |
| C11 | ETD-FGL ASR <5 % from round 1 | UNSUPPORTED (false) | `R07`, `R10` | **no** |
| C12 | Seed-42 clean accuracy vs Clean FedAvg: +0.00 (Cora), +1.30 (PubMed), −0.90 pp (Reddit) | EMPIRICAL (single seed) | `R02` | yes |
| C13 | "Within 0.5 % of clean FedAvg" | UNSUPPORTED | `R02` | **no** |
| C14 | Multi-seed accuracy of ETD-FGL ≈ Attacked FedAvg within SD | EMPIRICAL | `R03b` | yes |
| C15 | Controlled ablation: removing topology raises ASR by +37.3/+3.6/+52.2 pp (3/3 seeds positive) | EMPIRICAL | `R06b` | yes (no "significant") |
| C16 | Removing update: +1.2/+0.3/+11.1 pp (Cora 2/3 seeds >0) | EMPIRICAL | `R06b` | yes, cautious |
| C17 | The update channel provides "vital stabilization" | UNSUPPORTED (mechanism not isolated; Cora ≈0 update risk) | `T14` | no; say "adds on Reddit" |
| C18 | Standard ablation under-estimates update channel due to coefficient inflation | CODE FACT + EMPIRICAL consistency | `ConfigurableETDFGLAggregator`, `R04b` vs `R05b` | yes (as explanation of design difference) |
| C19 | Attacker mean share 4.76/4.55/2.53 % (range per round 1.97–5.38 %) | EMPIRICAL | `R05b`, `R08` | yes |
| C20 | Attacker share ≤4.7 % | UNSUPPORTED | `R08` | no |
| C21 | Benign mean trust 0.86/0.88/0.95; minimum single-round 0.46 | EMPIRICAL | `R05b` | yes |
| C22 | Fixed-No-Update attacker share is exactly 4.117 % (saturation) | CODE FACT + EMPIRICAL | `EQUATIONS…`, `R05b` | yes |
| C23 | PubMed attack is weak (2 victims; Attacked ASR 9.23 %) | EMPIRICAL | `R12`, `R03b` | yes |
| C24 | FedTGE ≥25× slower in recorded loops | EMPIRICAL (single runs) | `R02` | cautious |
| C25 | ETD-FGL has <5 ms aggregation overhead | UNSUPPORTED | – | no |
| C26 | ETD-FGL is faster than FedAvg on Reddit | UNSUPPORTED | `R11` | no |
| C27 | DMGNN-FL uses GNNExplainer | UNSUPPORTED (false) | `defenses.py:229-288` | no |
| C28 | DMGNN-FL pruned zero edges on Reddit | UNSUPPORTED (not logged) | – | no |
| C29 | Baselines are adapted lightweight implementations, untuned | CODE FACT | `defenses.py:89-288`, `fedtge.py` | yes |
| C30 | Server never sees client edges / privacy-preserving | UNSUPPORTED (not implemented) | `:518-533` | no |
| C31 | Compatible with secure aggregation | UNSUPPORTED (needs plaintext updates) | code | no |
| C32 | Checkpoint chosen by clean validation accuracy (not ASR/test) | CODE FACT | `core.py:554` | yes |
| C33 | Partition is label-aware (uses all splits' labels) IID round-robin | CODE FACT | `data.py:247-287` | yes (disclose) |
| C34 | Evaluation on the full graph; training on induced subgraphs | CODE FACT | `core.py:114-127,199-221` | yes (disclose) |
| C35 | Robust to adaptive/colluding attackers, other triggers, non-IID | UNSUPPORTED (not tested) | – | no |
| C36 | Five-seed ablation with bootstrap CIs (seeds 42–46) | UNSUPPORTED (no raw data) | `new version.zip` summary only | no |
| C37 | Seed-42 "Best Round" column of old table | UNSUPPORTED (16/24 differ) | `R02` | recompute or omit |
| C38 | Paired ΔClean-Acc SDs of old table | UNSUPPORTED (non-reproducing) | `R06b` | use R06b |
