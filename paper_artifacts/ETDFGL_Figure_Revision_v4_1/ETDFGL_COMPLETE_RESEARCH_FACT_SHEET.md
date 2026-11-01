# ETD-FGL Complete Research Fact Sheet and Technical Evidence Report (Revision v4.1)

**Document Purpose:** Independent academic and technical reference document for manual manuscript revision.  
**Target Audience:** Scientific editor / research author revising the ETD-FGL paper.  
**Verification Level:** Rigorously audited against the frozen codebase (Commit `80a3210`), 132 completed directory records (`final_summary.json`), 132 checkpoint file paths (`best_model.pt`), and 99 distinct checkpoint SHA-256 hashes on disk.  
**Repository Working Directory:** `c:\Users\R_Azarnia\Desktop\main paper\ETD-FGL\`  
**Date of Evidence Freeze:** October 17, 2026  

### Git Commit Provenance:
- **Current Working-Tree Commit:** `80a321027b26853eee1c2c4f415e1ec9c1f4961c` (HEAD, branch `audit-fix-verification`).
- **Parent Frozen Archive Commit:** `953e2501a3571d4e08bf6ef6d7e008d19762144d` (pre-audit archive; line numbers in `multidata_suite/defenses.py` are offset by -15 lines relative to HEAD due to diagnostic logging added at lines 232–285).

---

# SECTION 1 — RESEARCH IDENTITY AND OBJECTIVE

### 1.1 Full Project Name and Acronym
- **Author-Confirmed Manuscript Title:** *ETD-FGL: Evidence-Based Topological Defense for Federated Graph Learning Against Backdoor Attacks* (`1/main.tex:33`).
- **Repository Context Title:** *Federated Graph Learning Against Backdoor Attacks Using Topology-aware Defense* (`README.md:3`).
- **Short Name / Acronym:** ETD-FGL.
- **Expansion Note:** The title and acronym denote Evidence-based Topological Defense for Federated Graph Learning, aligning with author manuscript files and repository README (avoiding the unconfirmed "Explaining Topological Drift" expansion).

### 1.2 Problem Statement
Federated Graph Learning (FGL) enables decentralized clients to collaboratively train Graph Neural Networks (GNNs) on partitioned node-classification tasks without centralizing their raw graphs, node attributes, or local topological connections. However, FGL's decentralized topology creates vulnerability to **targeted structural backdoor attacks**. A malicious client can perturb its local subnetwork by injecting dense, synthetic graph triggers (e.g., small complete subgraphs / cliques) linked to designated victim nodes. When aggregated via standard Federated Averaging (FedAvg), the global GNN memorizes the trigger pattern, causing test-time nodes from non-target classes to be misclassified into the attacker's target class whenever the trigger subnetwork is attached, while preserving high classification accuracy on clean inputs.

### 1.3 Research Motivation
Existing federated defenses against backdoor attacks are predominantly designed for Euclidean data (computer vision, NLP) and operate exclusively in the parameter/gradient space (e.g., coordinate-wise median, trimmed mean, clipping, or update distance clustering). In graph domains, parameter-space defenses face specific challenges:
1. Backdoor gradient vectors can blend into the benign variance induced by non-IID graph structural heterogeneity.
2. Parameter-space defenses do not directly leverage graph-specific topological indicators: malicious structural modifications introduce measurable, non-local deformations in graph topology (e.g., changes in clustering coefficients, triangle counts, and degree distributions) that parameter updates alone may not reliably isolate.

Conversely, purely graph-based defenses (such as edge pruning via spectral clustering or homophily heuristics) either require careful thresholding or can impose substantial computational overhead (e.g., FedTGE's graph entropy matrix calculations, which take hundreds of seconds per 50-round loop in evaluated settings: 177s on Cora, 773s on PubMed, 400s on Reddit, or approximately 3.5s to 15.5s per round).

### 1.4 Implemented Defense Approach
ETD-FGL implements an **asymmetric dual-evidence server-side aggregation defense**:
1. **Offline Structural Channel (Topological Drift):** Each client's local graph topology is summarized using a label-free 5-dimensional structural descriptor. In simulation, the server evaluates the standardized Euclidean drift between the current graph and an authenticated clean pre-attack reference graph, mapped to a bounded topological anomaly score $A_i^{\text{topo}} \in [0, 1]$ via a one-sided robust positive median-absolute-deviation (MAD) sigmoid transform.
2. **Online Parameter Channel (Model Update Anomaly):** At every communication round, local model parameter updates are compared against the coordinate-wise update median. The Euclidean parameter divergence is transformed into a bounded dynamic update anomaly score $A_i^{\text{upd}, t} \in [0, 1]$.
3. **Risk Fusion and Exponential Trust Weighting:** The two evidence streams are combined via fixed convex weighting ($R_i^t = \frac{9}{13} A_i^{\text{topo}} + \frac{4}{13} A_i^{\text{upd}, t}$), yielding an exponential client trust factor $T_i^t = \text{clip}(\exp(-3 R_i^t), 0.02, 1.0)$ that dynamically downweights the malicious client's aggregation share to $\le 4.8\%$ in the evaluated multi-seed benchmarks.

### 1.5 Scope of Empirical Findings
- **Observed Empirical Results:**
  - In the evaluated benchmarks, ETD-FGL substantially mitigates targeted structural clique backdoor attacks across citation and social network datasets.
  - Across three random seeds (42, 43, 44), mean Backdoor Attack Success Rate (ASR) is reduced from $62.03 \pm 15.38\%$ to $5.21 \pm 0.88\%$ on Cora, from $9.23 \pm 7.36\%$ to $0.89 \pm 0.56\%$ on PubMed, and from $74.42 \pm 1.85\%$ to $14.08 \pm 18.19\%$ on Reddit (with single-seed ASR dropping to 0.85% on Seed 42).
  - **Clean Classification Accuracy Preservation:**
    - On Seed 42, where an unattacked **Clean FedAvg control** was evaluated, ETD-FGL preserves clean test accuracy within **1.30 percentage points** of Clean FedAvg: Cora $76.10\%$ vs $76.10\%$ ($+0.00$ pp), PubMed $77.60\%$ vs $76.30\%$ ($+1.30$ pp), Reddit $85.30\%$ vs $86.20\%$ ($-0.90$ pp).
    - In the multi-seed evaluation (Seeds 42, 43, 44), **no multi-seed Clean FedAvg control was executed**. Multi-seed comparisons are established against **Attacked FedAvg**, where ETD-FGL clean classification accuracy ($75.57 \pm 1.57\%$ Cora, $75.50 \pm 2.01\%$ PubMed, $84.87 \pm 0.40\%$ Reddit) closely tracks Attacked FedAvg clean accuracy ($75.00 \pm 0.72\%$, $74.80 \pm 3.18\%$, $84.90 \pm 0.80\%$), showing that trust-weighted downweighting does not penalize primary classification performance.
  - In recorded training loops, ETD-FGL runtimes remain within the same order of magnitude as standard FedAvg across all suites (under 11s: e.g., Cora Seed 42 is 3.26s vs 2.88s [1.13x], multi-seed is 2.85s vs 2.73s [1.04x]; PubMed multi-seed is 10.53s vs 9.44s [1.12x]; Reddit multi-seed is 7.40s vs 11.07s), avoiding the massive compute latency observed in graph-entropy baselines (FedTGE loop runtimes reach 177s to 773s for 50 rounds).
- **Explicit Limitations and Boundaries:**
  - GNNExplainer is NOT part of the active defense path. The explanation-subgraph module is explicitly bypassed ($c_{\text{expl}} = 0.0$) and serves only as an optional post-hoc diagnostic.
  - The evaluation does not claim universal robustness against arbitrary, feature-only, or clean-label poisoning attacks.
  - The defense model assumes benign clients constitute a majority ($M < K/2$). Colluding multi-attacker settings ($M \ge 2$) have not been evaluated.
  - Complete elimination of backdoor retention is not achieved in all partitions: on Reddit Seed 43, ASR remains at 34.82% (Attack Effect 34.39 pp), reflecting sensitivity to random graph partitioning across seeds (without unsupported causal conjectures regarding trigger contrast or degree variance).

### 1.6 Evidence-Supported Scientific Contributions
1. **Systematic empirical benchmark:** Evaluates parameter-space and graph-tailored federated defenses under targeted structural clique backdoors across three distinct network domains.
2. **Analysis of the 5-client scale-invariance:** Identifies and mathematically derives the scale-invariance property under the qualified nonzero-drift, single-attacker regime ($K=5$, $M=1$, $d_0 = d \ge 2.5 \times 10^{-8}$, $d_{1..4}=0$), producing an invariant outlier z-score $z_0 \equiv 2.50$ and topological anomaly score $A_0^{\text{topo}} \approx 0.848284$, which yields an invariant attacker weight share $w_0 \equiv 4.12\%$ under equal sample sizes in the Fixed No Update condition. Below $2.5 \times 10^{-8}$, anomaly varies continuously down to $0.0$ at $d=0$.
3. **Controlled channel ablation methodology:** Demonstrates that standard weight normalization masks individual channel contributions, and establishes a controlled held-constant ablation protocol showing that both topology and update channels provide non-redundant mitigation under held-constant penalization.

---

# SECTION 2 — SYSTEM AND THREAT MODEL

### 2.1 System Architecture
- **Federation Size:** $K = 5$ participating clients.
- **Client Topology:** Star topology; all clients communicate exclusively with a central federated aggregation server.
- **Communication Protocol:** Synchronous Federated Averaging over $T = 50$ communication rounds.
- **Local Optimization:** Each client executes $E = 3$ local epochs of Adam optimization per round.

### 2.2 Server Assumptions and Simulation Clean-Reference Access
- **Honest Server:** The central server is honest-but-curious and correctly executes the aggregation protocol.
- **Simulation Graph Access Mechanism:** In the experimental simulation code (`multidata_suite/defenses.py:498–507`), the `ETDFGLAggregator.__init__` method receives full `clean_graphs` and `current_graphs` PyG `Data` graph objects directly in memory and computes descriptors server-side.
- **Deployment Proposal vs Simulation Status:** In a practical privacy-preserving deployment, clients would compute their 5D descriptor vectors locally and transmit only the 5 summary scalars to the server during certified enrollment. However, **a descriptor-only authenticated network exchange is not implemented or validated in the codebase**. Claims that "the deployed server never sees client edge objects" represent an architectural proposal, not an established empirical property of the evaluated code.

### 2.3 Adversarial Model and Threat Capabilities
- **Adversary Identity:** Exactly one client ($M = 1$, designated as Client 0) is malicious, constituting 20% of the federation.
- **Attacker Knowledge:** The attacker has full access to its own local data partition (white-box over Client 0's local graph), including local features, adjacency, and labels. The attacker has no access to benign clients' local data or model states.
- **Target Class:** Targeted backdoor attack with target class $y^* = 0$.
- **Local Poisoning Budget:** $\rho = 0.20$ (20% of candidate non-target training nodes in Client 0's partition are chosen as victims).
- **Poisoning Timing:** Static offline poisoning executed prior to round 1; the poisoned local graph remains fixed throughout all 50 rounds.

### 2.4 Structural Backdoor Trigger Structure
- **Trigger Type:** Complete graph / clique trigger ($K_3$, size $s = 3$ nodes).
- **Trigger Injection Mechanism:**
  1. For each victim node $v \in \mathcal{V}_{\text{victim}}^{(0)}$, 3 synthetic trigger nodes are added to Client 0's graph.
  2. Complete mutual edges are formed among the 3 trigger nodes, forming a 3-clique.
  3. Bidirectional edges are added connecting each trigger node to the victim node $v$.
  4. The victim node's label and the trigger nodes' labels are set to target class $y^* = 0$.
  5. **Feature Perturbation:** Trigger nodes receive a deterministic sparse feature vector generated by `make_sparse_trigger_prototype()` with 16 active features, whose $L_2$ norm is calibrated to the median row norm of the dataset's clean features.
- **Test-Time Evaluation Trigger:** During test-time backdoor evaluation, the identical 3-node clique trigger and feature pattern are attached to global test nodes that do not belong to class 0 ($v_{\text{test}} \in \mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}$).

---

# SECTION 3 — DATASET CONSTRUCTION AND PARTITIONING

### 3.1 Benchmark Datasets
All experiments evaluate three benchmark graph datasets representing distinct topological domains:
1. **Cora:** Citation network; 2,708 nodes, 5,429 edges, 1,433 node features, 7 classes.
2. **PubMed:** Large-scale sparse citation network; 19,717 nodes, 44,338 edges, 500 node features, 3 classes.
3. **Reddit:** Online social post network; evaluated via a deterministic class-stratified 8,000-node subgraph (8,000 nodes, 24,710 edges, 602 features, 41 classes) to enable standardized GPU evaluation.

### 3.2 Partitioning Protocol
- Client graphs are constructed using label-aware class-stratified partitioning across $K = 5$ clients.
- Random seeds for graph partitioning and local initialization are strictly fixed to Seeds 42, 43, and 44 across all multi-seed suites.

---

# SECTION 4 — MODEL ARCHITECTURE AND TRAINING PROTOCOL

- **GNN Backbone:** 2-layer Graph Convolutional Network (GCN).
- **Layer Dimensions:** Input features $F \to 32$ hidden units $\to C$ classes (where $C = 7$ for Cora, $3$ for PubMed, $41$ for Reddit).
- **Activation & Dropout:** ReLU activation between layers; dropout probability $p = 0.5$.
- **Local Optimizer:** Adam optimizer with weight decay $5 \times 10^{-4}$. Learning rate is dataset-specific: $\eta = 0.01$ for Cora and PubMed, and $\eta = 0.005$ for Reddit (`multidata_suite/config.py:14, 49`).
- **Local Epochs:** $E = 3$ local epochs per communication round.
- **Global Communication Rounds:** $T = 50$ synchronous rounds across all 132 runs.

---

# SECTION 5 — DETAILED MATHEMATICAL SPECIFICATION OF ETD-FGL

### 5.1 Five-Dimensional Topological Descriptor
For any graph snapshot $G = (\mathcal{V}, \mathcal{E})$, the label-free structural descriptor vector $\mathbf{D}(G) \in \mathbb{R}^5$ is defined as:

$$\mathbf{D}(G) = \begin{bmatrix} \rho(G) \\ \mu_d(G) \\ \tilde{\sigma}_d^2(G) \\ C(G) \\ \tau(G) \end{bmatrix} = \begin{bmatrix} \frac{2|\mathcal{E}|}{|\mathcal{V}|(|\mathcal{V}| - 1)} \\ \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} d_v \\ \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} (d_v - \mu_d)^2 \cdot \frac{1}{\mu_d^2 + 10^{-12}} \\ \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} \frac{2 T_v}{d_v(d_v - 1)} \\ \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} T_v \end{bmatrix}$$

*Code Location:* `multidata_suite/defenses.py:322–357` (Commit `80a3210`; was `307–342` in `953e250`). Line 344 explicitly evaluates `norm_deg_var = float(degrees.var() / (degrees.mean() ** 2 + 1e-12))`, using $10^{-12}$ rather than $10^{-8}$.

### 5.2 Standardized Topological Drift Distance
Given clean reference graphs $G_0^{\text{clean}}, \dots, G_{K-1}^{\text{clean}}$ and current round graphs $G_0^{\text{curr}}, \dots, G_{K-1}^{\text{curr}}$:
1. Compute clean descriptor matrix $\mathbf{D}^{\text{clean}} \in \mathbb{R}^{K \times 5}$ and current descriptor matrix $\mathbf{D}^{\text{curr}} \in \mathbb{R}^{K \times 5}$.
2. Feature-wise standard deviation scale:
   $$\mathbf{s} = \text{std}(\mathbf{D}^{\text{clean}}, \text{axis}=0), \quad s_j = \begin{cases} s_j, & \text{if } s_j \ge 10^{-8} \\ 1.0, & \text{otherwise} \end{cases}$$
3. Standardized Euclidean drift distance $d_i$:
   $$d_i = \left\| \frac{\mathbf{D}_i^{\text{curr}} - \mathbf{D}_i^{\text{clean}}}{\mathbf{s}} \right\|_2$$

*Code Location:* `multidata_suite/defenses.py:506–510` (Commit `80a3210`; was `491–495` in `953e250`).

### 5.3 One-Sided Robust Positive MAD Mapping (`_robust_positive`)
For a vector of non-negative divergence values $\mathbf{v} = [v_0, \dots, v_{K-1}]$:

$$\text{med} = \text{median}(\mathbf{v})$$

$$\text{MAD} = \max\left(1.4826 \cdot \text{median}(|\mathbf{v} - \text{med}|), \; \text{std}(\mathbf{v}), \; 10^{-8}\right)$$

$$z_i = \max\left(\frac{v_i - \text{med}}{\text{MAD}}, \; 0.0\right)$$

$$A_i = \text{clip}\left(2.0 \cdot \left(\frac{1}{1 + e^{-z_i}} - 0.5\right), \; 0.0, \; 1.0\right)$$

- When $v_i \le \text{med}$, $z_i = 0 \implies A_i = 0.0$ (no false-positive penalty for clients below median drift).
- As $z_i \to \infty$, $A_i \to 1.0$.

*Code Location:* `multidata_suite/defenses.py:428–432` (Commit `80a3210`; was `413–417` in `953e250`).

### 5.4 Model-Update Anomaly Calculation
At communication round $t$, local model parameters $\mathbf{w}_i^t$ are flattened into delta vectors:

$$\Delta \mathbf{w}_i^t = \mathbf{w}_i^t - \mathbf{w}_{\text{global}}^{t-1}$$

The server computes the coordinate-wise update median $\mathbf{m}_{\text{upd}}^t \in \mathbb{R}^P$:

$$m_{\text{upd}, p}^t = \text{median}_{j \in \{0, \dots, K-1\}} \left(\Delta w_{j, p}^t\right)$$

The Euclidean parameter divergence $\delta_i^t$ is:

$$\delta_i^t = \|\Delta \mathbf{w}_i^t - \mathbf{m}_{\text{upd}}^t\|_2$$

The dynamic model update anomaly score is:

$$A_i^{\text{upd}, t} = \text{\_robust\_positive}\left(\left[\delta_0^t, \dots, \delta_{K-1}^t\right]\right)_i$$

*Empirical Note:* On Cora (Seed 42), the malicious client's update deviation remains below or at the median update deviation across all 50 rounds, yielding identically $A_0^{\text{upd}} \equiv 0.0000$.

*Code Location:* `multidata_suite/defenses.py:530–532` (Commit `80a3210`; was `515–517` in `953e250`).

### 5.5 Risk Fusion and Exponential Trust Factor
The fused client risk $R_i^t$ is a convex combination:

$$R_i^t = \alpha_{\text{topo}} A_i^{\text{topo}} + \alpha_{\text{upd}} A_i^{\text{upd}, t}$$

$$\text{Production Constants:} \quad \alpha_{\text{topo}} = \frac{9}{13} \approx 0.6923, \quad \alpha_{\text{upd}} = \frac{4}{13} \approx 0.3077$$

The trust factor $T_i^t \in [0.02, 1.0]$ is computed using exponential penalization with trust decay parameter $\beta = 3.0$ and clipping floor $\tau_{\min} = 0.02$:

$$T_i^t = \text{clip}\left(\exp\left(-3.0 \cdot R_i^t\right), \; 0.02, \; 1.0\right)$$

*Code Location:* `multidata_suite/defenses.py:533–534` (Commit `80a3210`; was `518–519` in `953e250`).

### 5.6 Sample-Weighted Aggregation
Let $n_i$ be the number of training nodes owned by client $i$. The aggregation weight $w_i^t$ is:

$$w_i^t = \frac{T_i^t \cdot n_i}{\sum_{j=0}^{K-1} T_j^t \cdot n_j}$$

The updated global model parameters are:

$$\mathbf{w}_{\text{global}}^t = \sum_{i=0}^{K-1} w_i^t \mathbf{w}_i^t$$

*Code Location:* `multidata_suite/defenses.py:535–545` (Commit `80a3210`; was `520–530` in `953e250`).

---

# SECTION 6 — BASELINE IMPLEMENTATIONS AND LIMITATIONS

All eight methods were executed under identical protocol settings (5 clients, Seed 42, 50 rounds, 3 local epochs, same 2-layer GCN architecture, identical execution environment).

| Baseline Method | Target Mechanism | Implementation in Repository | Datasets Available | Key Limitations Identified in Repository |
| :--- | :--- | :--- | :--- | :--- |
| **Clean FedAvg** | Unattacked Standard FedAvg | `fedavg_clean` | Cora, PubMed, Reddit | Baseline reference on clean accuracy; 0% attack. Evaluated on Seed 42 only (no multi-seed control). |
| **Attacked FedAvg** | Unmitigated Standard FedAvg | `fedavg_structural_backdoor` | Cora, PubMed, Reddit | Baseline reference for unmitigated attack; admits 48–74% ASR across seeds. |
| **PD-FL** | Projected Dynamic FL | `multidata_suite/defenses.py:89–197` | Cora, PubMed, Reddit | Uses update projection similarity; does not prevent structural backdoor convergence (ASR 53.2% Cora, 73.1% Reddit). |
| **GSP-FL** | Graph Spectral Pruning | `baseline_suite/gsp.py` | Cora, PubMed, Reddit | Prunes high-frequency graph laplacian components; ineffective against localized clique triggers (ASR 55.9% Cora, 73.1% Reddit). |
| **FLPurifier-GNN** | Gradient-Purified FL | `multidata_suite/defenses.py:198–299` | Cora, PubMed, Reddit | Purifies updates via internal reconstruction; heavily degrades clean accuracy (Cora acc drops to 56.9%, Reddit to 49.3%). |
| **DMGNN-FL** | Dynamic Masked GNN FL | `baseline_suite/dmgnn.py` | Cora, PubMed, Reddit | **Reddit Equivalence Note:** On Reddit, yielded metrics and model weight hashes identical to Attacked FedAvg (85.70% Acc, 72.29% ASR). Hypothesis that explanation saliency thresholds pruned 0 edges is unverified as pruning counts were not logged. |
| **FedTGE** | Graph Topology Entropy | `multidata_suite/fedtge.py:528+` | Cora, PubMed, Reddit | **Substantial Runtime Overhead:** Recorded 50-round loop times of 177s (Cora), 773s (PubMed), and 400s (Reddit), while admitting high ASR on Cora (82.9%). |
| **ETD-FGL** | Dual-Evidence Anomaly Fusion | `multidata_suite/defenses.py:476+` | Cora, PubMed, Reddit | Backdoor ASR drops to 4.25% (Cora), 1.22% (PubMed), 0.85% (Reddit) on Seed 42, maintaining loop runtime comparable to standard FedAvg. |

---

# SECTION 7 — EVALUATION METRICS DEFINITION

### 7.1 Clean Test Classification Accuracy
- **Definition:** Percentage of unpoisoned test nodes in global test set $\mathcal{V}_{\text{test}}$ correctly classified into their ground-truth classes:
  $$\text{Clean Accuracy} = \frac{\sum_{v \in \mathcal{V}_{\text{test}}} \mathbb{I}(\hat{y}_v = y_v)}{|\mathcal{V}_{\text{test}}|} \times 100\%$$
- **Denominator:** Number of clean test nodes ($|\mathcal{V}_{\text{test}}| = 1,000$ for Cora and PubMed; $1,000$ for Reddit).

### 7.2 Backdoor Attack Success Rate (ASR)
- **Definition:** Percentage of non-target test nodes ($y_v \ne y^*$) misclassified into target class $y^* = 0$ when the 3-node clique trigger is attached to their local egonet:
  $$\text{ASR} = \frac{\sum_{v \in \mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}} \mathbb{I}(\hat{y}_v^{\text{triggered}} = y^*)}{|\mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}|} \times 100\%$$
- **Denominator:** Number of test nodes whose ground truth is NOT class 0.

### 7.3 Trigger Attack Effect
- **Definition:** Net difference in target-class prediction rate induced by the trigger:
  $$\text{Attack Effect} = \text{ASR} - \text{Clean Target Rate}$$
  where $\text{Clean Target Rate} = \frac{\sum_{v \in \mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}} \mathbb{I}(\hat{y}_v^{\text{clean}} = y^*)}{|\mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}|} \times 100\%$.
- **Interpretation:** Reported in percentage points (`pp`). Positive values indicate trigger-induced target predictions. Non-positive values indicate that triggered target predictions remain at or below the clean baseline target rate.

### 7.4 Attacker Aggregation Weight Share ($w_0$)
- **Definition:** Normalized aggregation weight allocated to malicious Client 0:
  $$w_0^t = \frac{T_0^t n_0}{\sum_{j=0}^{K-1} T_j^t n_j} \times 100\%$$
- **Baseline Reference:** Under uniform 5-client aggregation with equal sample counts, $w_0 \equiv 20.0\%$.

### 7.5 Recorded Training-Loop Runtime
- **Definition:** Wall-clock elapsed execution time in seconds (`elapsed_seconds`) for completing all 50 federated rounds.
- **Scope:** Measures the active local training and server aggregation loop over 50 rounds. It does NOT isolate the server aggregation function from local client training.
- **Overhead Clarification:** In recorded 50-round loops, ETD-FGL runtimes remain within the same order of magnitude as standard FedAvg across all suites (under 11s), in stark contrast to FedTGE (up to 773s). Generic ratio assertions (e.g., $\le 1.1\times$ or $1.02\times$–$1.21\times$) are removed as unsupported; server aggregation step latency was not isolated from local training.

---

# SECTION 8 — COMPLETE EXPERIMENTAL RESULTS TABLES

### 8.1 Table 1: Comprehensive Baseline Comparisons (Seed 42)

| Dataset | Method | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (pp) ↓ | Training Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Clean FedAvg | 76.10 | 3.56 | -0.46 | 2.90 |
| | Attacked FedAvg | 74.20 | 48.05 | 40.34 | 2.88 |
| | PD-FL | 74.90 | 53.22 | 46.32 | 4.53 |
| | GSP-FL | 73.90 | 55.86 | 49.66 | 2.97 |
| | FLPurifier-GNN | 56.90 | 0.23 | -3.56 | 6.95 |
| | DMGNN-FL | 75.20 | 56.78 | 47.36 | 2.70 |
| | FedTGE | 76.80 | 82.87 | 73.91 | **177.03** |
| | **ETD-FGL** | **76.10** | **4.25** | **0.23** | **3.26** |
| **PubMed**| Clean FedAvg | 76.30 | 1.22 | -4.39 | 9.13 |
| | Attacked FedAvg | 75.30 | 17.68 | 11.22 | 11.40 |
| | PD-FL | 74.30 | 41.10 | 34.39 | 10.16 |
| | GSP-FL | 74.50 | 23.66 | 17.07 | 6.89 |
| | FLPurifier-GNN | 66.40 | 2.93 | -2.68 | 20.96 |
| | DMGNN-FL | 74.00 | 16.83 | 8.41 | 7.74 |
| | FedTGE | 71.30 | 79.27 | 66.71 | **773.29** |
| | **ETD-FGL** | **77.60** | **1.22** | **-3.78** | **6.57** |
| **Reddit**| Clean FedAvg | 86.20 | 0.11 | -0.11 | 24.02 |
| | Attacked FedAvg | 85.70 | 72.29 | 72.08 | 44.60 |
| | PD-FL | 85.90 | 73.14 | 73.04 | 46.99 |
| | GSP-FL | 85.50 | 73.14 | 73.04 | 42.95 |
| | FLPurifier-GNN | 49.30 | 0.21 | -0.11 | 45.96 |
| | DMGNN-FL | 85.70 | 72.29 | 72.08 | 43.68 |
| | FedTGE | 52.70 | 4.78 | 4.46 | **399.94** |
| | **ETD-FGL** | **85.30** | **0.85** | **0.64** | **7.41** |

*Source Verification:* `consolidated_data/baseline_seed42.csv`; `Table_02_Main_Baseline_Comparison.md`.

---

### 8.2 Table 2: Multi-Seed Robustness (Seeds 42, 43, 44)

*Note: Multi-seed baseline distributions represent **Attacked FedAvg**. No 3-seed Clean FedAvg control was evaluated in the repository.*

| Dataset | Method | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (pp) ↓ | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Attacked FedAvg | 75.00 ± 0.72 | 62.03 ± 15.38 | 52.26 ± 14.25 | 2.73 ± 0.04 |
| | **ETD-FGL** | **75.57 ± 1.57** | **5.21 ± 0.88** | **-2.22 ± 2.17** | **2.85 ± 0.01** |
| **PubMed**| Attacked FedAvg | 74.80 ± 3.18 | 9.23 ± 7.36 | 2.56 ± 7.73 | 9.44 ± 3.13 |
| | **ETD-FGL** | **75.50 ± 2.01** | **0.89 ± 0.56** | **-3.54 ± 0.53** | **10.53 ± 3.64** |
| **Reddit**| Attacked FedAvg | 84.90 ± 0.80 | 74.42 ± 1.85 | 74.06 ± 1.75 | 11.07 ± 6.58 |
| | **ETD-FGL** | **84.87 ± 0.40** | **14.08 ± 18.19** | **13.77 ± 18.09** | **7.40 ± 0.05** |

*Individual Per-Seed Values for Reddit ETD-FGL:*
- Seed 42: Acc = 85.30%, ASR = **0.85%**, Effect = 0.64 pp
- Seed 43: Acc = 84.50%, ASR = **34.82%**, Effect = 34.39 pp  *(Elevated retention in heterogeneous partition)*
- Seed 44: Acc = 84.80%, ASR = **6.58%**, Effect = 6.26 pp

*Source Verification:* `consolidated_data/multiseed_summary.csv`; `Table_03_MultiSeed_Robustness.md`.

---

### 8.3 Table 3: Standard Ablation Study (All 6 Original Variants, Seeds 42, 43, 44)

| Dataset | Variant Name | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (pp) ↓ |
| :--- | :--- | :--- | :--- | :--- |
| **Cora** | Attacked FedAvg | 75.00 ± 0.72 | 62.03 ± 15.38 | 52.26 ± 14.25 |
| | ETD-FGL (Full final) | 75.57 ± 1.57 | 5.21 ± 0.88 | -2.22 ± 2.17 |
| | ETD-FGL Topology-only | 75.40 ± 1.65 | 4.60 ± 0.90 | -3.98 ± 3.30 |
| | ETD-FGL Update-only | 74.90 ± 1.90 | 44.33 ± 8.02 | 35.86 ± 6.99 |
| | ETD-FGL w/o Trust Weighting | 75.00 ± 0.72 | 62.03 ± 15.38 | 52.26 ± 14.25 |
| | Historical Three-Channel (0.45/0.35/0.20) | 75.43 ± 1.10 | 18.93 ± 3.80 | 9.92 ± 4.53 |
| **PubMed**| Attacked FedAvg | 74.80 ± 3.18 | 9.23 ± 7.36 | 2.56 ± 7.73 |
| | ETD-FGL (Full final) | 75.50 ± 2.01 | 0.89 ± 0.56 | -3.54 ± 0.53 |
| | ETD-FGL Topology-only | 74.60 ± 3.64 | 0.81 ± 0.39 | -3.50 ± 0.69 |
| | ETD-FGL Update-only | 75.83 ± 1.93 | 6.50 ± 9.37 | 0.61 ± 7.54 |
| | ETD-FGL w/o Trust Weighting | 74.80 ± 3.18 | 9.23 ± 7.36 | 2.56 ± 7.73 |
| | Historical Three-Channel (0.45/0.35/0.20) | 75.80 ± 2.01 | 1.14 ± 0.87 | -3.86 ± 1.02 |
| **Reddit**| Attacked FedAvg | 84.90 ± 0.80 | 74.42 ± 1.85 | 74.06 ± 1.75 |
| | ETD-FGL (Full final) | 84.87 ± 0.40 | 14.08 ± 18.19 | 13.77 ± 18.09 |
| | ETD-FGL Topology-only | 84.93 ± 0.49 | 10.44 ± 16.08 | 10.16 ± 15.96 |
| | ETD-FGL Update-only | 84.80 ± 0.66 | 31.49 ± 17.73 | 31.25 ± 17.62 |
| | ETD-FGL w/o Trust Weighting | 84.90 ± 0.80 | 74.42 ± 1.85 | 74.06 ± 1.75 |
| | Historical Three-Channel (0.45/0.35/0.20) | 84.90 ± 0.62 | 21.87 ± 16.33 | 21.59 ± 16.27 |

*Source Verification:* `consolidated_data/standard_ablation_summary.csv`; `Table_04_Standard_Ablation_Study.md`.

---

### 8.4 Table 4: Controlled Scientific Ablation (Held-Constant Coefficients, Seeds 42, 43, 44)

| Dataset | Evaluated Variant | Risk Formulation $R_k$ | Clean Acc (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (pp) ↓ | Attacker Wt ($w_0$ %) ↓ | Benign Risk ($R_{benign}$) ↓ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Full ETD-FGL | $\frac{9}{13} A_{topo} + \frac{4}{13} A_{upd}$ | 75.57 ± 1.57 | 5.21 ± 0.88 | -2.22 ± 2.17 | 4.76 ± 0.03 | 0.0577 ± 0.0007 |
| | Fixed No Update | $\frac{9}{13} A_{topo}$ | 75.87 ± 1.56 | 6.40 ± 1.59 | -1.88 ± 2.76 | 4.12 ± 0.00 | **0.0000 ± 0.0000** |
| | Fixed No Topology | $\frac{4}{13} A_{upd}$ | 76.10 ± 0.87 | 42.53 ± 15.94 | 35.10 ± 14.40 | 18.41 ± 0.60 | 0.0610 ± 0.0032 |
| **PubMed**| Full ETD-FGL | $\frac{9}{13} A_{topo} + \frac{4}{13} A_{upd}$ | 75.50 ± 2.01 | 0.89 ± 0.56 | -3.54 ± 0.53 | 4.55 ± 0.04 | 0.0487 ± 0.0054 |
| | Fixed No Update | $\frac{9}{13} A_{topo}$ | 74.57 ± 3.17 | 1.18 ± 0.71 | -3.90 ± 0.49 | 4.12 ± 0.00 | **0.0000 ± 0.0000** |
| | Fixed No Topology | $\frac{4}{13} A_{upd}$ | 75.70 ± 1.90 | 4.47 ± 3.45 | -1.67 ± 3.78 | 15.76 ± 0.59 | 0.0281 ± 0.0058 |
| **Reddit**| Full ETD-FGL | $\frac{9}{13} A_{topo} + \frac{4}{13} A_{upd}$ | 84.87 ± 0.40 | 14.08 ± 18.19 | 13.77 ± 18.09 | 2.53 ± 0.08 | 0.0203 ± 0.0012 |
| | Fixed No Update | $\frac{9}{13} A_{topo}$ | 85.00 ± 0.89 | 25.19 ± 17.81 | 24.91 ± 17.65 | 4.12 ± 0.00 | **0.0000 ± 0.0000** |
| | Fixed No Topology | $\frac{4}{13} A_{upd}$ | 85.27 ± 0.81 | 66.31 ± 7.14 | 66.03 ± 7.08 | 13.24 ± 1.03 | 0.0223 ± 0.0024 |

*Source Verification:* `consolidated_data/controlled_ablation_summary.csv`; `Table_05_Controlled_Ablation_Study.md`.

---

### 8.5 Table 5: Paired Within-Seed Differences ($\Delta = \text{Variant} - \text{Full ETD-FGL}$)

| Dataset | Ablated Component | Paired Seeds | $\Delta$ Clean Acc (pp) | $\Delta$ Backdoor ASR (pp) | $\Delta$ Attack Effect (pp) | $\Delta$ Attacker Wt (pp) | $\Delta$ Benign Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Without Update ($-\frac{4}{13} A_{upd}$) | 3 | +0.30 ± 1.28 | **+1.19 ± 1.42** | +0.34 ± 0.91 | -0.64 ± 0.03 | -0.0577 ± 0.0007 |
| | Without Topology ($-\frac{9}{13} A_{topo}$) | 3 | +0.53 ± 1.17 | **+37.32 ± 15.35**| +37.32 ± 15.92 | +13.66 ± 0.58 | +0.0033 ± 0.0027 |
| **PubMed**| Without Update ($-\frac{4}{13} A_{upd}$) | 3 | -0.93 ± 1.27 | **+0.28 ± 0.19** | -0.37 ± 0.21 | -0.44 ± 0.04 | -0.0487 ± 0.0054 |
| | Without Topology ($-\frac{9}{13} A_{topo}$) | 3 | +0.20 ± 2.10 | **+3.58 ± 3.07** | +1.87 ± 3.78 | +11.21 ± 0.56 | -0.0206 ± 0.0082 |
| **Reddit**| Without Update ($-\frac{4}{13} A_{upd}$) | 3 | +0.13 ± 0.83 | **+11.11 ± 5.60**| +11.15 ± 5.57 | +1.59 ± 0.08 | -0.0203 ± 0.0012 |
| | Without Topology ($-\frac{9}{13} A_{topo}$) | 3 | +0.40 ± 0.50 | **+52.23 ± 14.61**| +52.26 ± 14.45 | +10.71 ± 1.02 | +0.0020 ± 0.0018 |

*Source Verification:* `consolidated_data/paired_differences.csv`; `Table_06_Paired_Component_Contributions.md`.

---

# SECTION 9 — SCIENTIFIC INTERPRETATION OF RESULTS

### 9.1 Topology vs. Update: Primary Driver vs. Dynamic Complement
- **Direct Empirical Observations:**
  1. Removing the topology channel ($c_{\text{topo}} = 0$) results in substantial defense degradation: mean ASR increases by **+37.32 pp** on Cora and **+52.23 pp** on Reddit. Mean attacker aggregation weight share rebounds from $\le 4.8\%$ back to $13.2\%–18.4\%$.
  2. Removing the update channel ($c_{\text{upd}} = 0$) while holding the topology coefficient constant results in an observed ASR increase of **+1.19 pp** on Cora, **+0.28 pp** on PubMed, and **+11.11 pp** on Reddit.
- **Scientific Interpretation:** Topological anomaly detection serves as the primary barrier against the evaluated structural clique backdoor. The parameter-update channel provides complementary mitigation, most visibly on Reddit where holding coefficients constant and removing update increases ASR by an average of 11.11 percentage points. Both channels contribute non-redundantly under held-constant penalization.

### 9.2 The Coefficient Normalization Artifact in Standard Ablation
- **Why Standard Topology-only Appeared Lower Than Full:** In standard ablation (`ConfigurableETDFGLAggregator`), active component weights are normalized to sum to 1.0. When the update channel was removed, the topology weight was re-normalized from $9/13 \approx 0.6923$ to $1.0$ (a **+44% coefficient inflation**). This inflated topology weight generated higher trust penalization ($T_0 = 0.078$ vs $0.172$), causing attacker weight to drop to $1.92\%$ and yielding an artificially lower sample mean ASR (4.60% vs 5.21% on Cora).
- **The Controlled Solution:** When coefficients are held strictly constant ($9/13$ for topology in both Full and Fixed No Update), removing the update channel increases mean ASR (+1.19 pp on Cora, +11.11 pp on Reddit), isolating its complementary contribution.

### 9.3 Qualification and Proof of the 5-Client Scale-Invariance Property
The scale-invariance property is qualified to the **nonzero-drift, single-attacker, fixed-client ($K=5, M=1$), and numerical-floor ($d \ge 2.5 \times 10^{-8}$)** regime:
1. **Regime Conditions:** Exactly one client exhibits topological drift ($d_0 = d \ge 2.5 \times 10^{-8}$), while the remaining $K-1 = 4$ clients exhibit zero drift ($d_1 = d_2 = d_3 = d_4 = 0.0$).
2. **Median & Absolute Deviations:** The drift vector is $[d, 0, 0, 0, 0]$. The median is $0.0$. The absolute deviations from median are $[d, 0, 0, 0, 0]$, whose median is $0.0$. Thus $1.4826 \times \text{median}(|\mathbf{v} - \text{med}|) = 0.0$.
3. **Standard Deviation Evaluation:**
   In `multidata_suite/defenses.py:430`, code evaluates:
   $$\text{MAD} = \max\left(1.4826 \cdot \text{median}(|\mathbf{v} - \text{med}|), \; \text{std}(\mathbf{v}), \; 10^{-8}\right) = \max\left(0.0, \; \text{std}(\mathbf{v}), \; 10^{-8}\right) = \max\left(\text{std}(\mathbf{v}), \; 10^{-8}\right)$$
   For values $[d, 0, 0, 0, 0]$, mean is $\bar{d} = d/5 = 0.2d$. Standard deviation is:
   $$\text{std}(\mathbf{v}) = \sqrt{\frac{1}{5} \left( (d - 0.2d)^2 + 4(0 - 0.2d)^2 \right)} = \sqrt{\frac{1}{5} (0.64 d^2 + 0.16 d^2)} = \sqrt{0.16 d^2} = 0.4 d$$
4. **Plateau Threshold Determination ($d \ge 2.5 \times 10^{-8}$):**
   The standard deviation term dominates the $10^{-8}$ floor if and only if:
   $$0.4 d \ge 10^{-8} \iff d \ge \frac{10^{-8}}{0.4} = \mathbf{2.5 \times 10^{-8}}$$
   - For all $d \ge 2.5 \times 10^{-8}$, $\text{MAD} = 0.4d$.
   - The outlier z-score is:
     $$z_0 = \frac{d - 0.0}{0.4 d} \equiv \mathbf{2.5000}$$
   - The resulting topological anomaly score is:
     $$A_0^{\text{topo}} = 2.0 \cdot \left(\frac{1}{1 + e^{-2.5}} - 0.5\right) = 2.0 \cdot (0.9241418 - 0.5) \approx \mathbf{0.848284}$$
   Thus, for all $d \ge 2.5 \times 10^{-8}$, $A_0^{\text{topo}}$ is strictly scale-invariant and independent of $d$.
5. **Continuous Sub-Threshold Regime ($0 \le d < 2.5 \times 10^{-8}$):**
   When $d < 2.5 \times 10^{-8}$, $0.4d < 10^{-8}$, so $\text{MAD} = 10^{-8}$.
   The z-score becomes:
   $$z_0 = \frac{d}{10^{-8}} = 10^8 d$$
   In this sub-threshold regime, $z_0$ and $A_0^{\text{topo}}$ vary continuously as a function of $d$. At $d = 0.0$, $z_0 = 0.0$ and $A_0^{\text{topo}} = 0.0$.
6. **Distinction Between Anomaly Score and Weight Percentage ($w_0 \equiv 4.12\%$ under Fixed No Update):**
   - **Dimensionless Anomaly Score:** $A_0^{\text{topo}} \approx 0.848284 \in [0, 1]$.
   - **Attacker Aggregation Weight Share:** In the **Fixed No Update** ablation variant ($A^{\text{upd}} = 0$), $R_0 = \frac{9}{13} \times 0.848284 \approx 0.587273$. Trust factor is $T_0 = \exp(-3 \times 0.587273) \approx 0.17173$. For benign clients ($k=1..4$), $d_k = 0 \implies A_k^{\text{topo}} = 0 \implies R_k = 0 \implies T_k = 1.0$.
   - Under equal client sample sizes ($n_i = n$), the normalized attacker weight share is:
     $$w_0 = \frac{0.17173}{0.17173 + 4.0} \times 100\% = \frac{0.17173}{4.17173} \times 100\% \equiv \mathbf{4.12\%} \quad (\sigma = 0.00\%)$$
   This exact value ($4.12\%$) appears empirically across all seeds in Table 4, validating the mathematical relationship in this regime. In the Full ETD-FGL model, dynamic update anomalies further modulate $w_0$ between 1.9% and 5.0%.
   - **Observed Update Anomaly on Cora:** In Figure F Panel (b), the attacker's model update anomaly on Cora (Seed 42) is identically zero ($A_0^{\text{upd}} \equiv 0.0000$) across all 50 rounds, showing that attacker downweighting on Cora is driven entirely by the structural topology channel.

### 9.4 Reddit Seed 43 Elevated Backdoor Retention
- **Empirical Observation:** Full ETD-FGL achieves 0.85% ASR on Seed 42 and 6.58% on Seed 44, but reaches **34.82%** on Seed 43 (Attack Effect = 34.39 pp).
- **Reporting Boundary:** Conjectured causal explanations attributing this elevated retention to intra-class degree variance or reduced trigger contrast are unsupported by experimental logs and are excluded from scientific claims. The finding is documented strictly as an empirical observation demonstrating sensitivity to client graph partitioning across random seeds.

### 9.5 Baseline Attack Penetration on PubMed
- **Observation:** On PubMed, Attacked FedAvg achieved **9.23 ± 7.36%** ASR across three seeds (17.68% on Seed 42, 5.73% on Seed 43, 4.27% on Seed 44).
- **Structural Characteristics:** PubMed is a sparse citation graph with 3 classes and 500 features. The clean target-class prediction rate is 4.35%.
- **Reporting Requirement:** Low ASR under ETD-FGL on PubMed (0.89%) must be contextualized by the weak baseline attack penetration observed in unmitigated FedAvg.

---

# SECTION 10 — INVENTORY OF EXPERIMENTAL RECORDS AND CHECKPOINTS

### 10.1 Audited Breakdown of 132 Records and 99 Distinct Checkpoints
An exhaustive cryptographic SHA-256 audit of all files in the `outputs/` hierarchy confirmed:
- **Directory Experiment Records (`final_summary.json`):** Exactly **132** run directories.
- **Checkpoint File Paths (`best_model.pt`):** Exactly **132** saved model paths on disk.
- **Distinct Checkpoint SHA-256 Hashes:** Exactly **99** unique hashes exist across the 132 checkpoint file paths on disk.
- **Legitimate Cross-Suite Baseline Reuses (33 file paths):**
  - **Attacked FedAvg Seed 42 (9 paths):** Baseline run reused in Multi-seed (3 datasets × 1), Standard Ablation (3 datasets × 1), and Controlled Ablation (3 datasets × 1).
  - **Attacked FedAvg Seeds 43 and 44 (12 paths):** Multi-seed runs reused in Standard Ablation (3 datasets × 2 seeds) and Controlled Ablation (3 datasets × 2 seeds).
  - **Full ETD-FGL Seeds 42, 43, 44 (9 paths):** Multi-seed runs reused as the Full ETD-FGL baseline in Controlled Ablation (3 datasets × 3 seeds).
  - **Baseline ETD-FGL Seed 42 (3 paths):** Baseline run reused as Seed 42 in the Multi-seed suite (3 datasets × 1).
- **Traceability Caveat:** Subtracting the 33 legitimate reuses from 132 paths yields exactly 99 unique checkpoint SHA-256 hashes on disk. This verified cryptographic property on disk is strictly distinguished from asserting proof of independent execution processes.

---

# SECTION 11 — THREATS TO VALIDITY AND RESEARCH LIMITATIONS

### 11.1 Methodological and Implementation Limitations
1. **Reference Graph Assumption:** ETD-FGL assumes the server holds an authenticated clean structural descriptor for each client's subnetwork prior to attack execution. In the simulation, descriptors are computed directly from client `Data` objects. While applicable to settings where initial client enrollment is audited, this assumption is restrictive for dynamic environments where network structure naturally evolves.
2. **Single Attacker Evaluation ($M = 1$ in $K = 5$):** All experiments evaluated a single malicious client (20% attacker ratio). The robust median and MAD estimators require benign clients to form a majority ($M < K/2$). Colluding multi-attacker scenarios ($M \ge 2$) have not been evaluated.
3. **Single Model Architecture:** All experiments used a 2-layer GCN. Transferability to GAT, GraphSAGE, or deeper GNN architectures has not been evaluated.
4. **Fixed Trigger Geometry:** Evaluated exclusively on 3-node clique ($K_3$) triggers with a fixed 20% local poisoning budget. Subgraph triggers of different sizes ($s \ne 3$) or topological motifs (trees, cycles, bipartite cliques) were not tested.
5. **Class-Stratified Partitioning:** Federated client splits rely on class labels across splits to avoid empty classes on Planetoid's small training sets. A fully label-blind partitioner was not evaluated.

---

# SECTION 12 — FIGURE-TO-RESULTS MAPPING TABLE

| Figure Filename | Layout | Dataset(s) | Method(s) | Plotted Evidence | Primary Source File | Section Placement | Neutral Descriptive Caption |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Fig_A_Baseline_Comparison_Overview.png` | 2×2 | Cora, PubMed, Reddit | 8 Baselines | Clean Acc, Backdoor ASR, Attack Effect, Log Loop Runtime | `baseline_seed42.csv` | Section 5.2 | *Figure A: Baseline evaluation of ETD-FGL and seven comparison methods on Cora, PubMed, and Reddit (Seed 42).* |
| `Fig_A1_Baseline_Comparison_Cora.png` | 2×2 | Cora | 8 Baselines | Acc, ASR, Effect (zero line), Loop Runtime (values atop bars) | `baseline_seed42.csv` | Section 5.2 / Supp | *Figure A1: Baseline comparison on Cora (Seed 42).* |
| `Fig_A2_Baseline_Comparison_PubMed.png` | 2×2 | PubMed | 8 Baselines | Acc, ASR, Effect (zero line), Loop Runtime (values atop bars) | `baseline_seed42.csv` | Section 5.2 / Supp | *Figure A2: Baseline comparison on PubMed (Seed 42).* |
| `Fig_A3_Baseline_Comparison_Reddit.png` | 2×2 | Reddit | 8 Baselines | Acc, ASR, Effect (zero line), Loop Runtime (values atop bars) | `baseline_seed42.csv` | Section 5.2 / Supp | *Figure A3: Baseline comparison on Reddit (Seed 42).* |
| `Fig_B_Standard_Ablation.png` | 2×2 | Cora, PubMed, Reddit | 6 Standard Variants | Clean Acc, ASR, Attack Effect, Attacker Weight | `consolidated_experiments.csv` | Section 5.3 | *Figure B: Standard multi-seed ablation study across six variants on Cora, PubMed, and Reddit (Seeds 42, 43, 44).* |
| `Fig_C_Controlled_Ablation.png` | 2×2 | Cora, PubMed, Reddit | 3 Controlled Variants | Backdoor ASR, Paired $\Delta$ ASR, Clean Acc, Paired $\Delta$ Acc (in pp) | `controlled_ablation_summary.csv` | Section 5.3 | *Figure C: Controlled ablation isolating evidence channels with held-constant coefficients across Cora, PubMed, and Reddit (Seeds 42, 43, 44).* |
| `Fig_D_MultiSeed_Robustness.png` | 1×3 | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Acc, ASR, Attack Effect with Reddit Seed 43 callouts | `consolidated_experiments.csv` | Section 5.2 | *Figure D: Multi-seed comparison between Attacked FedAvg and ETD-FGL across Seeds 42, 43, and 44.* |
| `Fig_E_Learning_Dynamics.png` | 2×3 | Cora, PubMed, Reddit | Clean, Attacked, FedTGE, ETD-FGL | 50-round convergence trajectories for Clean Acc and ASR | `training_history.csv` | Section 5.4 | *Figure E: Federated learning dynamics over 50 communication rounds on Cora, PubMed, and Reddit (Seed 42).* |
| `Fig_F_Trust_Defense_Mechanisms.png` | 2×2 | Cora, PubMed, Reddit | ETD-FGL | Weight suppression, risk decomposition (near-zero update anomaly on Cora), benign trust, qualified scale-invariance ($d \ge 2.5 \times 10^{-8}$) | `training_history.csv` | Section 4 / 5.4 | *Figure F: ETD-FGL defense mechanism dynamics (near-zero update anomaly on Cora) and 5-client analytic anomaly regime.* |
| `Fig_G_Attack_Effect_and_Defense_Gain.png` | 1×3 | Cora, PubMed, Reddit | Baselines, ETD-FGL | Trigger Attack Effect, Absolute ASR Drop, Relative Reduction % | `baseline_seed42.csv`, `multiseed_summary.csv` | Section 5.2 | *Figure G: Trigger Attack Effect and quantified defense improvements over unmitigated FedAvg.* |
| `Fig_H_Accuracy_ASR_Tradeoff.png` | 1×3 | Cora, PubMed, Reddit | Baselines + Multiseed | Accuracy vs ASR trade-off by dataset; 2D error whiskers | `baseline_seed42.csv`, `multiseed_summary.csv` | Section 5.2 | *Figure H: Clean accuracy versus backdoor robustness (ASR) trade-off plotted separately by dataset.* |
| `Fig_I_Training_Runtime_Comparison.png` | 1×2 | Cora, PubMed, Reddit | 8 Baselines | Multi-dataset log-scale + PubMed linear; FedTGE unclipped | `baseline_seed42.csv` | Section 5.5 | *Figure I: Recorded federated training-loop runtime over 50 communication rounds (Seed 42).* |
| `Fig_S_Reddit_Seed_Heterogeneity.png` | 1×3 | Reddit | Controlled Variants | Per-seed breakdown for Seeds 42, 43, 44 | `consolidated_experiments.csv` | Supplementary | *Supplementary Figure S1: Reddit Per-Seed Backdoor ASR across Controlled Variants.* |
| `Fig_S_Standard_vs_Controlled_Comparison.png` | 1×2 | Cora, PubMed, Reddit | Standard vs Controlled | Topology and Update channel comparison under normalized vs fixed | `standard_ablation_summary.csv` | Supplementary | *Supplementary Figure S2: Standard vs Controlled Ablation (Impact of Coefficient Normalization).* |

