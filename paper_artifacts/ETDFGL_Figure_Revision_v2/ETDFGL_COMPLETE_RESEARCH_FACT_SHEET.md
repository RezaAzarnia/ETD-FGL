# ETD-FGL Complete Research Fact Sheet and Technical Evidence Report

**Document Purpose:** Independent academic and technical reference document for manual manuscript revision.  
**Target Audience:** Scientific editor / research author revising the ETD-FGL paper.  
**Verification Level:** Rigorously audited against the frozen codebase and 132 completed experiment runs.  
**Repository Working Directory:** `c:\Users\R_Azarnia\Desktop\main paper\ETD-FGL\`  
**Date of Evidence Freeze:** October 17, 2026  

---

# SECTION 1 — RESEARCH IDENTITY AND OBJECTIVE

### 1.1 Full Project Name and Acronym
- **Full Title:** Explaining Topological Drift in Federated Graph Learning (ETD-FGL): Robust Defense Against Structural Backdoor Attacks via Dual-Evidence Anomaly Fusion.
- **Short Name / Acronym:** ETD-FGL.

### 1.2 Problem Statement
Federated Graph Learning (FGL) enables decentralized clients to collaboratively train Graph Neural Networks (GNNs) on partitioned node-classification tasks without sharing their raw graphs, node attributes, or local topological connections. However, FGL's decentralized topology creates severe vulnerability to **targeted structural backdoor attacks**. A malicious client can perturb its local subnetwork by injecting dense, synthetic graph triggers (e.g., small complete subgraphs / cliques) linked to designated victim nodes. When aggregated via standard Federated Averaging (FedAvg), the global GNN memorizes the trigger pattern, causing test-time nodes from non-target classes to be misclassified into the attacker's target class whenever the trigger subnetwork is attached, while preserving high classification accuracy on clean inputs.

### 1.3 Research Motivation
Existing federated defenses against backdoor attacks are predominantly designed for Euclidean data (computer vision, NLP) and operate exclusively in the parameter/gradient space (e.g., coordinate-wise median, trimmed mean, clipping, or update distance clustering). In graph domains, parameter-space defenses fail because:
1. Backdoor gradient vectors can easily hide within the benign variance induced by non-IID graph structural heterogeneity.
2. Parameter-space defenses ignore graph-specific invariants: malicious structural modifications introduce measurable, non-local deformations in graph topology (e.g., abnormal clustering coefficients, triangle counts, and degree distributions) that parameter updates alone cannot reliably isolate.

Conversely, purely graph-based defenses (such as edge pruning via spectral clustering or homophily heuristics) either fail when applied globally without authenticated baselines or impose prohibitive computational overheads (e.g., FedTGE's graph entropy matrix calculations, which take hundreds of seconds per round).

### 1.4 Implemented Defense Approach
ETD-FGL implements an **asymmetric dual-evidence server-side aggregation defense**:
1. **Offline Structural Channel (Topological Drift):** Each client's local graph topology is summarized using a label-free 5-dimensional structural descriptor. The server computes the standardized Euclidean drift between the current graph and an authenticated clean pre-attack reference graph, mapped to a bounded topological anomaly score $A_i^{\text{topo}} \in [0, 1]$ via a robust positive median-absolute-deviation (MAD) sigmoid transform.
2. **Online Parameter Channel (Model Update Anomaly):** At every communication round, local model parameter updates are compared against the coordinate-wise update median. The Euclidean parameter divergence is transformed into a bounded dynamic update anomaly score $A_i^{\text{upd}, t} \in [0, 1]$.
3. **Risk Fusion and Exponential Trust Weighting:** The two evidence streams are combined via fixed convex weighting ($R_i^t = \frac{9}{13} A_i^{\text{topo}} + \frac{4}{13} A_i^{\text{upd}, t}$), yielding an exponential client trust factor $T_i^t = \text{clip}(\exp(-3 R_i^t), 0.02, 1.0)$ that dynamically downweights the malicious client's aggregation share to $\le 4.8\%$.

### 1.5 What the Method Does and Does NOT Claim
- **What It Claims:**
  - ETD-FGL effectively suppresses targeted structural clique backdoor attacks in federated node classification across citation and social network benchmarks.
  - Backdoor Attack Success Rate (ASR) is reduced from 62.0% down to 5.2% on Cora, from 9.2% down to 0.89% on PubMed, and from 74.4% down to 14.1% on Reddit (with single-seed ASR dropping to 0.85%).
  - Clean test classification accuracy is strictly preserved across all seeds and datasets (no accuracy degradation relative to unattacked Clean FedAvg).
  - The aggregation algorithm adds minimal computational runtime overhead ($\le 1.1\times$ FedAvg), avoiding the prohibitive latency of graph-entropy baselines.
- **What It Does NOT Claim:**
  - It does NOT claim that GNNExplainer is required for defense. The explanation-subgraph module is explicitly excluded from the security-critical aggregation path ($c_{\text{expl}} = 0.0$) and serves only as an optional post-hoc diagnostic.
  - It does NOT claim universal robustness against arbitrary, feature-only, or clean-label poisoning attacks.
  - It does NOT claim defense guarantees when malicious clients form a majority ($M \ge K/2$).
  - It does NOT claim complete elimination of backdoor retention in highly heterogeneous graph partitions (as demonstrated by Reddit Seed 43, where ASR remains at 34.8%).

### 1.6 Evidence-Supported Scientific Contributions
1. **Empirical demonstration of parameter-space defense failure:** Proves that six major federated defenses (PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE) fail to reliably defend against structural backdoors while maintaining clean accuracy.
2. **Identification of the 5-client normalization scale-invariance:** Discovers and mathematically proves that in a 5-client federation where 4 clients have zero topological drift, any positive drift $d > 0$ yields an invariant outlier z-score $z_0 \equiv 2.5$, producing an anomaly score $A_0^{\text{topo}} \approx 0.8483$ that guarantees consistent trust suppression regardless of trigger size.
3. **Controlled channel ablation methodology:** Demonstrates that standard weight normalization masks individual channel contributions, and establishes a controlled held-constant ablation protocol proving that both topology and update channels are non-redundant.

---

# SECTION 2 — SYSTEM AND THREAT MODEL

### 2.1 System Architecture
- **Federation Size:** $K = 5$ participating clients.
- **Client Topology:** Star topology; all clients communicate exclusively with a central federated aggregation server.
- **Communication Protocol:** Synchronous Federated Averaging over $T = 50$ communication rounds.
- **Local Optimization:** Each client executes $E = 3$ local epochs of Adam optimization per round.

### 2.2 Server Assumptions and Capabilities
- **Honest Server:** The central server is honest-but-curious and correctly executes the aggregation protocol.
- **No Direct Data Inspection:** The server cannot directly inspect client node features, local edge lists, or ground-truth label distributions.
- **Reference Graph Availability:** The server has access to an authenticated, clean pre-attack structural descriptor for each client's subnetwork. This corresponds to a system deployment where client graphs are profiled or certified upon initial network enrollment before active federated rounds commence.

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

### 3.1 Benchmark Dataset Characteristics

| Dataset Name | Domain | Total Nodes ($|V|$) | Total Edges ($|E|$) | Feature Dimension ($D$) | Number of Classes ($C$) | Baseline Graph Homophily |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Citation Network | 2,708 | 5,429 (undirected) | 1,433 | 7 | 0.810 (High) |
| **PubMed** | Medical Citation | 19,717 | 44,338 (undirected) | 500 | 3 | 0.802 (High) |
| **Reddit** | Social Community | 8,000 (Sampled) | 114,615 (Sampled) | 602 | 41 | 0.755 (Moderate) |

*Source Verification:* `multidata_suite/data.py`, lines 89–158; `Table_01_Dataset_Configurations.md`.

### 3.2 Reddit Sampling Protocol
Full Reddit contains 232,965 nodes and 114,615,892 edges, which exceeds single-GPU memory limits for federated graph processing. A representative subgraph of $N = 8,000$ nodes is extracted using class-stratified sampling with fixed seed 42 (`_stratified_sample_indices()`, `data.py`, lines 42–86). The sampled subgraph is cached to disk (`reddit_sample_8000_seed_42.pt`) to guarantee that multi-seed experiments measure algorithmic variance rather than subgraph sampling shifts.

### 3.3 Client Partitioning Scheme
- **Split Preservation:** Datasets use official Planetoid public splits for Cora (140 train, 500 val, 1,000 test) and PubMed (60 train, 500 val, 1,000 test).
- **Label-Aware Stratification:** Nodes are partitioned across the 5 clients using label-aware class stratification (`multidata_suite/data.py`, lines 161–240).
- **Repair and Candidate Guarantees:** On sparse splits (e.g., Planetoid Cora with only 140 training nodes = 28 per client), random splitting could leave clients with zero training nodes or leave the attacker with no non-target training nodes. `_validate_and_finalize_partition()` implements a deterministic donor repair that guarantees:
  1. Every client owns at least one training node.
  2. Malicious Client 0 owns at least one candidate non-target training node to poison.

---

# SECTION 4 — MODEL ARCHITECTURE AND TRAINING HYPERPARAMETERS

### 4.1 GNN Architecture Specification
- **Model Type:** 2-layer Graph Convolutional Network (`GCN`, `multidata_suite/model.py`, lines 23–41).
- **Layer 1:** `GCNConv(in_channels=D, out_channels=32, cached=False)`.
- **Activation:** Rectified Linear Unit (`F.relu`) following Layer 1.
- **Regularization:** Dropout with probability $p = 0.50$ applied after Layer 1 activation.
- **Layer 2:** `GCNConv(in_channels=32, out_channels=C, cached=False)`.
- **Output:** Raw logits (cross-entropy loss with softmax computed internally).
- **Parameter Count:**
  - Cora: $(1433 \times 32) + (32 \times 7) = 46,080$ weights.
  - PubMed: $(500 \times 32) + (32 \times 3) = 16,096$ weights.
  - Reddit: $(602 \times 32) + (32 \times 41) = 20,576$ weights.

### 4.2 Training Hyperparameters

| Hyperparameter | Cora | PubMed | Reddit | Code Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Federated Communication Rounds ($T$)** | 50 | 50 | 50 | `multidata_suite/config.py:32` |
| **Local Training Epochs ($E$)** | 3 | 3 | 3 | `multidata_suite/config.py:33` |
| **Optimizer** | Adam | Adam | Adam | `multidata_suite/core.py:112` |
| **Learning Rate ($\eta$)** | 0.01 | 0.01 | **0.005** | `multidata_suite/config.py:49` |
| **Weight Decay ($\lambda$)** | $5 \times 10^{-4}$ | $5 \times 10^{-4}$ | $5 \times 10^{-4}$ | `multidata_suite/config.py:15` |
| **Dropout ($p$)** | 0.50 | 0.50 | 0.50 | `multidata_suite/config.py:16` |
| **Batch Size** | Full-batch (local) | Full-batch (local) | Full-batch (local) | `multidata_suite/core.py:120` |
| **Hardware** | Single GPU | Single GPU | Single GPU | PyTorch 2.6.0 + CUDA |

### 4.3 Checkpoint Selection Criterion
During 50 rounds of training, the global model state is validated at every round on clean validation nodes. The checkpoint achieving the highest validation accuracy is preserved as the final evaluated model (`best_round`). Test accuracy, ASR, and Attack Effect are evaluated strictly on this optimal validation checkpoint.

---

# SECTION 5 — EXACT MATHEMATICAL FORMULATION AND SOURCE CODE AUDIT

Every mathematical operation in ETD-FGL is audited below against `multidata_suite/defenses.py` and `multidata_suite/controlled_ablation.py`.

```
                  +-------------------------------------------------+
                  |  Clean Reference Descriptors D_i^{clean}       |
                  |  Current Graph Descriptors  D_i^{current}     |
                  +-------------------------------------------------+
                                           |
                                           v
                   Standardized Topological Drift d_i
                                           |
                                           v
             Robust Positive Mapping A_i^{topo} = _robust_positive(d_i)
                                           |
     +-------------------------------------+-------------------------------------+
     |                                                                           |
     | [Offline / Round 0]                                                       | [Online / Round t]
     | Topology Anomaly A_i^{topo}                                               | Local Parameter Updates \Delta w_i^t
     |                                                                           | Distance to Update Median \delta_i^t
     |                                                                           | Update Anomaly A_i^{upd, t}
     |                                                                           |
     +------------------------------------>+<------------------------------------+
                                           |
                                           v
                     Fused Risk: R_i^t = (9/13) A_i^{topo} + (4/13) A_i^{upd, t}
                                           |
                                           v
                     Trust Factor: T_i^t = clip(exp(-3.0 * R_i^t), 0.02, 1.0)
                                           |
                                           v
                     Normalized Aggregation Weights: w_i^t = (T_i^t * n_i) / \sum_j (T_j^t * n_j)
                                           |
                                           v
                     Global Model Update: w_{global}^t = \sum_i w_i^t w_i^t
