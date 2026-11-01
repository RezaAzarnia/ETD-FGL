# ETD-FGL Missing Experimental Evidence and Reproducibility Audit (Revision v4)

**Document Purpose:** Establishes the exact boundaries of verified experimental evidence available in the ETD-FGL repository, distinguishing **genuinely recorded measurements**, **unrecorded evaluation arrays**, and **unmeasured or unrelated metrics**.

---

## 1. Inventory of Genuinely Recorded Experimental Evidence and Checkpoints

Across the ETD-FGL repository, an independent audit of the `outputs/` filesystem verified:
- **Completed Experiment Records (`final_summary.json`):** Exactly **132** distinct runs.
- **Trained Model Checkpoints (`best_model.pt`):** Exactly **132** distinct saved checkpoint files, each located alongside its corresponding `final_summary.json` and `training_history.csv`.

### Breakdown of the 132 Distinct Runs:
1. **Baseline Comparison Suite (Seed 42):** 24 distinct runs (8 methods × 3 datasets)
   - Path pattern: `outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method_slug}/`
   - Checkpoints: 24 distinct `best_model.pt` files.
2. **Multi-Seed Robustness Suite (Seeds 42, 43, 44):** 18 distinct runs (2 methods × 3 datasets × 3 seeds)
   - Path pattern: `outputs/extended_experiments/multiseed/{dataset}/seed_{42,43,44}/{method_slug}/`
   - Checkpoints: 18 distinct `best_model.pt` files.
3. **Standard Ablation Suite (Seeds 42, 43, 44):** 54 distinct runs (6 variants × 3 datasets × 3 seeds)
   - Path pattern: `outputs/extended_experiments/ablation/{dataset}/seed_{42,43,44}/{variant_slug}/`
   - Checkpoints: 54 distinct `best_model.pt` files.
4. **Controlled Ablation Suite (Seeds 42, 43, 44):** 36 distinct runs (3 variants × 3 datasets × 3 seeds)
   - Path pattern: `outputs/extended_experiments/controlled_ablation_v1/{dataset}/seed_{42,43,44}/{variant_slug}/`
   - Checkpoints: 36 distinct `best_model.pt` files.

**Total:** $24 + 18 + 54 + 36 = 132$ distinct experiment runs, each with a complete `final_summary.json`, `training_history.csv`, and `best_model.pt`.

---

## 2. Genuinely Recorded Metrics in Scalar Output Summaries

The **only** metrics serialized in `final_summary.json` and `training_history.csv` are:

| Metric Name | Storage Key | Measurement Unit / Definition | Verification Status |
| :--- | :--- | :--- | :--- |
| **Clean Test Accuracy** | `clean_test_accuracy` | Percentage (0–100%) on unpoisoned global test set | **Verified** |
| **Clean Target Rate** | `clean_target_rate` | Percentage (0–100%) of clean test nodes predicted as target class | **Verified** |
| **Backdoor ASR** | `attack_success_rate` | Percentage (0–100%) of triggered test nodes predicted as target class | **Verified** |
| **Trigger Attack Effect** | `attack_effect` | Percentage points (`pp`): $ASR - \text{Clean Target Rate}$ | **Verified** |
| **Training-Loop Runtime** | `elapsed_seconds` | Wall-clock seconds for 50 federated rounds on GPU | **Verified** |
| **Best Communication Round** | `best_round` | Integer (1–50) identifying the checkpoint with highest validation accuracy | **Verified** |
| **Attacker Aggregation Weight** | `etdfgl_weight_client_0` | Decimal fraction / percentage allocated to malicious Client 0 | **Verified** |
| **Benign Client Weights** | `etdfgl_weight_client_{1..4}` | Decimal fractions / percentages allocated to benign Clients 1 through 4 | **Verified** |
| **Topology Anomaly** | `etdfgl_topology_risk_client_k` | Bounded anomaly score $A_k^{\text{topo}} \in [0, 1]$ | **Verified** |
| **Update Anomaly** | `etdfgl_update_risk_client_k` | Bounded anomaly score $A_k^{\text{upd}} \in [0, 1]$ | **Verified** |
| **Fused Client Risk** | `etdfgl_fused_risk_client_k` | Convex combination $R_k = \frac{9}{13} A_k^{\text{topo}} + \frac{4}{13} A_k^{\text{upd}}$ | **Verified** |
| **Client Trust Factor** | `etdfgl_trust_client_k` | Exponential trust factor $T_k = \text{clip}(\exp(-3 R_k), 0.02, 1.0)$ | **Verified** |

