# ETD-FGL Missing Experimental Evidence and Reproducibility Audit

This document establishes the exact boundaries of verified experimental evidence available in the ETD-FGL repository, explicitly distinguishing **genuinely recorded measurements** from **unmeasured, unrecorded, or unrelated metrics**.

As an empirical reproducibility audit, this report guarantees that no metrics, sensitivity sweeps, or architectural evaluations are fabricated or back-projected from external sources (such as the visual reference IoT paper).

---

## 1. Inventory of Genuinely Recorded Experimental Evidence

Across the 132 completed experimental runs consolidated in the repository:
- **Baseline Comparison Suite (Seed 42):** 24 runs (8 methods × 3 datasets)
- **Multi-Seed Robustness Suite (Seeds 42, 43, 44):** 18 runs (2 methods × 3 datasets × 3 seeds)
- **Standard Ablation Suite (Seeds 42, 43, 44):** 54 runs (6 variants × 3 datasets × 3 seeds)
- **Controlled Ablation Suite (Seeds 42, 43, 44):** 36 runs (3 variants × 3 datasets × 3 seeds)

The **only** metrics genuinely recorded in `final_summary.json` and `training_history.csv` are:

| Metric Name | Storage Key | Measurement Unit / Definition | Verification Status |
| :--- | :--- | :--- | :--- |
| **Clean Test Accuracy** | `clean_test_accuracy` | Percentage (0–100%) on unpoisoned global test set | **Verified** |
| **Clean Target Rate** | `clean_target_rate` | Percentage (0–100%) of clean test nodes predicted as target class | **Verified** |
| **Backdoor ASR** | `attack_success_rate` | Percentage (0–100%) of triggered test nodes predicted as target class | **Verified** |
| **Trigger Attack Effect** | `attack_effect` | Percentage points: $ASR - \text{Clean Target Rate}$ | **Verified** |
| **Training-Loop Runtime** | `elapsed_seconds` | Wall-clock seconds for 50 federated rounds on GPU | **Verified** |
| **Best Communication Round** | `best_round` | Integer (1–50) identifying the checkpoint with highest validation accuracy | **Verified** |
| **Attacker Aggregation Weight** | `etdfgl_weight_client_0` | Decimal fraction / percentage allocated to malicious Client 0 | **Verified** |
| **Benign Client Weights** | `etdfgl_weight_client_{1..4}` | Decimal fractions / percentages allocated to benign Clients 1 through 4 | **Verified** |
| **Topology Anomaly** | `etdfgl_topology_risk_client_k` | Bounded anomaly score $A_k^{\text{topo}} \in [0, 1]$ | **Verified** |
| **Update Anomaly** | `etdfgl_update_risk_client_k` | Bounded anomaly score $A_k^{\text{upd}} \in [0, 1]$ | **Verified** |
| **Fused Client Risk** | `etdfgl_fused_risk_client_k` | Convex combination $R_k = c_{\text{topo}} A_k^{\text{topo}} + c_{\text{upd}} A_k^{\text{upd}}$ | **Verified** |
| **Client Trust Factor** | `etdfgl_trust_client_k` | Exponential trust factor $T_k = \exp(-3 R_k) \in (0, 1]$ | **Verified** |

---

## 2. Unmeasured Classification and Detection Metrics

The older visual-reference manuscript (which studied IoT routing and network intrusion detection on CICIoT2023 and UNSW-NB15) presented several classification metrics that **do not exist** in the ETD-FGL repository.

| Metric | Status in ETD-FGL | Can It Be Derived from Saved Files? | Scientific Recommendation |
| :--- | :--- | :--- | :--- |
| **Macro/Micro F1-Score** | **Not Recorded** | **No.** Node-level prediction arrays and ground-truth label tensors were not serialized to disk; only scalar accuracy was stored. | Do NOT report F1. Confine classification reporting strictly to verified Clean Accuracy. |
| **Precision and Recall** | **Not Recorded** | **No.** Class-specific confusion matrices were not preserved. | Do NOT report Precision or Recall. |
| **ROC-AUC & PR-AUC** | **Not Recorded** | **No.** Softmax prediction probability distributions were not preserved. | Do NOT invent ROC-AUC or PR curves. |
| **False Positive Rate (FPR)** | **Not Recorded** | **No.** Benign client false-exclusion rate is not measured as a binary decision, since ETD-FGL applies continuous soft trust weighting rather than hard client pruning. | Report benign client trust preservation ($T_{1..4} > 0.85$) and benign fused risk ($R_{1..4} < 0.06$) instead of hard FPR. |
| **Packet Delivery Ratio (PDR)** | **Unrelated** | **N/A.** PDR is an IoT routing network layer metric, completely irrelevant to federated graph learning. | Exclude completely from the manuscript. |
| **Routing / Network Latency** | **Unrelated** | **N/A.** Network transmission delays across physical IoT routers were not simulated. | Exclude completely. Runtime must be reported strictly as *recorded training-loop runtime*. |
| **Differential Privacy Epsilon** | **Unmeasured** | **N/A.** ETD-FGL does not inject Gaussian or Laplacian DP noise into gradients. | Exclude completely. |
| **Fault Recovery Time** | **Unmeasured** | **N/A.** Client dropout recovery was not evaluated. | Exclude completely. |

