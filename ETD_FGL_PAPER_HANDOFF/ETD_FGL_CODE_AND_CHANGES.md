# ETD-FGL — Code, Changes, Verified Results and Manuscript Revision Map

Paper: *ETD-FGL: Evidence-Based Topological Defense for Federated Graph Learning Against Backdoor Attacks*.
Evidence base: repository commit `80a321027b26853eee1c2c4f415e1ec9c1f4961c` (branch `audit-fix-verification`, tag `paper-results-v1.0.0`). Tracked files are clean; only untracked figure-revision scripts/artifacts and this handoff exist.
Every number below was **recomputed by me from the 132 raw `outputs/**/final_summary.json` + `training_history.csv` files** (script `SCRIPTS/build_results.py`), not copied from earlier fact sheets. Earlier AI-written fact sheets in `paper_artifacts/` were used only as leads.

---

## START HERE (1-page summary for the manuscript editor)

**Which manuscript is "old"?** `../old/main.tex` (title, labels `tab:dataset_config … fig:runtime_figure` match your slot list). The file `../main.tex` + `../main.pdf` in the parent folder is a *different paper* (routing-aware IoT IDS) — ignore it. The HDQL-GTE Word report is not present and was not used. `old/main.tex` has no figure PDFs next to it; only 4 older PDFs exist in `manuscripts/etdfgl_snapshot_before_reassessment/images/etdfgl/`.

**Headline: the old manuscript's tables are numerically correct (nothing re-run changed them). What is wrong are several prose/caption claims and one table's ± values.**

| # | Fix required | Evidence |
|---|---|---|
| 1 | Remove "suppresses ASR to <5% from round 1" (Fig 5 caption, Sec 6.4). ETD-FGL seed-42 ASR at round 1 is **75.4 % (Cora), 99.9 % (PubMed)**; Cora spikes again at rounds 6 (40.5 %) and 12 (36.1 %). Only Reddit seed 42 stays <5 % in all rounds. | R07, R10 |
| 2 | Remove the causal story for Reddit seed 43 ("high community clustering overlap attenuates topological drift"). Logged attacker topology anomaly is **0.8483 in all 9 multi-seed runs**, including seed 43; no clustering/community statistic was logged. Report 34.82 % as an unexplained seed-dependent residual. | R03a, raw histories |
| 3 | Abstract "within 0.5 % of unattacked FedAvg" is false: seed-42 gaps vs Clean FedAvg are Cora +0.00, PubMed **+1.30**, Reddit −0.90 pp; no 3-seed Clean FedAvg exists. | R02 |
| 4 | "≤4.7 %" (Fig 7 caption, conclusion, architecture figure) contradicts Table 6's 4.76 %. Per-round Full-ETD-FGL attacker weight: Cora 4.39–5.00 %, PubMed 2.84–5.38 %, Reddit 1.97–4.91 %. Use "mean 4.76 / 4.55 / 2.53 %". | R05b, R08 |
| 5 | "<5 ms aggregation overhead" is unsupported (no isolated aggregation timing was recorded). Remove. | `core.py` timing |
| 6 | Runtime table: same algorithm/seed (Attacked FedAvg, Reddit seed 42) was timed at 44.6 s, 18.7 s and 50.7 s in different suites, while seeds 43/44 take ~7–10 s. "ETD-FGL 7.4 s vs FedAvg 44.6 s" is a timing artifact, not a speedup. | R11 |
| 7 | `tab:paired_contributions` ΔClean-Acc ± values do not reproduce (see Sec. 6.4); replace with R06b values. | R06b |
| 8 | "near-total elimination" (conclusion) and "ideal upper-left Pareto frontier" (Fig 3) must go; desirable region is lower-right; no pooled cross-dataset frontier. | R03b |
| 9 | DMGNN-FL: description "GNNExplainer saliency masks" is wrong for this code (it is a leave-one-edge-out probability-drop heuristic, threshold 0.02); the claim "zero edges pruned on Reddit" is unverified (pruning counts not logged). | `defenses.py:229-290` |
| 10 | Benign trust ">85 %" holds only as a mean over rounds (0.858/0.880/0.949); single-round benign trust drops to 0.46–0.49. | R05b |

**Figures:** 7 of 8 regenerated figures are data-valid (slots 2–8); slot 1 (architecture) is *not camera-ready* (see `FIGURE_MANIFEST.csv`). **Largest scientific caveat the paper should state:** the topology channel is effectively an oracle in this setup — benign clients have drift exactly 0 and the single attacker's anomaly is a constant 0.8483 independent of trigger magnitude (K=5, M=1 scale invariance), so topology results do not show graded detection.