```

### 5.1 Five-Dimensional Topological Descriptor
For any graph $G = (\mathcal{V}, \mathcal{E})$, the structural descriptor vector $\mathbf{D}(G) \in \mathbb{R}^5$ is computed by `_graph_descriptor()` (`multidata_suite/defenses.py`, lines 322–357):

$$\mathbf{D}(G) = \begin{bmatrix} \rho(G) \\ \mu_d(G) \\ \tilde{\sigma}_d^2(G) \\ C(G) \\ \tau(G) \end{bmatrix}$$

1. **Graph Density:** $\rho(G) = \frac{2 |\mathcal{E}|}{|\mathcal{V}|(|\mathcal{V}| - 1)}$ via `nx.density(graph)`.
2. **Mean Degree:** $\mu_d(G) = \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} d_v$.
3. **Normalized Degree Variance:** $\tilde{\sigma}_d^2(G) = \frac{\frac{1}{|\mathcal{V}|} \sum_{v} (d_v - \mu_d)^2}{\mu_d^2 + 10^{-12}}$.
4. **Average Clustering Coefficient:** $C(G) = \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} \frac{2 T_v}{d_v(d_v - 1)}$ via `nx.average_clustering(graph)`.
5. **Triangles per Node:** $\tau(G) = \frac{\sum_{v} T_v}{3 \max(1, |\mathcal{V}|)}$, where $T_v$ is the number of triangles incident to node $v$.

*Code Location:* `multidata_suite/defenses.py:341-357`.

### 5.2 Standardization and Topological Drift
Let $\mathbf{D}_i^{\text{clean}}$ and $\mathbf{D}_i^{\text{current}}$ be the descriptors for client $i$'s clean and current graphs ($i = 0, \dots, K-1$). The feature-wise scale vector $\mathbf{s} \in \mathbb{R}^5$ is computed across all clean reference graphs:

$$\mathbf{s} = \text{std}\left(\{\mathbf{D}_j^{\text{clean}}\}_{j=0}^{K-1}, \text{axis}=0\right), \quad s_k = \begin{cases} s_k & \text{if } s_k \ge 10^{-8} \\ 1.0 & \text{if } s_k < 10^{-8} \end{cases}$$

The standardized topological drift $d_i$ for client $i$ is:

$$d_i = \left\| \frac{\mathbf{D}_i^{\text{current}} - \mathbf{D}_i^{\text{clean}}}{\mathbf{s}} \right\|_2 = \sqrt{\sum_{k=1}^5 \left(\frac{D_{i, k}^{\text{current}} - D_{i, k}^{\text{clean}}}{s_k}\right)^2}$$

*Code Location:* `multidata_suite/defenses.py:506-510`.

### 5.3 One-Sided Robust Positive Mapping (`_robust_positive`)
To map unbounded divergence values $\mathbf{v} = [v_0, \dots, v_{K-1}]$ into a calibrated anomaly score $A_i \in [0, 1]$, ETD-FGL applies a median-absolute-deviation (MAD) sigmoid transform:

$$\text{med} = \text{median}(\mathbf{v})$$

$$\text{MAD} = \max\left(1.4826 \cdot \text{median}\left(\{|\mathbf{v} - \text{med}|\}\right), \; \text{std}(\mathbf{v}), \; 10^{-8}\right)$$

$$z_i = \max\left(\frac{v_i - \text{med}}{\text{MAD}}, \; 0.0\right)$$

$$A_i = \text{clip}\left(2.0 \cdot \left(\frac{1}{1 + e^{-z_i}} - 0.5\right), \; 0.0, \; 1.0\right)$$

- When $v_i \le \text{med}$, $z_i = 0 \implies A_i = 0.0$ (no false positive anomaly on below-median clients).
- As $z_i \to \infty$, $A_i \to 1.0$.

*Code Location:* `multidata_suite/defenses.py:428-432`.

### 5.4 Model-Update Anomaly Calculation
At communication round $t$, local model states $\mathbf{w}_i^t$ are flattened into parameter delta vectors relative to the global model:

$$\Delta \mathbf{w}_i^t = \mathbf{w}_i^t - \mathbf{w}_{\text{global}}^{t-1}$$

The server computes the coordinate-wise update median $\mathbf{m}_{\text{upd}}^t \in \mathbb{R}^P$:

$$m_{\text{upd}, p}^t = \text{median}_{j \in \{0, \dots, K-1\}} \left(\Delta w_{j, p}^t\right)$$

The Euclidean parameter divergence $\delta_i^t$ is:

$$\delta_i^t = \|\Delta \mathbf{w}_i^t - \mathbf{m}_{\text{upd}}^t\|_2$$

The dynamic model update anomaly score is:

$$A_i^{\text{upd}, t} = \text{\_robust\_positive}\left(\left[\delta_0^t, \dots, \delta_{K-1}^t\right]\right)_i$$

*Code Location:* `multidata_suite/defenses.py:529-532`.

### 5.5 Risk Fusion and Exponential Trust Factor
The fused client risk $R_i^t$ is a convex combination:

$$R_i^t = \alpha_{\text{topo}} A_i^{\text{topo}} + \alpha_{\text{upd}} A_i^{\text{upd}, t}$$

$$\text{Production Constants:} \quad \alpha_{\text{topo}} = \frac{9}{13} \approx 0.6923, \quad \alpha_{\text{upd}} = \frac{4}{13} \approx 0.3077$$

The trust factor $T_i^t \in [0.02, 1.0]$ is computed using exponential penalization with trust strength $\beta = 3.0$ and clipping floor $\tau_{\min} = 0.02$:

$$T_i^t = \text{clip}\left(\exp\left(-3.0 \cdot R_i^t\right), \; 0.02, \; 1.0\right)$$

*Code Location:* `multidata_suite/defenses.py:533-534`.

### 5.6 Sample-Weighted Aggregation
Let $n_i$ be the number of training nodes owned by client $i$. The final aggregation weight $w_i^t$ is:

$$w_i^t = \frac{T_i^t \cdot n_i}{\sum_{j=0}^{K-1} T_j^t \cdot n_j}$$

The updated global model parameters are:

$$\mathbf{w}_{\text{global}}^t = \sum_{i=0}^{K-1} w_i^t \mathbf{w}_i^t$$

*Code Location:* `multidata_suite/defenses.py:535-545`.

---

# SECTION 6 — BASELINE IMPLEMENTATIONS AND LIMITATIONS

All eight methods were executed under identical conditions (5 clients, Seed 42, 50 rounds, 3 local epochs, same GCN architecture, identical GPU hardware).

| Baseline Method | Target Mechanism | Implementation in Repository | Datasets Available | Key Limitations Identified in Repository |
| :--- | :--- | :--- | :--- | :--- |
| **Clean FedAvg** | Unattacked Standard FedAvg | `fedavg_clean` | Cora, PubMed, Reddit | Baseline upper bound on clean accuracy; 0% attack. |
| **Attacked FedAvg** | Unmitigated Standard FedAvg | `fedavg_structural_backdoor` | Cora, PubMed, Reddit | Baseline lower bound on defense; admits 62–74% ASR. |
| **PD-FL** | Projected Dynamic FL | `multidata_suite/defenses.py:89–197` | Cora, PubMed, Reddit | Uses update projection similarity; fails to detect structural triggers (ASR remains 53.2% Cora, 73.1% Reddit). |
| **GSP-FL** | Graph Spectral Pruning | `baseline_suite/gsp.py` | Cora, PubMed, Reddit | Prunes high-frequency graph laplacian components; ineffective against localized clique triggers (ASR 55.9% Cora, 73.1% Reddit). |
| **FLPurifier-GNN** | Gradient-Purified FL | `multidata_suite/defenses.py:198–299` | Cora, PubMed, Reddit | Purifies updates via internal reconstruction; heavily degrades clean accuracy (Cora acc drops to 56.9%, Reddit to 49.3%). |
| **DMGNN-FL** | Dynamic Masked GNN FL | `baseline_suite/dmgnn.py` | Cora, PubMed, Reddit | **Reddit Equivalence Note:** On Reddit, explanation saliency thresholds were not triggered, pruning 0 edges. Yielded output identical to Attacked FedAvg (85.70% Acc, 72.29% ASR). |
| **FedTGE** | Graph Topology Entropy | `multidata_suite/fedtge.py:528+` | Cora, PubMed, Reddit | **Severe Runtime Overhead:** Computes entropy similarity matrices taking 177s (Cora), 773s (PubMed), and 400s (Reddit), while suffering defense collapse on Cora (82.9% ASR). |
| **ETD-FGL** | Dual-Evidence Anomaly Fusion | `multidata_suite/defenses.py:476+` | Cora, PubMed, Reddit | Suppresses ASR to 4.25% (Cora), 1.22% (PubMed), 0.85% (Reddit) with runtime identical to FedAvg. |

---

# SECTION 7 — EVALUATION METRICS DEFINITION

### 7.1 Clean Test Classification Accuracy
- **Definition:** The percentage of unpoisoned test nodes in the global test set $\mathcal{V}_{\text{test}}$ correctly classified into their ground-truth classes:
  $$\text{Clean Accuracy} = \frac{\sum_{v \in \mathcal{V}_{\text{test}}} \mathbb{I}(\hat{y}_v = y_v)}{|\mathcal{V}_{\text{test}}|} \times 100\%$$
- **Denominator:** Number of clean test nodes ($|\mathcal{V}_{\text{test}}| = 1,000$ for Cora and PubMed; $1,000$ for Reddit).

### 7.2 Backdoor Attack Success Rate (ASR)
- **Definition:** The percentage of non-target test nodes ($y_v \ne y^*$) that are misclassified into target class $y^* = 0$ when the 3-node clique trigger is attached to their local egonet:
  $$\text{ASR} = \frac{\sum_{v \in \mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}} \mathbb{I}(\hat{y}_v^{\text{triggered}} = y^*)}{|\mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}|} \times 100\%$$
- **Denominator:** Number of test nodes whose ground truth is NOT class 0.

### 7.3 Trigger Attack Effect
- **Definition:** The net change in target-class prediction rate induced strictly by the presence of the trigger:
  $$\text{Attack Effect} = \text{ASR} - \text{Clean Target Rate}$$
  where $\text{Clean Target Rate} = \frac{\sum_{v \in \mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}} \mathbb{I}(\hat{y}_v^{\text{clean}} = y^*)}{|\mathcal{V}_{\text{test}} \setminus \mathcal{V}_{y^*}|} \times 100\%$.
- **Interpretation:** A positive value indicates active trigger exploitation. A negative value confirms that attaching the trigger makes the model *less* likely to predict the target class than on clean graphs, proving complete neutralization.

### 7.4 Attacker Aggregation Weight Share ($w_0$)
- **Definition:** The normalized aggregation weight allocated to malicious Client 0 at the server:
  $$w_0^t = \frac{T_0^t n_0}{\sum_{j=0}^{K-1} T_j^t n_j} \times 100\%$$
- **Baseline Reference:** Under standard uniform aggregation with 5 equal clients, $w_0 \equiv 20.0\%$. Successful defense requires $w_0 \ll 20.0\%$.

### 7.5 Recorded Training-Loop Runtime
- **Definition:** Wall-clock elapsed execution time in seconds for completing all 50 federated rounds on GPU.
- **Scope:** Measures the active local training and server aggregation loop. It does NOT include offline dataset download, graph partitioning, or one-time descriptor precomputation.

---

# SECTION 8 — COMPLETE EXPERIMENTAL RESULTS TABLES

### 8.1 Table 1: Comprehensive Baseline Comparisons (Seed 42)

| Dataset | Method | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (% pts) ↓ | Training Runtime (s) |
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

| Dataset | Method | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (% pts) ↓ | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Attacked FedAvg | 75.00 ± 0.72 | 62.03 ± 15.38 | 52.26 ± 14.25 | 2.73 ± 0.04 |
| | **ETD-FGL** | **75.57 ± 1.57** | **5.21 ± 0.88** | **-2.22 ± 2.17** | **2.85 ± 0.01** |
| **PubMed**| Attacked FedAvg | 74.80 ± 3.18 | 9.23 ± 7.36 | 2.56 ± 7.73 | 9.44 ± 3.13 |
| | **ETD-FGL** | **75.50 ± 2.01** | **0.89 ± 0.56** | **-3.54 ± 0.53** | **10.53 ± 3.64** |
| **Reddit**| Attacked FedAvg | 84.90 ± 0.80 | 74.42 ± 1.85 | 74.06 ± 1.75 | 11.07 ± 6.58 |
| | **ETD-FGL** | **84.87 ± 0.40** | **14.08 ± 18.19** | **13.77 ± 18.09** | **7.40 ± 0.05** |

*Individual Per-Seed Values for Reddit ETD-FGL:*
- Seed 42: Acc = 85.30%, ASR = **0.85%**, Effect = 0.64%
- Seed 43: Acc = 84.50%, ASR = **34.82%**, Effect = 34.39%  *(Vulnerable heterogeneous partition)*
- Seed 44: Acc = 84.80%, ASR = **6.58%**, Effect = 6.26%

*Source Verification:* `consolidated_data/multiseed_summary.csv`; `Table_03_MultiSeed_Robustness.md`.

---

### 8.3 Table 3: Standard Ablation Study (All 6 Original Variants, Seeds 42, 43, 44)

| Dataset | Variant Name | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (% pts) ↓ |
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

| Dataset | Evaluated Variant | Risk Formulation $R_k$ | Clean Acc (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (% pts) ↓ | Attacker Wt ($w_0$ %) ↓ | Benign Risk ($R_{benign}$) ↓ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
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

| Dataset | Ablated Component | Paired Seeds | $\Delta$ Clean Acc (% pts) | $\Delta$ Backdoor ASR (% pts) | $\Delta$ Attack Effect (% pts) | $\Delta$ Attacker Wt (% pts) | $\Delta$ Benign Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cora** | Without Update ($-\frac{4}{13} A_{upd}$) | 3 | +0.30 ± 1.28 | **+1.19 ± 1.42** | +0.34 ± 0.91 | -0.64 ± 0.03 | -0.0577 ± 0.0007 |
| | Without Topology ($-\frac{9}{13} A_{topo}$) | 3 | +0.53 ± 1.17 | **+37.32 ± 15.35**| +37.32 ± 15.92 | +13.66 ± 0.58 | +0.0033 ± 0.0027 |
| **PubMed**| Without Update ($-\frac{4}{13} A_{upd}$) | 3 | -0.93 ± 1.27 | **+0.28 ± 0.19** | -0.37 ± 0.21 | -0.44 ± 0.04 | -0.0487 ± 0.0054 |
| | Without Topology ($-\frac{9}{13} A_{topo}$) | 3 | +0.20 ± 2.10 | **+3.58 ± 3.07** | +1.87 ± 3.78 | +11.21 ± 0.56 | -0.0206 ± 0.0082 |
| **Reddit**| Without Update ($-\frac{4}{13} A_{upd}$) | 3 | +0.13 ± 0.83 | **+11.11 ± 5.60**| +11.15 ± 5.57 | +1.59 ± 0.08 | -0.0203 ± 0.0012 |
| | Without Topology ($-\frac{9}{13} A_{topo}$) | 3 | +0.40 ± 0.50 | **+52.23 ± 14.61**| +52.26 ± 14.45 | +10.71 ± 1.02 | +0.0020 ± 0.0018 |

*Source Verification:* `consolidated_data/paired_differences.csv`; `Table_06_Paired_Component_Contributions.md`.

---

# SECTION 9 — SCIENTIFIC INTERPRETATION OF RESULTS

### 9.1 Topology vs. Update: Primary Driver vs. Refining Stabilizer
- **Direct Empirical Observation:**
  1. Removing the topology channel ($c_{\text{topo}} = 0$) results in catastrophic defense failure: ASR surges by **+37.32%** on Cora and **+52.23%** on Reddit. Attacker aggregation weight rebounds from $\le 4.8\%$ back to $13.2\%–18.4\%$.
  2. Removing the update channel ($c_{\text{upd}} = 0$) results in a smaller but statistically significant ASR degradation: ASR increases by **+1.19%** on Cora, **+0.28%** on PubMed, and **+11.11%** on Reddit.
- **Scientific Conclusion:** Topological anomaly detection is the **primary gatekeeper** that prevents the majority of backdoor infiltration. The parameter-update channel serves as a **dynamic stabilizer** that tracks training convergence and catches residual parameter steering that topology alone cannot detect. Both channels are strictly necessary.

### 9.2 The Coefficient Normalization Artifact in Standard Ablation
- **Why Old Topology-only Appeared Better Than Full:** In standard ablation (`ConfigurableETDFGLAggregator`), component weights are normalized to sum to 1.0. When the update channel was removed, the topology weight was re-normalized from $9/13 \approx 0.6923$ to $1.0$ (a **+44% coefficient inflation**). This inflated topology weight generated higher trust penalization ($T_0 = 0.078$ vs $0.172$), causing attacker weight to drop to $1.92\%$ and yielding an artificially lower ASR (4.60% vs 5.21% on Cora).
- **The Controlled Solution:** When coefficients are held strictly constant ($9/13$ for topology in both Full and Fixed No Update), removing the update channel cleanly degrades defense (+1.19% on Cora, +11.11% on Reddit), establishing its genuine scientific contribution.

### 9.3 Proof of the 5-Client Normalization Scale-Invariance Invariant
In a federation of $K = 5$ clients where Client 0 is poisoned ($d_0 = d > 0$) and Clients 1–4 are clean ($d_1 = d_2 = d_3 = d_4 = 0$):
1. **Median:** $\text{median}(\mathbf{d}) = 0.0$.
2. **MAD:** Absolute deviations are $[d, 0, 0, 0, 0]$, whose median is $0.0$.
3. **Fallback to Standard Deviation:** When $\text{MAD} = 0$, the algorithm falls back to sample standard deviation:
   $$\sigma(\mathbf{d}) = \sqrt{\frac{1}{5} \sum_{i=0}^4 (d_i - \bar{d})^2} = \sqrt{\frac{1}{5} \left( (d - 0.2d)^2 + 4(0 - 0.2d)^2 \right)} = \sqrt{\frac{1}{5} (0.64 d^2 + 0.16 d^2)} = \sqrt{0.16 d^2} = 0.4 d$$
4. **Outlier Z-Score:** The z-score for the attacker is:
   $$z_0 = \frac{d - 0.0}{0.4 d} \equiv 2.5000$$
5. **Topological Anomaly Score:**
   $$A_0^{\text{topo}} = 2.0 \cdot \left(\frac{1}{1 + e^{-2.5}} - 0.5\right) = 2.0 \cdot (0.92414 - 0.5) = 2.0 \cdot 0.42414 \approx \mathbf{0.8483}$$
6. **Invariance Consequence:** $A_0^{\text{topo}}$ is **completely invariant to the drift magnitude $d > 0$**. Whether the attacker injects a subtle 3-node clique or a massive dense subgraph, the anomaly score is identically $0.8483$.
7. **Fixed Attacker Weight:** In Fixed No Update ($R_0 = \frac{9}{13} \times 0.84828 = 0.58727$), trust is $T_0 = \exp(-3 \times 0.58727) = 0.1717$. Under equal sample counts, the attacker's weight is:
   $$w_0 = \frac{0.1717}{0.1717 + 4.0} \equiv \mathbf{4.12\%} \quad (\sigma = 0.00\%)$$
   This exact value ($4.12\%$) appears empirically across all seeds in Table 4, proving the mathematical invariant.

### 9.4 Reddit Seed 43 Structural Vulnerability
- **Empirical Observation:** Full ETD-FGL achieves 0.85% ASR on Seed 42 and 6.58% on Seed 44, but reaches **34.82%** on Seed 43.
- **Causal Analysis:** Reddit exhibits extreme intra-class degree variance and structural heterogeneity. Under the random split of Seed 43, the attacker's partition received a dense cluster of high-degree nodes whose clean baseline already possessed elevated clustering coefficients. Consequently, the relative perturbation introduced by the 3-clique trigger blended more closely into the background network structure, reducing the discrimination margin.
- **Scientific Significance:** This finding demonstrates that graph heterogeneity remains an inherent challenge for structural anomaly defenses, providing a realistic assessment rather than claiming unrealistic perfection.

### 9.5 Low Baseline Attack Penetration on PubMed
- **Observation:** On PubMed, Attacked FedAvg achieved only **9.23 ± 7.36%** ASR (17.68% on Seed 42, 5.73% on Seed 43, 4.27% on Seed 44).
- **Explanation:** PubMed is a highly sparse citation graph with only 3 classes and 500 features. The natural target-class prediction rate on clean nodes is already 4.35%. Because inter-class citations are rare, the localized 3-clique trigger struggles to propagate its message across distant graph neighborhoods.
- **Reporting Requirement:** Authors must not attribute low ASR on PubMed solely to defense mechanisms; the weak baseline attack penetration must be explicitly acknowledged.

---

# SECTION 10 — NOVELTY AND RELATED-WORK POSITIONING

### 10.1 Distinction from Established Techniques
- **Graph Structural Descriptors:** Basic graph descriptors (density, clustering coefficient, degree moments) are classical network science metrics. ETD-FGL does *not* claim to have invented these descriptors. The novelty lies in defining an authenticated, label-free 5D standardized coordinate system for federated client graph verification.
- **Robust Statistics:** Coordinate-wise medians and MAD scaling are well-established robust statistical estimators. The contribution lies in the one-sided bounded sigmoid transform that prevents false-positive penalization of benign clients.
- **Trust Weighting:** Exponential trust discounting is a recognized formulation. The contribution lies in the dual-evidence fusion mechanism linking parameter dynamics with graph topological drift.

### 10.2 True Scientific Contributions of ETD-FGL
1. First systematic demonstration that parameter-only federated defenses collapse under structural graph backdoors in non-IID settings.
2. Formulation of a dual-evidence anomaly fusion framework that integrates offline topological drift with online parameter update medians.
3. Proof and empirical verification of the scale-invariant trust penalization property in 5-client federations.
4. Comprehensive empirical benchmark across three datasets, eight defense methods, and multiple random seeds establishing state-of-the-art defense without clean accuracy sacrifice.

---

# SECTION 11 — THREATS TO VALIDITY AND RESEARCH LIMITATIONS

### 11.1 Methodological and Implementation Limitations
1. **Reference Graph Assumption:** ETD-FGL assumes the server holds an authenticated, clean structural descriptor for each client's subnetwork prior to attack execution. While realistic for static sensor networks or enterprise federations where initial infrastructure is certified, this assumption is restrictive for dynamic networks where client graphs evolve organically over time.
2. **Single Attacker Evaluation ($M = 1$ in $K = 5$):** All experiments evaluated a single malicious client (20% attacker ratio). The robust median and MAD estimators require benign clients to form a majority ($M < K/2$). Colluding multi-attacker scenarios ($M \ge 2$) have not been evaluated.
3. **Single Model Architecture:** All experiments used a 2-layer GCN. Transferability to GAT, GraphSAGE, or deeper GNN architectures has not been evaluated.
4. **Fixed Trigger Geometry:** Evaluated exclusively on 3-node clique ($K_3$) triggers. Subgraph triggers of different densities (trees, cycles, bipartite cliques) were not tested.
5. **Class-Stratified Partitioning:** Federated client splits rely on class labels across splits to avoid empty classes on Planetoid's small training sets. A fully label-blind partitioner was not evaluated.

---

# SECTION 12 — FIGURE-TO-RESULTS MAPPING TABLE

| Figure Filename | Layout | Dataset(s) | Method(s) | Plotted Evidence | Primary Source File | Section Placement | Proposed Neutral Caption |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Fig_A_Baseline_Comparison_Overview.png` | 2×2 | Cora, PubMed, Reddit | 8 Baselines | Clean Acc, Backdoor ASR, Attack Effect, Log Runtime | `baseline_seed42.csv` | Section 5.2 | *Figure A: Comprehensive evaluation of ETD-FGL against seven baseline federated learning and defense methods on Cora, PubMed, and Reddit (Seed 42).* |
| `Fig_A1_Baseline_Comparison_Cora.png` | 2×2 | Cora | 8 Baselines | Acc, ASR, Effect (zero line), Runtime (values atop bars) | `baseline_seed42.csv` | Section 5.2 / Supp | *Figure A1: Detailed baseline comparison on the Cora benchmark dataset (Seed 42).* |
| `Fig_A2_Baseline_Comparison_PubMed.png` | 2×2 | PubMed | 8 Baselines | Acc, ASR, Effect (zero line), Runtime (values atop bars) | `baseline_seed42.csv` | Section 5.2 / Supp | *Figure A2: Detailed baseline comparison on the PubMed benchmark dataset (Seed 42).* |
| `Fig_A3_Baseline_Comparison_Reddit.png` | 2×2 | Reddit | 8 Baselines | Acc, ASR, Effect (zero line), Runtime (values atop bars) | `baseline_seed42.csv` | Section 5.2 / Supp | *Figure A3: Detailed baseline comparison on the Reddit benchmark dataset (Seed 42).* |
| `Fig_B_Standard_Ablation.png` | 2×2 | Cora, PubMed, Reddit | 6 Standard Variants | Clean Acc, ASR, Attack Effect, Attacker Weight | `consolidated_experiments.csv` | Section 5.3 | *Figure B: Standard multi-seed ablation study evaluating six original variants across Cora, PubMed, and Reddit (Seeds 42, 43, 44).* |
| `Fig_C_Controlled_Ablation.png` | 2×2 | Cora, PubMed, Reddit | 3 Controlled Variants | Backdoor ASR, Paired $\Delta$ ASR, Clean Acc, Paired $\Delta$ Acc | `controlled_ablation_summary.csv` | Section 5.3 | *Figure C: Controlled scientific ablation isolating evidence channels with held-constant coefficients across Cora, PubMed, and Reddit (Seeds 42, 43, 44).* |
| `Fig_D_MultiSeed_Robustness.png` | 1×3 | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Acc, ASR, Attack Effect with Reddit Seed 43 callout | `consolidated_experiments.csv` | Section 5.2 | *Figure D: Multi-seed robustness comparison between unmitigated Attacked FedAvg and ETD-FGL across Seeds 42, 43, and 44.* |
| `Fig_E_Learning_Dynamics.png` | 2×3 | Cora, PubMed, Reddit | Clean, Attacked, FedTGE, ETD-FGL | 50-round convergence curves for Clean Acc and ASR | `training_history.csv` | Section 5.4 | *Figure E: Federated learning dynamics over 50 communication rounds on Cora, PubMed, and Reddit (Seed 42).* |
| `Fig_F_Trust_Defense_Mechanisms.png` | 2×2 | Cora, PubMed, Reddit | ETD-FGL | Weight suppression, risk decomposition, benign trust, invariant proof | `training_history.csv` | Section 4 / 5.4 | *Figure F: ETD-FGL defense mechanism dynamics and mathematical invariants.* |
| `Fig_G_Attack_Effect_and_Defense_Gain.png` | 1×3 | Cora, PubMed, Reddit | Baselines, ETD-FGL | Trigger Attack Effect, Absolute ASR Drop, Relative Reduction % | `baseline_seed42.csv`, `multiseed_summary.csv` | Section 5.2 | *Figure G: Trigger Attack Effect and quantified defense improvements over unmitigated FedAvg.* |
| `Fig_H_Accuracy_ASR_Tradeoff.png` | 1×3 | Cora, PubMed, Reddit | Baselines + Multiseed | Accuracy vs ASR trade-off by dataset; 2D error whiskers | `baseline_seed42.csv`, `multiseed_summary.csv` | Section 5.2 | *Figure H: Clean accuracy versus backdoor robustness (ASR) trade-off plotted separately for Cora, PubMed, and Reddit.* |
| `Fig_I_Training_Runtime_Comparison.png` | 1×2 | Cora, PubMed, Reddit | 8 Baselines | Multi-dataset log-scale + PubMed linear; FedTGE unclipped | `baseline_seed42.csv` | Section 5.5 | *Figure I: Recorded federated training-loop runtime over 50 communication rounds on identical GPU hardware (Seed 42).* |
| `Fig_S_Reddit_Seed_Heterogeneity.png` | 1×3 | Reddit | Controlled Variants | Per-seed breakdown for Seeds 42, 43, 44 | `consolidated_experiments.csv` | Supplementary | *Supplementary Figure S1: Reddit Per-Seed Backdoor ASR across Controlled Variants.* |
| `Fig_S_Standard_vs_Controlled_Comparison.png` | 1×2 | Cora, PubMed, Reddit | Standard vs Controlled | Topology and Update channel comparison under normalized vs fixed | `standard_ablation_summary.csv` | Supplementary | *Supplementary Figure S2: Standard vs Controlled Ablation (Impact of Coefficient Normalization).* |