---

# SECTION 13 — UNRESOLVED RESEARCH QUESTIONS AND OPEN ITEMS

| Item / Open Question | Category | Nature of Ambiguity / Recommendation |
| :--- | :--- | :--- |
| **Descriptor-Only Authenticated Network Exchange** | Architectural Scope | In simulation, server evaluates descriptors directly from client graph objects. Implementing and testing a cryptographically authenticated client-side descriptor exchange is recommended for future systems research. |
| **Label-Blind Graph Partitioning** | Future Work | Current partitioning uses label stratification to avoid empty training classes on Planetoid. Evaluating Metis graph partitioning or Dirichlet partitioning is recommended for future research. |
| **Colluding Malicious Clients ($M \ge 2$)** | Future Work | All 132 runs evaluated exactly $M = 1$ in $K = 5$. Multi-client collusive poisoning requires future empirical validation. |
| **Dynamic Graph Topologies** | Deployment Scope | Method assumes static client graphs where pre-attack descriptors are recorded at enrollment. The manuscript should state this deployment scope explicitly. |
| **GNN Architecture Generalization** | Future Work | Codebase evaluates a 2-layer GCN. Evaluating GAT, GraphSAGE, or GIN requires new training runs. |
| **Trigger Size and Poisoning Ratio Sweeps** | Boundary | Sweeps across $s \in \{2, 4, 5\}$ and $\rho \in \{0.05, 0.10, 0.30\}$ were not executed in the 132 consolidated runs. |