---

## 3. Unrecorded Classification Metrics and Feasibility Clarification

| Metric | Status in ETD-FGL | Current Summary Derivability | Clarification on Computational Feasibility | Scientific Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Macro/Micro F1-Score** | **Not Recorded in Summaries** | **Cannot be derived from scalar summaries.** Node-level prediction arrays ($\hat{\mathbf{y}}$) and ground-truth label tensors ($\mathbf{y}$) were not serialized to the summary JSON files. | **Does NOT require retraining.** Because exactly 132 `best_model.pt` checkpoints and raw test datasets are preserved on disk, F1 scores could be computed via a fast, inference-only forward pass if separately approved. Under current frozen evidence, F1 is not available. | Confine current manuscript reporting strictly to verified Clean Accuracy. Do NOT invent F1 numbers. |
| **Precision and Recall** | **Not Recorded in Summaries** | **Cannot be derived from scalar summaries.** Class-specific confusion matrices were not serialized. | Inference-feasible via saved checkpoints, but currently uncomputed. | Do NOT report Precision or Recall without approved inference pass. |
| **ROC-AUC & PR-AUC** | **Not Recorded in Summaries** | **Cannot be derived from scalar summaries.** Softmax probability distributions were not saved. | Inference-feasible via saved checkpoints, but currently uncomputed. | Do NOT invent ROC-AUC or PR curves. |
| **False Positive Rate (FPR)** | **Not Recorded** | **No.** Benign client exclusion was not framed as a binary decision, since ETD-FGL applies continuous soft trust weighting ($T_i \in [0.02, 1.0]$) rather than hard client pruning. | N/A (Algorithmic formulation uses soft weighting). | Report benign trust preservation ($T_{1..4} > 0.85$) and benign fused risk ($R_{1..4} < 0.06$) instead of hard FPR. |
| **Packet Delivery Ratio (PDR)** | **Unrelated** | **N/A.** PDR is an IoT routing/physical-layer metric from an unrelated reference manuscript, completely irrelevant to federated graph learning. | Irrelevant. | Exclude completely from the manuscript. |
| **Routing / Network Latency** | **Unrelated** | **N/A.** Network transmission delays across physical IoT routers were not simulated. | Irrelevant. | Runtime must be reported strictly as recorded training-loop runtime. |
| **Differential Privacy ($\epsilon, \delta$)**| **Unmeasured** | **N/A.** ETD-FGL does not inject Gaussian or Laplacian DP noise into parameters. | Irrelevant. | Exclude completely. |
| **Fault Recovery Time** | **Unmeasured** | **N/A.** Client dropout recovery dynamics were not simulated. | Irrelevant. | Exclude completely. |

---

## 4. Missing Experimental Sweeps and Sensitivity Analyses (Audited Boundaries)

The following experimental sweeps exist in the broader federated learning literature but were **never executed** in the 132 consolidated runs:

### 4.1 Sensitivity to Number of Malicious Clients ($M \in \{1, 2, 3\}$)
- **Status:** **NOT PERFORMED.**
- **Details:** All 132 completed runs strictly evaluated a federation of $K = 5$ clients with exactly $M = 1$ malicious client (Client 0, representing a 20% malicious client ratio).
- **Caveat:** The robust median-based aggregation and positive MAD outlier mapping assume benign clients constitute a majority ($M < K/2$). Evaluating $M \ge 2$ in a 5-client federation has not been experimentally tested.
- **Reporting Boundary:** State explicitly in Section 11 (Limitations) that empirical validation is currently restricted to a single attacker in a 5-client federation.