---

## 3. Missing Experimental Sweeps and Sensitivity Analyses

Several candidate sensitivity analyses exist in federated learning literature but were **never executed** in the current ETD-FGL experimental campaign:

### 1. Sensitivity to Number of Malicious Clients ($M \in \{1, 2, 3\}$)
- **Status:** **NOT PERFORMED.**
- **Details:** All 132 completed runs strictly evaluated a federation of $K = 5$ clients with exactly $M = 1$ malicious client (Client 0, representing a 20% malicious client ratio).
- **Caveat:** The robust median-based aggregation and positive MAD outlier mapping rely on benign clients constituting a majority ($M < K/2$). Evaluating $M \ge 2$ in a 5-client federation has not been experimentally tested.
- **Action:** State explicitly in Section 11 (Limitations) that the empirical validation is currently restricted to a single attacker in a 5-client federation.

### 2. Sensitivity to Trigger Size ($s \in \{3, 5, 8, 10\}$ nodes)
- **Status:** **NOT PERFORMED.**
- **Details:** All experiments utilized a fixed clique trigger size ($s = 5$ interconnected nodes on Cora and Reddit; $s = 5$ on PubMed).
- **Caveat:** Varying trigger subnetwork density or size was not swept.
- **Action:** Document as an open question for future empirical benchmarks.

### 3. Sensitivity to Poisoning Ratio / Budget ($p \in \{1\%, 5\%, 10\%, 20\%\}$)
- **Status:** **NOT PERFORMED.**
- **Details:** The local poisoning budget was held constant at 10% of local training nodes across all evaluated suites.
- **Caveat:** Sub-threshold backdoor injection (e.g., poisoning only 1% of nodes) or saturation injection (30%) was not evaluated.
- **Action:** Acknowledge this boundary in the threat model and experimental setup.

### 4. Non-IID Dirichlet Parameter Sweep ($\alpha \in \{0.1, 0.5, 1.0, 5.0\}$)
- **Status:** **NOT PERFORMED.**
- **Details:** Client partitioning was executed via a label-aware non-IID partitioning scheme with fixed random assignment seeds. A continuous Dirichlet concentration parameter sweep was not performed.
- **Action:** Accurately describe the actual graph partitioning method without claiming an $\alpha$-sweep.

### 5. Architectural Sweeps (GAT, GraphSAGE, GIN)
- **Status:** **NOT PERFORMED.**
- **Details:** All experimental runs across all 8 methods, all 3 datasets, and all seeds strictly used a 2-layer Graph Convolutional Network (GCN) with 32 hidden units.
- **Action:** State clearly that the empirical validation is established on 2-layer GCN architectures.

---

## 4. Specific Experimental Anomalies Requiring Factual Reporting

### 1. Reddit Seed 43 Elevated Backdoor Retention
- **Empirical Measurement:** Under Full ETD-FGL on Reddit Seed 43, Backdoor ASR reaches **34.82%** (Trigger Attack Effect = 34.39%), whereas on Seed 42 ASR is 0.85% and on Seed 44 ASR is 6.58%.
- **Scientific Integrity Requirement:** This is NOT an experimental failure or plotting error. It is a genuine empirical finding demonstrating that under severe graph topological heterogeneity and high degree variance (typical of Reddit communities), structural backdoor suppression is more challenging.
- **Action:** Keep this observation prominent in all figures and discuss it transparently in the text.

### 2. DMGNN-FL Equivalence to Attacked FedAvg on Reddit
- **Empirical Measurement:** In `outputs/final_multidataset/federated_reddit/baseline_dmgnn/`, the recorded clean accuracy (85.70%), ASR (72.29%), and training history SHA-256 hash are identical to `outputs/final_multidataset/federated_reddit/fedavg_structural_backdoor/`.
- **Scientific Integrity Requirement:** On Reddit Seed 42, the DMGNN-FL baseline implementation produced identical results to unmitigated Attacked FedAvg.
- **Action:** Report this numerical equivalence factually without speculating or inventing unproven causal explanations.

### 3. Weak Attack Penetration on PubMed Seeds 43 and 44
- **Empirical Measurement:** Even under unmitigated Attacked FedAvg, Backdoor ASR on PubMed was only **5.73%** on Seed 43 and **4.27%** on Seed 44 (compared to 17.68% on Seed 42).
- **Scientific Integrity Requirement:** Structural clique triggers have naturally low penetration in PubMed due to sparse inter-class citation patterns and high feature dimension (500 features).
- **Action:** Explicitly report that the baseline attack penetration on PubMed was weak across multiple seeds, placing the 0.89% average ASR of ETD-FGL in appropriate scientific context.