### 200–400-word editorial overview (English)

ETD-FGL is a server-side, trust-weighted aggregation defense for federated node classification under a static structural backdoor. In each of 50 synchronous rounds, five clients train a 2-layer GCN locally (3 Adam epochs); one client (client 0) holds a poisoned graph in which 20 % of its non-target training nodes were each given a 3-node clique trigger with a fixed 16-feature sparse vector and relabeled to target class 0. The server combines two evidence streams. The first is a static topology anomaly: a label-free five-coordinate descriptor (density, mean degree, normalized degree variance, average clustering, triangles per node) is computed for every client's current graph and for an authenticated clean pre-attack reference; the Euclidean distance between them, standardized per coordinate across clients, is mapped by a one-sided median/MAD sigmoid to [0,1]. The second is a per-round update anomaly: the distance of each client's parameter update to the coordinate-wise median update, mapped through the same transform. Risk is fused as 9/13 topology + 4/13 update, converted to trust exp(−3R) clipped to [0.02, 1], and multiplied by training-node counts to give aggregation weights. Across seeds 42–44, mean ASR falls from 62.03±15.38 to 5.21±0.88 % (Cora), from 9.23±7.36 to 0.89±0.56 % (PubMed; weak attack, only two poisoned nodes) and from 74.42±1.85 to 14.08±18.19 % (Reddit, with seed 43 at 34.82 %), with clean accuracy within seed noise of attacked FedAvg. Controlled fixed-coefficient ablations indicate that removing the topology channel largely restores the attack (paired ΔASR +37.3, +3.6, +52.2 pp), whereas removing the update channel adds +1.2, +0.3, +11.1 pp; with three seeds no significance test was run. Important limits: the reference graph is simulated by exact access to clean client graphs, benign topology drift is exactly zero, the attacker's topology anomaly saturates at a constant, only one attacker/IID partition/one trigger/one architecture were tested, baselines are lightweight adaptations, and runtime values are single-run wall-clock times without isolated aggregation timing.

---

## 1. Executive technical summary

* **Input/Output.** Input: K=5 client graphs (features, edges, labels), clean reference graphs (simulation), local model updates each round. Output: a global GCN; per-round diagnostics (topology/update risk, fused risk, trust, weight per client).
* **Threat model (as implemented).** One malicious client (id 0), static offline poisoning before round 1, victims = ceil(0.2 × non-target train nodes of client 0), label flip to class 0, K3 clique attached bidirectionally to each victim, trigger nodes carry one fixed sparse feature vector (16 active features, L2 norm = median clean row norm) and label 0 but are *not* in the train mask. No model replacement/scaling.
* **Contribution.** Fusion of authenticated-reference topology drift with round-wise update anomaly into a soft trust weight; controlled-coefficient ablation methodology.
* **What changed vs the manuscript.** Results: nothing (old tables = recomputed values). Claims: see START HERE. Code (Git-traceable): see Sec. 3.
* **Superseded/invalid old items:** all items marked CONTRADICTED/REVISE in `RESULTS/R13_old_manuscript_vs_verified.csv`.

## 2. Code architecture and traceability

All paths relative to repo root; line numbers at `80a3210`.