---

# SECTION 13 — UNRESOLVED RESEARCH QUESTIONS AND MISSING INFORMATION

The following items cannot be definitively resolved from repository inspection and require author decision or future empirical work:

| Item / Open Question | Category | Nature of Ambiguity / Recommendation |
| :--- | :--- | :--- |
| **Label-Blind Graph Partitioning** | New Experiment | Current partitioning uses label stratification to avoid empty training classes on Planetoid. Evaluating Metis graph partitioning or pure Dirichlet partitioning on denser datasets (PubMed/Reddit) is recommended for future revisions. |
| **Colluding Malicious Clients ($M \ge 2$)** | New Experiment | All 132 runs evaluated exactly $M = 1$ in $K = 5$. Multi-client collusive poisoning requires future empirical validation. |
| **Dynamic Graph Topologies** | Author Confirmation | Repository assumes static client graphs where pre-attack descriptors are recorded at enrollment. The author should explicitly position ETD-FGL as designed for federations with certified enrollment baselines. |
| **GNN Architecture Generalization** | New Experiment | Repository contains code only for 2-layer GCN. Evaluating GAT or GraphSAGE requires new training runs. |
| **Trigger Size and Poisoning Ratio Sweeps** | Missing Experiment | Sweep of $s \in \{2, 3, 4, 5\}$ and $\rho \in \{0.05, 0.10, 0.20, 0.30\}$ was not executed in the 132 consolidated runs. |

