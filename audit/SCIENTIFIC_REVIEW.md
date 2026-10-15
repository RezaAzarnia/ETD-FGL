# ETD-FGL Scientific and Methodological Review

**Author/Auditor:** Senior Machine Learning Research Engineer & Scientific Reviewer
**Context:** Journal-Level Scientific Audit of ETD-FGL Codebase
**Date:** October 2026

---

## 1. Executive Scientific Appraisal

The ETD-FGL defense introduces a topology-aware mitigation strategy against structural backdoor attacks in Federated Graph Learning (FGL). By measuring structural graph drift alongside parameter-update anomalies, the server assigns continuous trust weights $\tau_i \in [0.02, 1.0]$ to down-weight malicious clients.

The code audit verified that the mathematical formulas implemented in the production defense match the frozen manuscript specifications:
$$\mathcal{R}_i^{(t)} = \frac{9}{13} \mathcal{A}_i^{\text{topo}} + \frac{4}{13} \mathcal{A}_i^{\text{upd}, t}, \quad \tau_i = \text{clip}\left(\exp(-3.0 \cdot \mathcal{R}_i^{(t)}), 0.02, 1.0\right)$$

However, rigorous scientific scrutiny requires a clear demarcation between **proven software defects** (which were repaired in Phase 2) and **foundational scientific assumptions or experimental limitations** (which must be disclosed to reviewers). This report analyzes six critical methodological aspects.

---

## 2. Detailed Methodological Analysis

### Issue A: Privileged Clean-Graph Reference Assumption
- **Current Implementation:** In `multidata_suite/defenses.py`, `ETDFGLAggregator.__init__` computes topology drift as:
  $$\Delta_i = \left\| \frac{\mathbf{d}(G_i^{(t)}) - \mathbf{d}(G_i^{(0)})}{\boldsymbol{\sigma}_{\text{clean}}} \right\|_2$$
  where $G_i^{(0)}$ is the exact pre-attack clean client graph.
- **Scientific Appraisal:**
  - *Simulation Validity:* In controlled simulated benchmarks, having access to $G_i^{(0)}$ provides a rigorous ground truth reference to assess topological sensitivity.
  - *Real-World Threat Model Limitation:* In practical decentralized federated learning, clients possess private graphs. An adversary that poisons its graph prior to participating in the federation would never present $G_i^{(0)}$ to the server.
  - *Deployable Alternative:* In real deployments, the server could:
    1. Authenticate client graph topology during a trusted initialization/warm-up phase (e.g., first 5 rounds before attack activation).
    2. Monitor inter-round topological drift: $\Delta_i^{(t)} = \|\mathbf{d}(G_i^{(t)}) - \mathbf{d}(G_i^{(t-1)})\|$.
    3. Compare local client descriptors against the cross-client median descriptor: $\Delta_i = \|\mathbf{d}(G_i) - \text{median}_{j}(\mathbf{d}(G_j))\|$.
  - *Recommendation:* Clearly disclose in the manuscript that the benchmark uses an authenticated pre-attack clean reference, and discuss the warm-up/temporal baseline as the practical deployment pathway. Do not alter the benchmark baseline without explicit re-evaluation.

---

### Issue B: Test-Label-Aware Federated Partitioning
- **Current Implementation:** In `multidata_suite/data.py`, `create_partition()` and `create_dirichlet_partition()` stratify node assignments across clients using class labels across all splits (`train_mask`, `val_mask`, `test_mask`).
- **Scientific Appraisal:**
  - *Does this leak test labels into training loss?* **No.** Client training still occurs strictly over `local_graph.train_mask`. Test labels are never passed to the loss function.
  - *Does it affect client graph topology?* **Yes.** Because client subgraphs are induced by the assigned node subsets, partitioning that depends on test labels changes the exact edge boundaries between clients.
  - *Scientific Motivation:* Public benchmark datasets (especially Planetoid Cora with only 140 training nodes total, 20 per class) suffer severe client starvation without stratified allocation. Across 5 clients, random assignment frequently results in clients with 0 training nodes of certain classes or empty splits.
  - *Recommendation:* Disclose that partitioning is class-stratified to prevent degenerate empty-class clients on sparse Planetoid splits. A fully label-blind partitioner (e.g., Metis graph clustering or uniform random node assignment) should be presented as an ablation variant on denser datasets (PubMed, Reddit).

---