| Component | File : symbol | Inputs → Outputs | Role | Evidence |
|---|---|---|---|---|
| Config | `multidata_suite/config.py:6-54` `DatasetConfig` | – | K=5, 50 rounds, 3 local epochs, hidden 32, lr 0.01 (Cora/PubMed) / 0.005 (Reddit), wd 5e-4, dropout 0.5, poison 0.20, trigger 3, target 0, malicious id 0, Reddit sample 8000 seed 42 | in every `final_summary.json` |
| Dataset loader | `data.py:89` `load_dataset` | Planetoid public split (Cora, PubMed) with `NormalizeFeatures`; Reddit: class-stratified 8,000-node induced subgraph cached `.pt` | graph | R12 |
| Partitioner | `data.py:247` `create_partition` (strategy `iid`) | graph → 5 node sets | label- and split-aware round-robin per (split,class): every node (incl. val/test) assigned to exactly one client, client subgraph = induced subgraph (cross-client edges dropped). Dirichlet variant exists (`create_dirichlet_partition`) but **no Dirichlet result exists** | `partition_metadata.strategy = iid` in all 132 runs |
| Poison/trigger injection | `attack.py:80` `inject_clique_trigger`; `make_sparse_trigger_prototype` | client-0 graph | see Sec. 1 | `attack_metadata` |
| Evaluation trigger | `attack.py` `attach_evaluation_triggers`; `core.py:114-127` | global graph + all non-target **test** nodes | one triggered graph with K3 attached to every victim test node simultaneously | `core.py` |
| Clean-reference capture | `run_real_dataset_pipeline.py` passes `context.clean_graphs_cpu` and `attacked_graphs_cpu` to `ETDFGLAggregator` | in-memory PyG objects | **simulation-only**: server reads full client graphs | `defenses.py:497-512` |
| 5-D descriptor | `defenses.py:322-371` `_graph_descriptor` | PyG `Data` → R^5 | density, mean degree, Var(d)/(mean²+1e-12) (population variance), `nx.average_clustering` (degree<2 nodes count as 0), triangles/|V| | verified |
| Drift + topology anomaly | `defenses.py:506-511` | descriptors | per-coordinate scale = population std (ddof=0) of the 5 clean descriptors (<1e-8 → 1.0); drift = ‖(cur−clean)/scale‖₂; then `_robust_positive` | verified |
| One-sided robust map | `defenses.py:428-432` `_robust_positive` | vector of K scores | see Sec. 4 | verified |
| Update distance | `defenses.py:527-532` | flattened deltas of all parameters vs previous global state | coordinate-wise median (torch.median, K=5 odd) and L2 distance → `_robust_positive` | verified |
| Risk fusion/trust/aggregation | `defenses.py:533-545` `ETDFGLAggregator.__call__` | – | R, T, w, weighted average of states | verified |
| Standard ablation | `defenses.py:548-663` `ConfigurableETDFGLAggregator` (weights renormalized to sum 1) | – | variants set in `run_extended_experiments.py:402-405` | – |
| Controlled ablation | `multidata_suite/controlled_ablation.py` `ControlledAblationETDFGLAggregator` (un-normalized fixed coefficients); runner `run_controlled_ablation.py` | – | Full / Fixed-No-Update / Fixed-No-Topology | – |
| Baselines | `defenses.py`: `PDFLAggregator:89`, `purify_gsp:111`, `make_flpurifier_trainer:144`+`FLPurifierAggregator:198`, `purify_explanation_guided:229`; `multidata_suite/fedtge.py` | – | see Sec. 8 fidelity notes | – |
| Runner | `run_real_dataset_pipeline.py` (8 methods, seed 42), `run_extended_experiments.py` (`multiseed`, `ablation`), `multidata_suite/core.py:411` `run_method` | – | training loop, per-round evaluation, validation-based checkpoint | – |
| Metrics | `core.py:158-179` `evaluate` | – | test acc, clean target rate, ASR, attack effect | – |
| Aggregation of results | `extract_and_consolidate_results.py`, `build_publication_tables.py` (HEAD) | raw JSON/CSV | publication CSV/TeX tables (ddof=1) | matches my recomputation |
| Figure generators | `generate_publication_figures.py` (committed, v1 PDFs), `build_figure_revision_v2/v3/v4.py` (untracked, PNG only) | – | superseded here by `SCRIPTS/make_figures.py` | – |
| Logging | `training_history.csv` (50 rows/run), `final_summary.json`, `experiment_manifest.json` (SHA-256 of history/checkpoint) | – | – | – |

Evidence status: raw results live in `outputs/` which is **git-ignored** (0 tracked files) — provenance is on-disk only, protected by per-run manifests.

## 3. Actual code changes (before → after)

Git has three commits. The old manuscript's numbers equal the HEAD results, so **no experimental result was invalidated by these changes after the results were produced**. Whether the *first* manuscript draft (`manuscripts/etdfgl_snapshot_before_reassessment/main.tex`, Oct 15) was written against another commit is not documented → **PREVIOUS IMPLEMENTATION FOR THE EARLIEST DRAFT NOT AVAILABLE** (I did not diff that draft).