---

# SECTION 14 — MANUSCRIPT-READY FACTUAL OUTLINE

This section provides an objective, evidence-based structural outline for manual manuscript revision:

### 1. Abstract
- State the security challenge of targeted structural backdoor attacks in Federated Graph Learning (FGL).
- Note that parameter-space aggregation defenses face challenges in isolating structural backdoor perturbations from non-IID graph variance.
- Introduce ETD-FGL: server-side aggregation combining standardized topological drift with coordinate-wise update medians.
- Summarize verified results: reduces mean ASR from 62.03% to 5.21% on Cora, 9.23% to 0.89% on PubMed, and 74.42% to 14.08% on Reddit (0.85% on Seed 42). Clean accuracy remains within 1.30 pp of unattacked Clean FedAvg on Seed 42 (Cora 0.00 pp, PubMed +1.30 pp, Reddit -0.90 pp) and tracks Attacked FedAvg within normal variance across seeds. Training loop runtime remains under 11s across all suites, avoiding the high latency of graph-entropy baselines (FedTGE reaches 177s to 773s).

### 2. Introduction
- Paragraph 1: Context of decentralized graph learning applications and privacy constraints.
- Paragraph 2: Vulnerability of GNNs to structural clique backdoors; limitations of parameter-space defenses in graph settings.
- Paragraph 3: Trade-offs in existing graph defenses: FLPurifier exhibits clean accuracy degradation in evaluated settings (down to 49.3%), while FedTGE incurs high computational latency (up to 773s for 50 rounds).
- Paragraph 4: Proposed ETD-FGL approach: dual-channel anomaly fusion and exponential trust weighting.
- Paragraph 5: Summary of concrete scientific contributions.