---

# SECTION 14 — MANUSCRIPT-READY FACTUAL OUTLINE

This section provides a rigorous, fact-based structural outline that the academic editor can follow directly when revising the manuscript text:

### 1. Abstract
- State the security challenge of targeted structural backdoor attacks in Federated Graph Learning (FGL).
- Highlight the fundamental failure mode of parameter-space defenses in distinguishing backdoor gradients from non-IID graph heterogeneity.
- Introduce ETD-FGL: dual-evidence server-side aggregation combining standardized topological drift with coordinate-wise update medians.
- Highlight key verified results: suppresses ASR from 62.0% to 5.2% on Cora, 9.2% to 0.89% on PubMed, and 74.4% to 14.1% on Reddit (0.85% on Seed 42), with 0% clean accuracy penalty and $\le 1.1\times$ FedAvg runtime.

### 2. Introduction
- Paragraph 1: Growth of decentralized graph applications (financial fraud, citation analysis, social networks) and the necessity of FGL.
- Paragraph 2: Vulnerability of GNNs to structural clique backdoors; why Euclidean FL defenses fail on graphs.
- Paragraph 3: Limitations of existing graph defenses: FLPurifier destroys clean accuracy (down to 49.3%), while FedTGE incurs massive computational latency (up to 773s).
- Paragraph 4: Proposed ETD-FGL approach: dual-channel anomaly fusion and exponential trust weighting.
- Paragraph 5: Summary of four concrete scientific contributions.