| Change | Commit | Old | New | Result impact |
|---|---|---|---|---|
| Descriptor | `05f070a`→`953e250` (`defenses.py:273-405`) | 6-D including **label-dependent homophily** (uses `train_mask`,`y`) | 5-D label-free; homophily moved to diagnostic function `compute_homophily_diagnostics` (never used in risk) | Material. Old 6-D results (if any existed) are not in the repo; all current results use 5-D. |
| Constants/metadata | `953e250` | – | `ALPHA_TOPOLOGY=9/13`, `ALPHA_UPDATE=4/13`, `ALPHA_EXPLANATION=0`, `DESCRIPTOR_VERSION="topology_5d_label_free_v1"` | none |
| Aggregator dispatch | `80a3210` `core.py:378` | `try/except TypeError` fallback | signature inspection, errors propagate | none (per `audit/FIX_CHANGELOG.md`) |
| FedTGE | `80a3210` `fedtge.py` | silent all-ones energy fallback; docs said hidden=16 | strict validation; metadata says hidden=32 (runtime model was already 32); edge-augmentation mode documented | audit states no rerun needed ("verified not triggered") |
| DMGNN diagnostics | `80a3210` | no logging | logs removed-edge count to stdout/graph attribute (not saved in run summaries) | pruning counts for stored runs remain unknown |
| Fail-closed overwrite, partition cache validation, manifests | `80a3210` | overwrite allowed | refuses overwrite without `--force`; SHA-256 manifest | none |
| Controlled ablation + consolidation + figure/table scripts | `80a3210` | – | new | produces `controlled_ablation_v1` results |

Cosmetic: docs, tests (`test_audit_regressions.py`, 26 tests), CI workflow. Not independently executed by me.

## 4. Exact currently implemented method (verified against code)

Notation: K=5 clients, client graphs simplified to undirected simple graphs (self-loops removed, duplicates collapsed) before the descriptor.