### 3. Related Work
- Subsection 3.1: Federated Graph Learning paradigms and non-IID partitioning.
- Subsection 3.2: Backdoor attacks on graph neural networks (subgraph triggers, feature triggers).
- Subsection 3.3: Byzantine-robust federated defenses (parameter-space filtering vs graph-tailored mechanisms).

### 4. System and Threat Model
- Subsection 4.1: Federated node classification setup ($K = 5$ clients, 2-layer GCN, synchronous FedAvg).
- Subsection 4.2: Threat model ($M = 1$ malicious client, 20% local poisoning budget, 3-node clique trigger, target class $y^* = 0$).
- Subsection 4.3: Reference graph availability assumption, simulation access mechanism, and deployment scope.

### 5. Proposed ETD-FGL Method
- Subsection 5.1: 5-dimensional label-free structural descriptor vector.
- Subsection 5.2: Standardized topological drift computation.
- Subsection 5.3: One-sided robust positive MAD mapping (`_robust_positive`).
- Subsection 5.4: Coordinate-wise parameter update median and update anomaly.
- Subsection 5.5: Convex risk fusion ($9/13$ topology, $4/13$ update) and exponential trust factor calculation.
- Subsection 5.6: Sample-weighted aggregation and theoretical derivation of the 5-client scale-invariance property ($d \ge 2.5 \times 10^{-8}$).

