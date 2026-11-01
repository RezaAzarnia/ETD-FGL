# Results and statistics (all recomputed from raw run files; CSVs in `TABLES/`)

Conventions: accuracy/ASR/CTR in %, attack effect = ASR − CTR in percentage points (pp); mean ± **sample SD (ddof=1) over n=3 seeds (42, 43, 44)**; runtime = 50-round loop wall-clock in seconds including per-round evaluation. Seeds 45/46 do not exist. No hypothesis test, CI, or multiplicity control was run. Independent recomputation agrees with the repository's own consolidated CSVs to <5·10⁻⁵.

## A. Seed-42 baseline comparison (single run per cell; no uncertainty) — `TABLES/R02`
| Dataset | Method | Acc | ASR | Effect | CTR | Time s |
|---|---|---|---|---|---|---|
| Cora | Clean FedAvg | 76.10 | 3.56 | −0.46 | 4.02 | 2.90 |
| | Attacked FedAvg | 74.20 | 48.05 | 40.34 | 7.70 | 2.88 |
| | PD-FL | 74.90 | 53.22 | 46.32 | 6.90 | 4.53 |
| | GSP-FL | 73.90 | 55.86 | 49.66 | 6.21 | 2.97 |
| | FLPurifier-GNN | 56.90 | 0.23 | −3.56 | 3.79 | 6.95 |
| | DMGNN-FL | 75.20 | 56.78 | 47.36 | 9.43 | 2.70 |
| | FedTGE | 76.80 | 82.87 | 73.91 | 8.97 | 177.03 |
| | **ETD-FGL** | 76.10 | 4.25 | 0.23 | 4.02 | 3.26 |
| PubMed | Clean FedAvg | 76.30 | 1.22 | −4.39 | 5.61 | 9.13 |
| | Attacked FedAvg | 75.30 | 17.68 | 11.22 | 6.46 | 11.40 |
| | PD-FL | 74.30 | 41.10 | 34.39 | 6.71 | 10.16 |
| | GSP-FL | 74.50 | 23.66 | 17.07 | 6.59 | 6.89 |
| | FLPurifier-GNN | 66.40 | 2.93 | −2.68 | 5.61 | 20.96 |
| | DMGNN-FL | 74.00 | 16.83 | 8.41 | 8.41 | 7.74 |
| | FedTGE | 71.30 | 79.27 | 66.71 | 12.56 | 773.29 |
| | **ETD-FGL** | 77.60 | 1.22 | −3.78 | 5.00 | 6.57 |
| Reddit | Clean FedAvg | 86.20 | 0.11 | −0.11 | 0.21 | 24.02 |
| | Attacked FedAvg | 85.70 | 72.29 | 72.08 | 0.21 | 44.60 |
| | PD-FL | 85.90 | 73.14 | 73.04 | 0.11 | 46.99 |
| | GSP-FL | 85.50 | 73.14 | 73.04 | 0.11 | 42.95 |
| | FLPurifier-GNN | 49.30 | 0.21 | −0.11 | 0.32 | 45.96 |
| | DMGNN-FL | 85.70 | 72.29 | 72.08 | 0.21 | 43.68 |
| | FedTGE | 52.70 | 4.78 | 4.46 | 0.32 | 399.94 |
| | **ETD-FGL** | 85.30 | 0.85 | 0.64 | 0.21 | 7.41 |
Observations [MEASURED]: ETD-FGL vs Clean FedAvg accuracy: Cora +0.00, PubMed +1.30, Reddit −0.90 pp (single seed). FLPurifier-GNN and FedTGE reach low ASR only on some datasets and lose 10–35 accuracy points or are far slower. DMGNN-FL Reddit outputs equal Attacked FedAvg (cause unverified). Runtime column is unreliable (§F).

## B. Multi-seed (n=3) — `TABLES/R03a/b`
| Dataset | Method | Acc | ASR | Effect | Time |
|---|---|---|---|---|---|
| Cora | Attacked FedAvg | 75.00±0.72 | 62.03±15.38 | 52.26±14.25 | 2.73±0.04 |
| | ETD-FGL | 75.57±1.57 | 5.21±0.88 | −2.22±2.17 | 2.85±0.01 |
| PubMed | Attacked FedAvg | 74.80±3.18 | 9.23±7.36 | 2.56±7.73 | 9.44±3.13 |
| | ETD-FGL | 75.50±2.01 | 0.89±0.56 | −3.54±0.53 | 10.53±3.64 |
| Reddit | Attacked FedAvg | 84.90±0.80 | 74.42±1.85 | 74.06±1.75 | 11.07±6.58 |
| | ETD-FGL | 84.87±0.40 | 14.08±18.19 | 13.77±18.09 | 7.40±0.05 |
Per-seed ETD-FGL ASR (42/43/44): Cora 4.25/5.98/5.40; PubMed 1.22/1.22/0.24; **Reddit 0.85/34.82/6.58**. Per-seed Attacked FedAvg ASR: Cora 48.05/59.54/78.51; PubMed 17.68/5.73/4.27; Reddit 72.29/75.69/75.27. No multi-seed Clean FedAvg. PubMed's unattacked-baseline ASR is already low (2 poisoned victim nodes); defence "success" there is small in absolute terms.