### Issue C: FedTGE Energy-Vector Alignment
- **Current Implementation:** In `multidata_suite/fedtge.py`, FedTGE evaluates node free energy $E_v = \text{logsumexp}(Z_{v, :})$ on local subgraphs, pads client energy vectors to $\max_i(N_i)$ with zeros, and computes cosine similarity between vectors.
- **Scientific Appraisal:**
  - *Alignment Invariance:* Node indices across different federated clients represent distinct graph partitions. Index $k$ in client $A$ has no semantic correspondence to index $k$ in client $B$.
  - *Cos-Sim Behavior:* Directly computing cosine similarity between unaligned zero-padded 1D node arrays is permutation-sensitive. If client $A$'s nodes are permuted while preserving graph structure, the resulting dot product changes.
  - *Provenance:* This logic was adopted directly from the official FedTGE codebase (`ZitongShi/fedTGE`).
  - *Recommendation:* Do not alter the comparator silently, as doing so would invalidate comparability with the published FedTGE baseline. A distribution-based energy alignment (e.g., sorting energies or Wasserstein distance / histogram similarity) should be documented as an adapted baseline extension.

---

### Issue D: Confounding in Client-Scalability Experiments
- **Current Implementation:** In `run_extended_experiments.py::run_client_scalability`, the client count varies over $\{5, 10, 20, 30, 50\}$, while the number of malicious clients is held fixed at 1 (`malicious_client_id = 0`).
- **Scientific Appraisal:**
  - When $K = 5$, the malicious fraction is $1/5 = 20.0\%$.
  - When $K = 50$, the malicious fraction drops to $1/50 = 2.0\%$.
  - Consequently, as $K$ increases, observed improvements in defense performance or changes in attack success rate conflate federation scale with a 10-fold reduction in adversarial power.
  - *Recommendation:* Document this dual effect clearly. Future extended studies should report two separate scalability evaluations:
    - *Study 1:* Fixed attacker count ($M = 1$, scaling $K \in \{5, 10, 20, 50\}$).
    - *Study 2:* Fixed attacker fraction ($M/K = 20\%$, e.g., $1/5, 2/10, 4/20, 10/50$).

---

### Issue E: Attack Success Rate (ASR) Evaluation Protocol
- **Current Implementation:**
  - Target class: $y_{\text{target}} = 0$.
  - Trigger: 3-node clique ($K_3$) with fixed trigger feature values.
  - Test Victims: In `multidata_suite/data.py::attach_test_trigger`, triggers are attached to selected non-target test nodes ($y \ne 0, \text{test\_mask} = \text{True}$).
  - ASR is computed as:
    $$\text{ASR} = \frac{\sum_{v \in \mathcal{V}_{\text{victim}}} \mathbb{I}(\hat{y}_v = y_{\text{target}})}{|\mathcal{V}_{\text{victim}}|}$$
- **Scientific Appraisal:**
  - *Label Integrity:* Test victim original labels are verified to remain unmodified in `test_homophily_leakage_fix.py` and `test_final_5d_descriptor.py`.
  - *Batch Injection Interaction:* When multiple triggers are attached to test victims simultaneously within the same test graph, high-order message passing could theoretically allow trigger patterns to propagate between adjacent victims if victims are within 2-hop neighborhoods.
  - *Empirical Check:* In sparse Planetoid graphs with 10–20 test victims, victim-to-victim 2-hop overlap is minimal. However, single-victim isolated inference should be considered for absolute rigor.

---

### Issue F: Baseline Fairness and Computational Parity
- **Compared Baselines:** Clean FedAvg, Attacked FedAvg, PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE, ETD-FGL.
- **Fairness Audit:**
  - *Architecture:* All methods utilize a 2-layer GCN with 32 hidden units and identical dropout ($p=0.5$).
  - *Optimizer:* Shared Adam optimizer ($\text{lr}=0.01$, weight decay $5 \times 10^{-4}$).
  - *Supervised Epochs:* All methods train for $E=3$ local supervised epochs per round.
  - *Computational Overhead Disclosure:* While supervised epoch counts match, FLPurifier requires additional contrastive pre-training passes, FedTGE executes energy calibration and belief propagation, and ETD-FGL computes descriptor drift and coordinate-wise update medians. These differing runtime profiles are accurately logged in `training_history.csv` and depicted in runtime comparison figures.
  - *Sampled Reddit Graph:* The Reddit dataset uses a deterministic stratified 8,000-node subgraph to fit workstation memory. The manuscript must explicitly describe Reddit results as "Sampled Reddit (8,000 nodes)" rather than the full 232,965-node graph.

---

## 3. Conclusion

The ETD-FGL codebase is mathematically sound and faithfully executes the declared defense formulation. The scientific considerations highlighted above do not constitute coding bugs, but rather represent modeling assumptions that must be clearly disclosed in the methodology and limitation sections of the journal manuscript.