### 6. Experimental Setup
- Subsection 6.1: Benchmark datasets (Cora, PubMed, Sampled Reddit) and statistics.
- Subsection 6.2: Baseline methods and parameter configurations (7 comparison methods; learning rate $\eta=0.01$ for Cora/PubMed, $\eta=0.005$ for Reddit).
- Subsection 6.3: Evaluation metrics (Clean Accuracy, Backdoor ASR, Trigger Attack Effect, Attacker Weight, Loop Runtime).
- Subsection 6.4: Reproducibility protocols, random seeds (42, 43, 44), and audit of 132 run directories (99 unique checkpoint hashes on disk, 33 legitimate baseline reuses).

### 7. Results and Discussion
- Subsection 7.1: Overall baseline comparison on Seed 42 (referencing Figure A, A1–A3, and Table 1).
- Subsection 7.2: Multi-seed evaluation vs Attacked FedAvg and empirical discussion of Reddit Seed 43 partition sensitivity (referencing Figure D and Table 2).
- Subsection 7.3: Accuracy vs Robustness trade-off (referencing Figure H).
- Subsection 7.4: Federated learning dynamics over 50 rounds (referencing Figure E).
- Subsection 7.5: Defense mechanism dynamics, weight suppression, and scale-invariance (referencing Figure F; note near-zero update anomaly on Cora).
- Subsection 7.6: Computational loop runtime analysis (referencing Figure I).

### 8. Ablation Studies
- Subsection 8.1: Standard ablation study across 6 original variants (referencing Figure B and Table 3).
- Subsection 8.2: Controlled ablation with held-constant coefficients isolating channel contributions (referencing Figure C, Tables 4–5, and Figure S2).

### 9. Threats to Validity and Limitations
- Detail the reference graph requirement, simulation graph access mechanism, single-attacker scope, 2-layer GCN architecture, and class-stratified partitioning.

### 10. Conclusion
- Conclude with a factual summary of ETD-FGL's empirical defense performance and future directions for dynamic and collusive settings.