## C. Standard (renormalized) ablation — `TABLES/R04b` (ASR mean±SD; accuracy in file)
| Variant | Cora | PubMed | Reddit |
|---|---|---|---|
| Attacked FedAvg | 62.03±15.38 | 9.23±7.36 | 74.42±1.85 |
| Full ETD-FGL | 5.21±0.88 | 0.89±0.56 | 14.08±18.19 |
| Topology-only (1.0/0) | 4.60±0.90 | 0.81±0.39 | 10.44±16.08 |
| Update-only (0/1.0) | 44.33±8.02 | 6.50±9.37 | 31.49±17.73 |
| No trust (≡ Attacked) | 62.03±15.38 | 9.23±7.36 | 74.42±1.85 |
| Historical 3-channel | 18.93±3.80 | 1.14±0.87 | 21.87±16.33 |
Mean attacker share: Full 4.76/4.55/2.53 %; Topology-only 1.92 % (all datasets); Update-only 17.56/14.65/5.21 %. Topology-only is not worse than Full because its coefficient is inflated 9/13→1.0 [CODE]; differences are inside the SDs.

## D. Controlled ablation and paired differences — `TABLES/R05, R06`
| Dataset | Variant | ASR | Acc | w₀ % | benign R |
|---|---|---|---|---|---|
| Cora | Full | 5.21±0.88 | 75.57±1.57 | 4.76±0.03 | 0.0577 |
| | Fixed-No-Update | 6.40±1.59 | 75.87±1.56 | 4.12±0.00 | 0 (by construction) |
| | Fixed-No-Topology | 42.53±15.94 | 76.10±0.87 | 18.41±0.60 | 0.0610 |
| PubMed | Full / No-Upd / No-Top | 0.89±0.56 / 1.18±0.71 / 4.47±3.45 | 75.50 / 74.57 / 75.70 | 4.55 / 4.12 / 15.76 | 0.0487 / 0 / 0.0281 |
| Reddit | Full / No-Upd / No-Top | 14.08±18.19 / 25.19±17.81 / 66.31±7.14 | 84.87 / 85.00 / 85.27 | 2.53 / 4.12 / 13.24 | 0.0203 / 0 / 0.0223 |

Paired ΔASR (variant − Full; per seed 42/43/44; mean±SD):
| Dataset | Remove update | Remove topology |
|---|---|---|
| Cora | +0.80/+0.00/+2.76 → +1.19±1.42 | +21.84/+37.59/+52.53 → +37.32±15.35 |
| PubMed | +0.49/+0.24/+0.12 → +0.28±0.19 | +7.07/+2.32/+1.34 → +3.58±3.07 |
| Reddit | +7.11/+8.70/+17.52 → +11.11±5.60 | +57.22/+35.77/+63.69 → +52.23±14.61 |
Paired ΔClean-Acc: Cora +0.30±1.28 / +0.53±1.17; PubMed −0.93±1.27 / +0.20±2.10; Reddit +0.13±0.83 / +0.40±0.50. **Statistical status:** direction is consistent across seeds for topology removal (3/3 positive everywhere), for update removal on PubMed (3/3) and Reddit (3/3), but n=3, no test; the Cora update effect has one seed at exactly 0. Magnitudes are small except Reddit.

## E. Mechanism/provenance measurements — `TABLES/T14, R08, R10`
Attacker A_topo = 0.848284 (min=max) and benign A_topo = 0 in all 84 ETD-type runs; attacker update risk mean: Cora ≈0 (seeds 42,43), PubMed 0.02–0.05, Reddit 0.61–0.66. Fixed-No-Update attacker share = 4.117 % in every round. Fixed-No-Topology share fluctuates 10.6–25.0 % (exceeds the 20 % uniform share in some rounds). Round-1 ASR (seed 42): ETD-FGL Cora 75.4, PubMed 99.9, Reddit 0.4; Clean FedAvg 40.5, 61.2, 0.2; Attacked 100, 100, 3.7. ETD-FGL ASR ≥5 % in 30 (Cora) and 10 (PubMed) of 50 rounds; Reddit seed 42 max 3.2 %. Reddit seed 43 ASR trajectory ends at 37.8 % (round 50), best-validation checkpoint 34.82 %.

## F. Runtime — `TABLES/R11`
Single runs. Reddit Attacked FedAvg seed 42: 44.60 s (baseline suite), 18.66 s (multi-seed), 50.72 s (ablation/controlled suites); seeds 43/44: ≈7.2–10.8 s. ETD-FGL Reddit 7.3–7.4 s. Cora/PubMed Full ETD-FGL vs FedAvg differ by ≤1.3× within noise. Not hardware-documented (stored runs), no isolated aggregation timing ⇒ **no valid runtime-overhead or speed-up claim**; only "same order of magnitude as FedAvg on the evaluated runs" and "FedTGE ≥ 25× slower in these runs" are supportable.

## G. Unsupported / not run
Significance tests; CIs; 3-seed Clean FedAvg; seeds ≥45; non-IID; M≥2; other trigger sizes/poison rates; other GNNs; F1/AUC; isolated aggregation latency; hardware metadata for stored runs.