**Descriptor** `d(G)=[ρ, k̄, Var_norm, C̄, τ]`: ρ=2|E|/(|V|(|V|−1)); k̄=mean degree; Var_norm = (1/|V|)Σ(d_v−k̄)² / (k̄²+10⁻¹²); C̄=mean local clustering with zeros for d_v<2 (networkx default); τ = (#triangles)/max(1,|V|).

**Drift:** s_j = std_i[d_j(G_i^clean)] (ddof=0; set to 1 if <10⁻⁸); Δ_i = ‖(d(G_i^cur) − d(G_i^clean)) ⊘ s‖₂.
**Robust one-sided map R(v):** m=median(v); MAD=max(1.4826·median|v−m|, std(v), 10⁻⁸) — note it is a **max of MAD and std (not a fallback)**; z_i=max((v_i−m)/MAD,0); R_i = clip(2(σ(z_i)−0.5),0,1). A_topo = R(Δ) computed once (static, constructor); A_upd^t = R(‖u_i^t − median_j u_j^t‖₂), u_i^t = θ_i^t − θ^{t-1} (all parameters flattened).
**Fusion/trust/aggregation:** R_i^t = (9/13)A_topo,i + (4/13)A_upd,i^t; T_i^t = clip(exp(−3R_i^t), 0.02, 1); w_i^t = n_i T_i^t / Σ n_j T_j^t, n_i = number of training nodes (labelled train mask) of client i; θ^t = Σ w_i θ_i (non-float buffers copied). **Still used:** 9/13, 4/13, exp(−3R), floor 0.02, K=5. Explanation channel weight 0 (GNNExplainer not in the defense path).
**Checkpoint:** global model evaluated every round; the stored/reported model is the round with the highest *clean validation accuracy* (strict `>`, first maximum); ASR is not used for selection.
**Consequence of K=5, M=1 (derived, and confirmed in all logs):** if benign drifts are exactly 0 and attacker drift d≥2.5·10⁻⁸ then z₀=2.5, A_topo,0 = 0.848284 regardless of d; T₀=exp(−3·(9/13)·0.848284)=0.1717; with equal n_i attacker weight = 4.117 % (Fixed-No-Update: exactly 4.12 %, SD 0.00 in all 9 runs).
**Standard ablation semantics** (`ConfigurableETDFGLAggregator`, weights renormalized to sum 1, trust strength 3): Topology-only → R=A_topo (coefficient 9/13→1.0); Update-only → R=A_upd; No-trust → uniform n_i-weighted FedAvg (numerically identical to Attacked FedAvg, confirmed); Historical 3-channel → 0.45 topology / 0.35 explanation (GNNExplainer score) / 0.20 update.
**Controlled ablation semantics:** coefficients kept un-normalized: Fixed-No-Update R=(9/13)A_topo; Fixed-No-Topology R=(4/13)A_upd; Full as production. Same trust map.

## 5. Experiment protocols and provenance

* **Datasets (logged):** Cora 2,708 nodes / 10,556 directed edge entries; PubMed 19,717 / 88,648; Reddit sample 8,000 / 135,224 (PyG directed entries; undirected = half). Features/classes (1,433/7, 500/3, 602/41) are standard PyG values, not logged in run files. Reddit: fixed class-stratified sample (seed 42) of the PyG Reddit graph, test/val capped at min(1000, 1000, 8000/8) → 1,000/1,000 nodes, train 6,000.
* **Splits:** Planetoid public (Cora train 140 / val 500 / test 1,000; PubMed 60/500/1,000 — client-level counts in R12: Cora 28/100/200 per client; PubMed 12/100/200; Reddit 1200/200/200). Evaluation and checkpoint selection use the **global graph with global val/test masks**.
* **Partition:** IID class-stratified round-robin only; no Dirichlet/non-IID result exists.
* **Attack:** 1 attacker of 5, ρ=0.20, K3, target class 0; victims: **Cora 5, PubMed 2, Reddit 227** nodes (R12). Trigger feature norm: Cora ≈0.22, PubMed ≈0.19, Reddit ≈18.5–18.8.
* **Training:** 2-layer GCN (hidden 32, dropout 0.5), Adam, 3 full-batch local epochs/round, 50 rounds, lr/wd above. Seeds 42/43/44 change partition, victim choice, trigger feature indices and init; Reddit sample fixed.
* **Metrics:** accuracy = test accuracy on clean global graph; clean target rate (CTR) = fraction of non-target test nodes predicted class 0 without trigger; ASR = same with triggers attached to all of them simultaneously (isolated single-victim evaluation was not done); attack effect = ASR − CTR (pp). Attacker share = mean over the 50 rounds of w₀ (not the best-round value); benign risk = mean over rounds of mean fused risk of clients 1–4. Runtime = `time.perf_counter` over the 50-round loop (local training + aggregation + per-round evaluation; excludes data loading/reference prep).
* **Uncertainty:** mean ± sample SD (ddof=1) over n=3 seeds (extraction code `ddof=1`; I reproduced). Paired comparisons (ablation Δ) are within-seed; baseline comparisons across methods in Seed-42 table are single-run.
* **Hardware/software:** device not recorded in run files (`core.py` uses CUDA if available). Current project venv: torch 2.14.1+cpu (CPU-only build), torch_geometric 2.8.1, scikit-learn 1.9.1, gudhi 3.13.0, networkx 3.6.1, numpy 2.4.6; `nvidia-smi` lists an RTX 2060 SUPER on this machine. Neither proves what the runs used → device and versions of the actual runs are UNVERIFIED.
* **Reference graph vs practical server:** server uses exact clean graphs; not available to a real server (limitation). Secure aggregation incompatible (needs plaintext updates).
* **Seed-42 reuse:** multiseed/ablation/controlled seed-42 histories are byte-identical to the baseline-suite runs but `elapsed_seconds` differ, so I cannot tell whether they were re-executed or copied; metrics identical either way.

## 6. VERIFIED current results (all recomputed; ASR/acc in %, effect in pp)

Sources: R01 (all 132 runs, with file path + summary hash), R02–R06 below. **n=3 seeds; ± = sample SD.**

### 6.1 Seed-42 baselines (`tab:seed42_baselines`; R02) — identical to old table
Cora: Clean FedAvg 76.10/3.56/−0.46/2.90 s; Attacked 74.20/48.05/40.34/2.88; PD-FL 74.90/53.22/46.32/4.53; GSP-FL 73.90/55.86/49.66/2.97; FLPurifier 56.90/0.23/−3.56/6.95; DMGNN 75.20/56.78/47.36/2.70; FedTGE 76.80/82.87/73.91/177.03; **ETD-FGL 76.10/4.25/0.23/3.26**. PubMed: ETD-FGL 77.60/1.22/−3.78/6.57 vs Attacked 75.30/17.68/11.22/11.40 (FedTGE 71.30/79.27/66.71/773.29). Reddit: ETD-FGL 85.30/0.85/0.64/7.41 vs Attacked 85.70/72.29/72.08/44.60; FLPurifier 49.30/0.21; FedTGE 52.70/4.78/4.46/399.94; DMGNN row identical to Attacked FedAvg. Best rounds in R02. (Clean FedAvg Cora ASR 3.56 % with clean target rate 4.02 %.)

### 6.2 Multi-seed (`tab:multiseed_robustness`; R03a/b)
| Dataset | Method | Acc | ASR | Effect | Time s |
|---|---|---|---|---|---|
| Cora | Attacked | 75.00±0.72 | 62.03±15.38 | 52.26±14.25 | 2.73±0.04 |
| Cora | ETD-FGL | 75.57±1.57 | 5.21±0.88 | −2.22±2.17 | 2.85±0.01 |
| PubMed | Attacked | 74.80±3.18 | 9.23±7.36 | 2.56±7.73 | 9.44±3.13 |
| PubMed | ETD-FGL | 75.50±2.01 | 0.89±0.56 | −3.54±0.53 | 10.53±3.64 |
| Reddit | Attacked | 84.90±0.80 | 74.42±1.85 | 74.06±1.75 | 11.07±6.58 |
| Reddit | ETD-FGL | 84.87±0.40 | 14.08±18.19 | 13.77±18.09 | 7.40±0.05 |

Per-seed ETD-FGL ASR: Cora 4.25/5.98/5.40; PubMed 1.22/1.22/0.24; Reddit 0.85/**34.82**/6.58. Attacked FedAvg: Cora 48.05/59.54/78.51; PubMed 17.68/5.73/4.27; Reddit 72.29/75.69/75.27. Seed-43 Reddit: acc 84.50, attacker share 2.44 % (final round 2.16 %), attack effect 34.39 pp. In the seed-43 trajectory ASR *rises* to 37.8 % at round 50.

### 6.3 Standard ablation (R04b; ASR mean±SD, 3 seeds; full table incl. accuracy in file)
Cora: Full 5.21±0.88; Topology-only 4.60±0.90; Update-only 44.33±8.02; No-trust 62.03±15.38 (= Attacked); Historical 3-ch 18.93±3.80. PubMed: 0.89±0.56; 0.81±0.39; 6.50±9.37; 9.23±7.36; 1.14±0.87. Reddit: 14.08±18.19; 10.44±16.08; 31.49±17.73; 74.42±1.85; 21.87±16.33. Interpretation: Topology-only is not worse than Full under renormalization (coefficient 9/13→1.0); differences are within the large SDs.

### 6.4 Controlled ablation (R05b) and paired differences (R06b)
| Dataset | Variant | ASR | Attacker w₀ % | Benign risk |
|---|---|---|---|---|
| Cora | Full | 5.21±0.88 | 4.76±0.03 | 0.0577±0.0007 |
| Cora | No-Update (9/13) | 6.40±1.59 | 4.12±0.00 | 0 (by construction) |
| Cora | No-Topology (4/13) | 42.53±15.94 | 18.41±0.60 | 0.0610±0.0032 |
| PubMed | Full / No-Upd / No-Top | 0.89±0.56 / 1.18±0.71 / 4.47±3.45 | 4.55±0.04 / 4.12 / 15.76±0.59 | 0.0487 / 0 / 0.0281 |
| Reddit | Full / No-Upd / No-Top | 14.08±18.19 / 25.19±17.81 / 66.31±7.14 | 2.53±0.08 / 4.12 / 13.24±1.03 | 0.0203 / 0 / 0.0223 |

Paired ΔASR (variant−Full), per seed 42/43/44: Cora remove-update +0.80/+0.00/+2.76 (mean +1.19±1.42); remove-topology +21.84/+37.59/+52.53 (+37.32±15.35). PubMed remove-update +0.49/+0.24/+0.12 (+0.28±0.19); remove-topology +7.07/+2.32/+1.34 (+3.58±3.07). Reddit remove-update +7.11/+8.70/+17.52 (+11.11±5.60); remove-topology +57.22/+35.77/+63.69 (+52.23±14.61). **Corrected ΔClean-acc SDs:** Cora remove-update +0.30±1.28, remove-topology +0.53±1.17; PubMed −0.93±1.27 / +0.20±2.10; Reddit +0.13±0.83 / +0.40±0.50 (old table printed 0.56/1.63/1.25/0.46/0.50/0.56). **No test, CI or multiple-comparison control was run (n=3); do not write "statistically significant".** Note the Cora remove-update effect includes a seed with exactly 0.00 and PubMed's effect is < 0.5 pp — treat as not distinguishable from zero.

### 6.5 Attacker suppression / early rounds / runtime
Attacker share: see 6.4; uniform baseline 20 %. Fixed-No-Update is a fixed 4.12 % in every round/seed (saturation artifact, not an adaptive measurement). ASR trajectories and first-round values: R07, R09, R10. Runtime: R11 (same method varies 2.5× across suites on Reddit).

**Not available (MISSING):** F1/precision/recall/AUC, per-class results, 3-seed Clean FedAvg, >3 seeds, CIs/tests, non-IID, M≥2 attackers, trigger-size/poison-rate sweeps, isolated aggregation latency, ETD-FGL on GAT/SAGE.

## 7. Manuscript revision map (`old/main.tex`)

| Location | Action | Replacement-ready statement (evidence-backed) |
|---|---|---|
| Abstract | REVISE | Replace "within 0.5 % of unattacked FedAvg" with: "On the single seed with an unattacked reference (seed 42), clean accuracy differs from Clean FedAvg by +0.00, +1.30 and −0.90 pp (Cora, PubMed, Reddit); over three seeds it tracks attacked FedAvg within seed variance." Remove "heavy-tailed community overlap". Say residual ASR on Reddit seed 43 (34.82 %) is unexplained. |
| Sec 3.2 (threat model) | REVISE | State: victims' labels are set to 0; trigger nodes are appended with label 0 but are not in the training mask; victims per client 0: 5/2/227. |
| Sec 4.1 Eq. `eq:topo_drift`, `s_j` | REVISE | "s_j is the population standard deviation across clients' clean descriptors; set to 1 if <10⁻⁸" (old text `max(Std,10⁻⁸)` is wrong). |
| Eq. `eq:robust_scaling` | KEEP | MAD term is max(1.4826·MAD, Std, 10⁻⁸). |
| Sec 4 end | ADD | Note A_topo is computed once, depends on an authenticated exact reference and, for K=5/M=1, saturates at 0.8483. |
| `tab:dataset_config` | KEEP | Label edge counts as directed edge entries; add victim counts and per-client splits (R12). |
| Baseline list (Sec 5.2) | REVISE | Describe the implemented adaptations (Sec. 8 below), not the original papers. |
| `tab:seed42_baselines`, `tab:multiseed_robustness` | KEEP | Values verified. Add "single run" / "n=3". |
| Sec 6.1 DMGNN failure analysis | REVISE | "DMGNN-FL's outputs on Reddit are identical to Attacked FedAvg; edge-removal counts were not logged, so the mechanism is unverified." |
| Fig 3 + Sec 6.2 "Pareto" | REVISE | "Operating points per dataset; lower-right is desirable." Delete "Pareto frontier". |
| Sec 6.3 seed-43 paragraph (items 1–2) | REMOVE | Keep only: "Seed 43 on Reddit retains 34.82 % ASR (attack effect 34.39 pp; attacker share 2.44 %); we have no logged evidence explaining it. Attacker topology anomaly was 0.8483 in all seeds." The "40.87-point reduction" figure (75.69 − 34.82 = 40.87) is arithmetically right and may stay. |
| Fig 5 caption + Sec 6.4 | REVISE | "ETD-FGL's ASR is not suppressed at round 1 (Cora 75.4 %, PubMed 99.9 %, seed 42) and remains ≥5 % in 30 of 50 rounds on Cora and 10 of 50 on PubMed; on Reddit seed 42 it stays below 3.2 % throughout." Final reported metrics are best-validation checkpoints. |
| `tab:ablation_comparison` | KEEP | Verified; add that standard variants renormalize and No-trust ≡ Attacked FedAvg. |
| `tab:paired_contributions` | REVISE | Use R06b SDs (Sec 6.4); add per-seed values; say n=3, no test. |
| Fig 6 caption "+52.2 %" | REVISE | "pp", not "%"; delete "significantly". |
| `tab:attacker_suppression` + Sec 6.5 | KEEP/REVISE | Table OK; text: "mean attacker share 4.76/4.55/2.53 %; benign mean trust 0.86/0.88/0.95 (single-round minimum ≈0.46)". Note Fixed-No-Update 4.12 % is saturation. |
| Fig 7 caption | REVISE | Delete "≤4.7 %". |
| Sec 6.7 runtime | REVISE | Delete "<5 ms"; add "single-run wall-clock incl. evaluation; same method varied 7–51 s across suites on Reddit; no isolated aggregation timing". |
| `tab:runtime_comparison`/Fig 8 | REVISE | Keep numbers but caveat; do not claim ETD-FGL faster than FedAvg. |
| Discussion §"Seed 43" | REMOVE | Remove "highlighting the necessity of multi-channel defense" as causal support. |
| Limitations | ADD | topology channel benign drift = 0; exact reference; M=1; IID only; one trigger; 3 seeds; PubMed attack has 2 poisoned nodes; baselines adapted; secure aggregation. Existing 5 items KEEP. |
| Conclusion | REVISE | Replace "near-total elimination" with: "reduced mean ASR to 5.21 %, 0.89 % and 14.08 % (Reddit seed 43: 34.82 %)"; delete "≤4.7 %". |
| Fig 1 | REVISE | Redraw (Sec FIGURE_MANIFEST). |

Updated captions/column definitions: attacker weight column = mean over 50 rounds of w₀ (%); benign risk = mean over rounds of mean R of clients 1–4; ± = sample SD (ddof=1); runtime = 50-round loop incl. evaluation.

## 8. Scientific consistency and limitation checks

| Check | Outcome |
|---|---|
| Reddit seed 43 ASR 34.82 % | **Confirmed** (R03a). Not hidden. Cause unexplained; old causal story contradicted. |
| Table 6 Cora 4.76 % vs "≤4.7 %" | **Persists**; fix text (Sec. 7). |
| Fig 3 "upper-left" / Pareto | **Wrong**; lower-right; no pooled frontier. |
| Fig 5 "from round 1" | **False** for Cora/PubMed (R10). |
| Standard vs controlled ablation | Keep separate. Standard renormalizes (9/13→1.0); controlled holds coefficients. No significance analysis exists. |
| Near-total elimination | Not supported (Reddit 14.08±18.19; seed 43 34.82). |
| PubMed context | Weak attack: Attacked FedAvg ASR 9.23±7.36 %, only 2 poisoned victim nodes; Clean-FedAvg ASR already 1.22 %. ETD-FGL "success" there is small in absolute terms. Attack effect values of −3 to −4 pp show ETD-FGL ASR below clean target rate. |
| Baseline fidelity | **PD-FL**: IsolationForest on a 24×24 cubical-persistence signature of the update (+ 5 norm stats), trust sigmoid floored at 0.03 — an adaptation, not the original system; calibrated on clean updates of 4 rounds. **GSP-FL**: prunes 12 % of edges per client by spectral-embedding distance (rank 20) before FedAvg. **FLPurifier-GNN**: conv1 averaged by n_i, conv2 weighted by cosine-to-median similarity (floor 0.05), contrastive local trainer; accuracy collapses (49–67 %). **DMGNN-FL**: leave-one-edge-out drop of target-class probability for ≤8 most target-confident train nodes (≤12 edges each, threshold 0.02), uses the Attacked-FedAvg checkpoint; not GNNExplainer. **FedTGE**: adapted from the official repo (commit `e80950c`), hidden 32, 3 supervised epochs; very slow and unstable here (ASR 82.9/79.3 % on Cora/PubMed; per-round test accuracy ≈35–50 % in late rounds on PubMed/Reddit (Fig 5)). All baselines use default/non-tuned settings; no per-baseline hyperparameter search is recorded → "known failure modes" may reflect adaptation, not the original methods. |
| Reference graph/privacy | Exact clean reference is available in simulation only; descriptor-only exchange not implemented. Secure aggregation not compatible (plain updates). |
| Assumption scope | 1 attacker / static K3 / 20 % / IID / 2-layer GCN / K=5 — all untested beyond these. |
| "<5 ms" | Unsupported. "Within 0.5 %": contradicted. "Dominance": ETD-FGL is not dominant on accuracy everywhere (e.g., Cora FedTGE acc 76.80 > 76.10; but ASR 82.87), and Reddit FLPurifier has lower ASR (0.21) with 49.3 % accuracy; ETD-FGL differences vs Clean FedAvg are single-seed. No dominance/significance claims are supported. |
| Topology channel degeneracy | Benign topology risk is exactly 0 and attacker risk 0.8483 constant in all 9 multi-seed ETD-FGL runs — topology evidence is binary here. Update risk of the attacker: ≈0 on Cora (seed 42/43), up to 0.74 on PubMed, ~0.6 mean on Reddit. |
| Checkpoint selection | By clean validation accuracy over all 50 rounds; ASR trajectories fluctuate strongly, so single-checkpoint ASR may under-represent late-round oscillation (Reddit seed 43 ASR 37.8 % at round 50 vs 34.82 % at best round). |

## 9. Open questions and minimal next steps (not launched)

1. **Seed-43 explanation** — cheapest: compute descriptors (drift per coordinate) for Reddit seeds 42/43/44 from the stored partitions (no training). Without this, state "unexplained".
2. **Is a real-server reference possible?** Author decision (see `audit/UNRESOLVED_QUESTIONS.md` #1).
3. **DMGNN pruning counts** — one inference-only pass of `purify_explanation_guided` on stored Reddit/Cora checkpoints would settle the "zero edges" claim.
4. **Runtime** — a controlled re-timing (same session, repeated, with device logged) if a runtime claim is retained; otherwise drop it.
5. **Clean FedAvg multi-seed** (6 short runs) if the "close to clean FedAvg" claim is wanted.
6. **Statistics** — more seeds (≥10) if significance is claimed; otherwise keep descriptive language.
