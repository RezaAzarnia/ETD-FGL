# ETD-FGL — Complete Code Truth (implementation at 80a3210; line numbers at branch HEAD 3084163)

Everything here is derived from code and raw outputs, not from the old manuscript. Facts are tagged **[CODE]** (implementation), **[MEASURED]** (raw results), **[INTERP]** (interpretation, not isolated by an experiment), **[HYP]** (hypothesis). The method is not a rewrite of an earlier ETD-FGL: only one implementation exists (the single algorithmic change in Git is 6-D → 5-D label-free descriptor, commit 953e250).

## 1. Identity, novelty, execution sequence
**What it is [CODE].** A server-side, soft (trust-weighted) robust aggregation rule for federated node classification. Per round the server weighs each client's model by sample count × trust, where trust is an exponential of a fused anomaly risk. Two evidence streams: (i) a static *topology drift* between each client's current graph and an authenticated clean reference graph, via a 5-D label-free descriptor; (ii) a dynamic *update anomaly* (distance of the client's parameter update to the coordinate-wise median update). Both are mapped to [0,1] by the same one-sided robust sigmoid map and fused 9/13 : 4/13.
**Actual novelty (defensible).** Using exact-reference topology drift as evidence inside a trust-weighted FL aggregator, combined with median-update anomaly, plus a *controlled* ablation protocol that holds coefficients fixed (the renormalized ablation confounds channel removal with a 44 % coefficient increase). **Not novel/over-claimable:** coordinate-wise median distance, MAD/sigmoid scoring, exponential trust. No privacy-preserving deployment, no adaptive-attack robustness, no graded detection (see §10).
**Execution per run [CODE]** (`core.py:run_method`, `defenses.py:ETDFGLAggregator`):
1. `set_seed(seed)`; load dataset; IID class-stratified partition into K=5 induced subgraphs; inject trigger into client 0; build evaluation-trigger graph.
2. Construct `ETDFGLAggregator(clean_graphs, attacked_graphs, …)` ⇒ compute descriptors, drift, **A_topo once** (static for all rounds).
3. For round t=1..50: every client trains the global state for 3 full-batch Adam epochs on its local graph; server flattens deltas, computes median update, distances, A_upd^t, R, T, w; global ← Σ w_i θ_i; evaluate on global clean graph and global triggered graph; log; save checkpoint if clean validation accuracy strictly improves.
4. Reload best-validation checkpoint; report its test accuracy, ASR, CTR, attack effect. Wall-clock = whole loop.

## 2. Threat model [CODE]
K=5 clients, M=1 malicious (client 0, fixed id), static poisoning before round 1, honest-looking local training with no update scaling/model replacement. Attacker knows its own data only. Poison budget ρ=0.20 of client-0 **non-target training nodes** (victims = ⌈0.2·|candidates|⌉ random); victim label set to target class 0; each victim receives 3 new nodes forming a K3 clique, each connected to the victim (bidirectional edges); trigger nodes carry the same fixed sparse feature vector (16 active features chosen by seeded permutation, value = median clean row norm/√16), label 0, but are **not** in the training mask. Evaluation trigger: the same prototype attached (K3) to **every** non-target test node in one global graph. Victim counts: Cora 5, PubMed 2, Reddit 227. No collusion, no adaptive trigger, no cross-round strategy. Server: honest; in the simulation it reads both clean and current client graphs and plaintext updates.

## 3. Datasets and partitioning [CODE][MEASURED]
Cora (2,708 nodes, 10,556 directed edge entries) and PubMed (19,717; 88,648) with Planetoid public splits and `NormalizeFeatures`; Reddit: fixed class-stratified induced 8,000-node subgraph (sample seed 42, 135,224 directed entries; 6,000 train / 1,000 val / 1,000 test, 41 classes, 602 features). Public splits: Cora 140/500/1000, PubMed 60/500/1000. Partition: IID **label-aware** round-robin per (split, class) so every client gets ≈1/5 of each; clients hold induced subgraphs (cross-client edges are lost). Per-client counts: Cora 542 nodes (28/100/200), PubMed ≈3,943 (12/100/200), Reddit 1,600 (1,200/200/200). Partition seed = run seed. A Dirichlet non-IID option exists but was **never run**.

## 4. Model and training [CODE]
2-layer GCN (hidden 32, ReLU, dropout 0.5); Adam, lr 0.01 (Cora, PubMed) / 0.005 (Reddit), weight decay 5e-4; 3 local epochs/round (full batch); 50 rounds; seeds 42/43/44; cross-entropy on local train mask. FedAvg weights = local train-node counts. Evaluation each round on the global graph with global masks; checkpoint = highest clean validation accuracy (first maximum). Device/software of the stored runs were **not recorded** (added to future runs by commit 28340f8); the project venv has CPU-only torch 2.14.1 [UNVERIFIED which device ran them].

## 5. Metrics [CODE]
Test accuracy over the clean global test mask (1,000 nodes). CTR = share of non-target test nodes predicted class 0 on the clean graph; ASR = same on the triggered graph; attack effect = ASR − CTR (pp). Denominators (non-target test nodes, derived from ASR granularity): Cora 870, PubMed 820, Reddit 942. Attacker share = mean over rounds of w₀. Benign risk = mean over rounds of mean R of clients 1–4. Runtime = `elapsed_seconds` (§core `TIMING_SCOPE`: includes per-round evaluation; no CUDA sync/warm-up control). ± = sample SD (ddof=1) over n=3.

## 6. Baselines (what is really implemented) [CODE]
| Method | Implementation | Notes |
|---|---|---|
| Clean FedAvg | FedAvg on unpoisoned client graphs | seed 42 only |
| Attacked FedAvg | FedAvg on attacked graphs | 3 seeds |
| PD-FL | IsolationForest (250 trees) on a 24×24 cubical-persistence signature + norm stats of each update; trust = clip(sigmoid(z),0.03,1); calibrated on 4 rounds of *clean* client updates | uses clean reference; adaptation |
| GSP-FL | per client prune 12 % of edges with largest spectral-embedding (rank 20) distance, then FedAvg | adaptation |
| FLPurifier-GNN | contrastive (NT-Xent) local training; conv1 averaged by n_i, conv2 weighted by cosine-to-median (floor 0.05) | accuracy collapses (49–67 %) |
| DMGNN-FL | per client: ≤8 highest-target-probability train nodes; ≤12 incident edges each; remove up to 3 edges whose removal lowers target probability by ≥0.02 (uses the Attacked-FedAvg checkpoint); then FedAvg | leave-one-edge-out heuristic, **not GNNExplainer**; pruning counts not stored for existing runs |
| FedTGE | adapted from official repo (commit e80950c): energy-calibrated LayerNorm, FINCH cluster rejection, energy belief propagation; 3 supervised epochs; hidden 32 | very slow; unstable accuracy |
All share backbone, rounds, local epochs, seeds; none tuned. Information asymmetry: ETD-FGL (and PD-FL calibration) use clean references; DMGNN reuses a prior attacked run.

## 7. Ablations [CODE]
* **Standard (renormalized)** — `ConfigurableETDFGLAggregator`: Topology-only (weights 1.0/0), Update-only (0/1.0), No-trust (uniform; ≡ Attacked FedAvg, confirmed numerically), Historical 3-channel (0.45 topology / 0.35 GNNExplainer-score / 0.20 update). Coefficients are normalized to sum 1 ⇒ topology-only raises the topology coefficient from 9/13 to 1.0.
* **Controlled (fixed coefficients)** — `ControlledAblationETDFGLAggregator`: Full (9/13, 4/13), Fixed-No-Update (9/13, 0), Fixed-No-Topology (0, 4/13); trust map unchanged. Paired by seed.
Interpretation limits [INTERP]: both removal and renormalization change the algorithm; with n=3 no variant ranking is statistically supported.

## 8. Results [MEASURED] (all in `TABLES/`, summary in `RESULTS_AND_STATISTICS.md`)
Seed-42 ETD-FGL: Cora 76.10 / ASR 4.25; PubMed 77.60 / 1.22; Reddit 85.30 / 0.85. 3-seed ASR: Cora 5.21±0.88 (Attacked 62.03±15.38); PubMed 0.89±0.56 (9.23±7.36; only 2 poisoned nodes); Reddit 14.08±18.19 (74.42±1.85; seeds 0.85/**34.82**/6.58). Clean accuracy 3-seed: 75.57±1.57 / 75.50±2.01 / 84.87±0.40 vs Attacked FedAvg 75.00 / 74.80 / 84.90. Controlled paired ΔASR: remove-topology +37.3 / +3.6 / +52.2 pp; remove-update +1.2 / +0.3 / +11.1 pp (n=3, no test). Attacker mean share 4.76 / 4.55 / 2.53 %.

## 9. Mechanism evidence [MEASURED] and interpretation
* Attacker A_topo = 0.848284 exactly in all 84 ETD-type runs; benign A_topo = 0 in every round [MEASURED, `T14`]. ⇒ the topology channel is a binary "client graph ≠ reference" signal, independent of trigger size/strength [INTERP, follows from the formula].
* Attacker A_upd: ≈0 on Cora (seeds 42,43), up to 0.74 on PubMed, mean ≈0.6 on Reddit [MEASURED]; so the update channel only matters where the attacker's update is atypical (Reddit) [INTERP].
* Fixed-No-Update attacker share is a constant 4.117 % (analytic: 0.1717/(0.1717+4)) [MEASURED+CODE].
* Round-1 ASR (Cora 75.4 %, PubMed 99.9 %) is high even for unattacked Clean FedAvg at round 1 (40.5 %, 61.2 %) ⇒ early ASR reflects initialization/class-0 bias, not only the backdoor [INTERP].
* Reddit seed 43 residual ASR: cause unknown [HYP only].

## 10. Weaknesses that remain
Reference graph unavailable to real servers; benign drift is exactly zero (no benign graph variability tested); single static non-adaptive attacker; IID label-aware partition only; evaluation on the full graph vs training on induced subgraphs; centralized validation set for checkpoint selection; n=3 seeds, no tests, large Reddit variance; baselines are adapted and untuned; runtimes unreliable; PubMed attack is weak (2 victims); 2-layer GCN only; no ε/privacy analysis; sum of fixed constants 9/13, 4/13, β=3, floor 0.02 never tuned or sensitivity-tested.

## 11. Provenance
Authoritative code: commit `80a321027b26853eee1c2c4f415e1ec9c1f4961c` (tag `paper-results-v1.0.0`). Revision branch `revision-audit-2026-11`: `28340f8` (runtime provenance), `7a1cc1f` (DMGNN diagnostics), `3084163` (raw-recompute tools) — **none changes algorithm, protocol or any stored metric**; stored results remain valid for 80a3210. Raw results: `outputs/**` (git-ignored; per-run `experiment_manifest.json` SHA-256), 132 runs: baseline 24, multiseed 18, standard ablation 54, controlled ablation 36 (some seed-42 reuse; elapsed times differ between suites for byte-identical histories).
Source map (line numbers, branch HEAD): `defenses.py` descriptor 344, `_robust_positive` 450, `ETDFGLAggregator` 498, `ConfigurableETDFGLAggregator` 570, `purify_explanation_guided` 229, `purify_gsp` 111, `PDFLAggregator` 89, `FLPurifierAggregator` 198; `core.py` `build_context` 78, `evaluate` 199, `run_method` 452; `attack.py` trigger 91, eval trigger 257; `data.py` `create_partition` 247, `load_dataset` 89; `controlled_ablation.py` (whole file).

## 12. Pseudocode
See `EQUATIONS_AND_PSEUDOCODE.md`.