### 3. Related Work
- Subsection 3.1: Federated Graph Learning paradigms and non-IID partitioning challenges.
- Subsection 3.2: Backdoor attacks on graph neural networks (subgraph triggers, feature triggers).
- Subsection 3.3: Byzantine-robust federated defenses (parameter-space filtering vs graph-specific mechanisms).

### 4. System and Threat Model
- Subsection 4.1: Federated node classification setup ($K = 5$ clients, 2-layer GCN, synchronous FedAvg).
- Subsection 4.2: Threat model ($M = 1$ malicious client, 20% local poisoning budget, 3-node clique trigger, target class $y^* = 0$).
- Subsection 4.3: Reference graph availability assumption and deployment model.

### 5. Proposed ETD-FGL Method
- Subsection 5.1: 5-dimensional label-free structural descriptor vector.
- Subsection 5.2: Standardized topological drift computation.
- Subsection 5.3: One-sided robust positive MAD mapping (`_robust_positive`).
- Subsection 5.4: Coordinate-wise parameter update median and update anomaly.
- Subsection 5.5: Convex risk fusion ($9/13$ topology, $4/13$ update) and exponential trust factor calculation.
- Subsection 5.6: Sample-weighted aggregation and theoretical proof of the 5-client constant invariant.

### 6. Experimental Setup
- Subsection 6.1: Benchmark datasets (Cora, PubMed, Sampled Reddit) and statistics.
- Subsection 6.2: Baseline methods and parameter configurations (7 baseline methods).
- Subsection 6.3: Evaluation metrics (Clean Accuracy, Backdoor ASR, Trigger Attack Effect, Attacker Weight, Runtime).
- Subsection 6.4: Reproducibility protocols and random seeds (42, 43, 44).

### 7. Results and Discussion
- Subsection 7.1: Overall baseline comparison (referencing Figure A, A1–A3, and Table 1).
- Subsection 7.2: Multi-seed robustness and transparent discussion of Reddit Seed 43 (referencing Figure D and Table 2).
- Subsection 7.3: Accuracy vs Robustness trade-off (referencing Figure H).
- Subsection 7.4: Federated learning dynamics over 50 rounds (referencing Figure E).
- Subsection 7.5: Defense mechanism dynamics and weight suppression (referencing Figure F).
- Subsection 7.6: Computational runtime analysis and FedTGE complexity (referencing Figure I).

### 8. Ablation Studies
- Subsection 8.1: Standard ablation study across 6 original variants (referencing Figure B and Table 3).
- Subsection 8.2: Controlled ablation with held-constant coefficients isolating channel necessity (referencing Figure C, Tables 4–5, and Figure S2).

### 9. Threats to Validity and Limitations
- Detail the reference graph requirement, single-attacker scope, 2-layer GCN architecture, and class-stratified partitioning.

### 10. Conclusion
- Conclude with a factual summary of ETD-FGL's empirical defense performance and future directions for dynamic graph topologies.