### 4.2 Sensitivity to Trigger Size ($s \in \{2, 4, 5, 8\}$ nodes)
- **Status:** **NOT PERFORMED.**
- **Details:** All 132 completed experiments utilized a fixed 3-node clique trigger ($s = 3$ interconnected nodes, $K_3$) across Cora, PubMed, and Reddit (`multidata_suite/config.py:21`).
- **Caveat:** Sweeps across varying trigger subnetwork sizes (e.g., $s = 2, 4, 5, 8$) or non-clique topological motifs (trees, cycles, bipartite cliques) were not conducted.
- **Reporting Boundary:** Document as an open question for future empirical benchmarks; do not fabricate sensitivity curves.

### 4.3 Sensitivity to Poisoning Ratio / Budget ($\rho \in \{5\%, 10\%, 30\%\}$)
- **Status:** **NOT PERFORMED.**
- **Details:** The local poisoning budget was held constant at strictly 20% ($\rho = 0.20$) of candidate non-target training nodes in Client 0's partition across all evaluated suites (`multidata_suite/config.py:20`).
- **Caveat:** Sub-threshold backdoor injection (e.g., poisoning only 5% of candidate nodes) or saturation injection (30%) was not evaluated.
- **Reporting Boundary:** Acknowledge this fixed 20% budget boundary in the threat model and experimental setup without claiming sensitivity sweeps.

### 4.4 Non-IID Dirichlet Parameter Sweep ($\alpha \in \{0.1, 0.5, 1.0, 5.0\}$)
- **Status:** **NOT PERFORMED.**
- **Details:** Client partitioning was executed via a label-aware class-stratified partitioning scheme with fixed random assignment seeds. A continuous Dirichlet concentration parameter sweep was not performed.
- **Reporting Boundary:** Accurately describe the actual graph partitioning method without claiming an $\alpha$-sweep.

### 4.5 Architectural Sweeps (GAT, GraphSAGE, GIN)
- **Status:** **NOT PERFORMED.**
- **Details:** All experimental runs across all 8 methods, all 3 datasets, and all seeds strictly used a 2-layer Graph Convolutional Network (GCN) with 32 hidden units.
- **Reporting Boundary:** State clearly that empirical validation is established on 2-layer GCN architectures.

---

## 5. Specific Experimental Observations Requiring Objective Reporting

### 5.1 Reddit Seed 43 Elevated Backdoor Retention
- **Empirical Measurement:** Under Full ETD-FGL on Reddit Seed 43, Backdoor ASR reaches **34.82%** (Trigger Attack Effect = 34.39 pp), whereas on Seed 42 ASR is 0.85% and on Seed 44 ASR is 6.58%.
- **Evidentiary Basis:** Genuinely recorded in `outputs/extended_experiments/multiseed/reddit/seed_43/defended_etdfgl/final_summary.json`.
- **Classification:** Elevated ASR is a **Verified** observation. The explanation attributing it to high intra-class degree variance reducing trigger contrast is an unverified **Hypothesis**.
- **Action:** Retain prominent reporting of Seed 43 in all figures and tables without smoothing or suppression.

### 5.2 DMGNN-FL Equivalence to Attacked FedAvg on Reddit
- **Empirical Measurement:** In `outputs/final_multidataset/federated_reddit/baseline_dmgnn/`, recorded Clean Accuracy (85.70%), ASR (72.29%), and training history SHA-256 hash match `outputs/final_multidataset/federated_reddit/fedavg_structural_backdoor/`.
- **Classification:** Output numerical equivalence is a **Verified** observation. The claim that explanation saliency thresholds specifically pruned 0 edges is an unverified **Hypothesis** because raw edge pruning counts were not logged.
- **Action:** Report the numerical equivalence factually and classify the pruning count mechanism as an unverified hypothesis.

### 5.3 Low Baseline Attack Penetration on PubMed
- **Empirical Measurement:** Under unmitigated Attacked FedAvg, Backdoor ASR on PubMed across three seeds is only **9.23 ± 7.36%** (17.68% on Seed 42, 5.73% on Seed 43, 4.27% on Seed 44).
- **Classification:** Low baseline ASR is a **Verified** observation. The citation sparsity explanation is an unverified **Hypothesis**.
- **Action:** Acknowledge that the low ASR achieved by ETD-FGL on PubMed (0.89%) occurs in a setting where the unmitigated attack itself achieves low penetration.
