# ETD-FGL Scientific Figure Index (Revision v2)

This index documents the complete suite of 14 redesigned, publication-grade scientific figures produced for the ETD-FGL manuscript revision. All figures are generated at **600 DPI PNG** format, adhering strictly to IEEE/ACM/Elsevier academic typography, high contrast, clean white backgrounds, and colorblind-safe palettes.

---

## Summary of Figure Deliverables

| Figure Identifier | Filename | Layout | Focus / Purpose | Suggested Manuscript Section |
| :--- | :--- | :--- | :--- | :--- |
| **Figure A (Overview)** | `Fig_A_Baseline_Comparison_Overview.png` | 2×2 Multi-panel | 8-method baseline comparison across Cora, PubMed, Reddit (Acc, ASR, Attack Effect, Runtime) | Section 5.2 (Main Results) |
| **Figure A1 (Cora)** | `Fig_A1_Baseline_Comparison_Cora.png` | 2×2 Multi-panel | In-depth 8-method baseline evaluation on Cora dataset | Section 5.2 / Supplementary |
| **Figure A2 (PubMed)** | `Fig_A2_Baseline_Comparison_PubMed.png` | 2×2 Multi-panel | In-depth 8-method baseline evaluation on PubMed dataset | Section 5.2 / Supplementary |
| **Figure A3 (Reddit)** | `Fig_A3_Baseline_Comparison_Reddit.png` | 2×2 Multi-panel | In-depth 8-method baseline evaluation on Reddit dataset | Section 5.2 / Supplementary |
| **Figure B** | `Fig_B_Standard_Ablation.png` | 2×2 Multi-panel | Standard multi-seed ablation of 6 original variants across Cora, PubMed, Reddit | Section 5.3 (Ablation Studies) |
| **Figure C** | `Fig_C_Controlled_Ablation.png` | 2×2 Multi-panel | Controlled scientific ablation isolating channels with held-constant coefficients | Section 5.3 (Controlled Ablation) |
| **Figure D** | `Fig_D_MultiSeed_Robustness.png` | 1×3 Multi-panel | Multi-seed robustness (Seeds 42, 43, 44) with prominent Reddit Seed 43 callout | Section 5.2 (Multi-Seed Robustness) |
| **Figure E** | `Fig_E_Learning_Dynamics.png` | 2×3 Multi-panel | 50-round convergence trajectories for Clean Accuracy and Backdoor ASR | Section 5.4 (Convergence Dynamics) |
| **Figure F** | `Fig_F_Trust_Defense_Mechanisms.png` | 2×2 Multi-panel | Dynamic client risk breakdown, trust factor, attacker weight, and 5-client invariance | Section 4 / Section 5.4 (Defense Analysis) |
| **Figure G** | `Fig_G_Attack_Effect_and_Defense_Gain.png` | 1×3 Multi-panel | Trigger Attack Effect (zero line), absolute ASR drop, and relative percentage reduction | Section 5.2 (Defense Effectiveness) |
| **Figure H** | `Fig_H_Accuracy_ASR_Tradeoff.png` | 1×3 Multi-panel | Accuracy vs Backdoor Robustness Pareto trade-off by dataset (no overlapping annotations) | Section 5.2 (Trade-off Analysis) |
| **Figure I** | `Fig_I_Training_Runtime_Comparison.png` | 1×2 Multi-panel | Training-loop runtime comparison fixing FedTGE clipping (log-scale + linear PubMed) | Section 5.5 (Computational Overhead) |
| **Figure S1** | `Fig_S_Reddit_Seed_Heterogeneity.png` | 1×3 Multi-panel | Per-seed breakdown on Reddit highlighting structural vulnerability on Seed 43 | Supplementary Material |
| **Figure S2** | `Fig_S_Standard_vs_Controlled_Comparison.png` | 1×2 Multi-panel | Empirical proof of why topology coefficient inflation ($9/13 \to 1.0$) masked update channel | Supplementary Material |

---

## Detailed Descriptions and Neutral Academic Captions

### Figure A: Comprehensive Baseline Comparison Overview
- **Filename:** `Fig_A_Baseline_Comparison_Overview.png`
- **Layout:** 2×2 panels: (a) Clean Test Accuracy (%), (b) Backdoor Attack Success Rate (ASR %), (c) Trigger Attack Effect (% points), (d) Training Loop Runtime (seconds, log scale).
- **Methods:** Clean FedAvg, Attacked FedAvg, PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE, ETD-FGL.
- **Datasets:** Cora, PubMed, Reddit.
- **Evaluation Scope:** Single-seed (Seed 42), explicitly noted without fictitious error bars.
- **Proposed Caption:**
  > *Figure A: Comprehensive evaluation of ETD-FGL against seven baseline federated learning and defense methods on Cora, PubMed, and Reddit (evaluated on Seed 42). (a) Clean test classification accuracy shows that ETD-FGL preserves the baseline performance of unattacked FedAvg. (b) Backdoor Attack Success Rate (ASR) demonstrates that ETD-FGL restricts backdoor penetration to below 5% on Cora, 1% on PubMed, and 1% on Reddit (Seed 42). (c) Trigger Attack Effect ($ASR - \text{Clean Target Rate}$) confirms complete neutralization of the backdoor trigger, dropping below zero for ETD-FGL. (d) Recorded training-loop execution runtime across 50 communication rounds plotted on a logarithmic scale; FedTGE exhibits 25×–117× greater runtime overhead due to dense structural graph entropy calculations.*

---

### Figures A1, A2, A3: Dataset-Specific Baseline Comparisons
- **Filenames:** `Fig_A1_Baseline_Comparison_Cora.png`, `Fig_A2_Baseline_Comparison_PubMed.png`, `Fig_A3_Baseline_Comparison_Reddit.png`
- **Layout:** 2×2 panels per dataset: (a) Clean Test Accuracy, (b) Backdoor ASR, (c) Trigger Attack Effect with zero line, (d) Training Runtime with exact second annotations.
- **Design Inspiration:** Follows the clean, multi-panel academic format of the visual reference figures (`fig3.png`, `fig5.png`), providing uncrowded bar plots with numeric values atop every bar.
- **Proposed Caption (Template for A1/A2/A3):**
  > *Figure A[1/2/3]: Detailed baseline comparison on the [Cora / PubMed / Reddit] benchmark dataset (Seed 42). Panels illustrate: (a) Clean test accuracy, (b) Backdoor Attack Success Rate (ASR), (c) Trigger Attack Effect with a prominent zero reference line, and (d) Recorded training-loop runtime over 50 rounds. Numeric values above bars indicate exact empirical measurements.*

---

### Figure B: Standard Multi-Seed Ablation Study
- **Filename:** `Fig_B_Standard_Ablation.png`
- **Layout:** 2×2 panels: (a) Clean Test Accuracy, (b) Backdoor ASR, (c) Trigger Attack Effect, (d) Attacker Aggregation Weight Share (%).
- **Variants (6):**
  1. Full ETD-FGL (`ETD-FGL (Full final)`)
  2. Topology-only (`ETD-FGL Topology-only`, normalized $c_{\text{topo}}=1.0$)
  3. Update-only (`ETD-FGL Update-only`, normalized $c_{\text{upd}}=1.0$)
  4. No Trust Weighting (`ETD-FGL w/o Trust Weighting`, uniform 20% weight)
  5. Historical Three-Channel (`Historical Three-Channel Variant (0.45/0.35/0.20)`)
  6. Attacked FedAvg (`Attacked FedAvg`, unmitigated baseline)
- **Seeds:** 42, 43, 44 (Mean ± sample standard deviation with overlaid jittered seed markers).
- **Proposed Caption:**
  > *Figure B: Standard multi-seed ablation study evaluating six original variants across Cora, PubMed, and Reddit (Seeds 42, 43, 44). Bars indicate sample means; error bars denote sample standard deviation ($ddof=1$); overlaid points show individual seed outcomes. (a) Clean accuracy remains stable across all variants. (b) Backdoor ASR reveals that removing trust weighting or relying strictly on update anomaly allows substantial backdoor injection. (c) Trigger Attack Effect displays complete trigger suppression for Full ETD-FGL and Topology-only. (d) Attacker aggregation weight share demonstrates that trust weighting effectively suppresses malicious client contribution from the 20% uniform baseline down to $\le 4.8\%$.*

---

### Figure C: Controlled Scientific Ablation
- **Filename:** `Fig_C_Controlled_Ablation.png`
- **Layout:** 2×2 panels: (a) Backdoor ASR under held-constant coefficients, (b) Paired ASR degradation ($\Delta \text{ASR} = \text{Variant} - \text{Full}$), (c) Clean Accuracy, (d) Paired Clean Accuracy difference ($\Delta \text{Acc} = \text{Variant} - \text{Full}$).
- **Variants (3):**
  1. Full ETD-FGL ($c_{\text{topo}}=9/13, c_{\text{upd}}=4/13$)
  2. Fixed No Update ($c_{\text{topo}}=9/13, c_{\text{upd}}=0$)
  3. Fixed No Topology ($c_{\text{topo}}=0, c_{\text{upd}}=4/13$)
- **Seeds:** 42, 43, 44.
- **Proposed Caption:**
  > *Figure C: Controlled scientific ablation isolating evidence channels with held-constant coefficients across Cora, PubMed, and Reddit (Seeds 42, 43, 44). (a) Backdoor ASR across the three controlled variants. (b) Paired ASR degradation ($\Delta = \text{Variant} - \text{Full ETD-FGL}$) computed seed-by-seed. Holding coefficients strictly constant reveals that removing the model-update channel causes a statistically significant increase in backdoor ASR (+1.19% on Cora, +0.28% on PubMed, and +11.11% on Reddit), while removing the topology channel leads to severe defense failure (+37.3% on Cora, +1.9% on PubMed, +52.2% on Reddit). (c)–(d) Clean accuracy and paired clean accuracy differences confirm that robustness gains are achieved without sacrificing classification accuracy.*

---

### Figure D: Multi-Seed Robustness Evaluation
- **Filename:** `Fig_D_MultiSeed_Robustness.png`
- **Layout:** 1×3 panels: (a) Clean Test Accuracy, (b) Backdoor ASR, (c) Trigger Attack Effect.
- **Methods:** Attacked FedAvg vs Full ETD-FGL across Seeds 42, 43, 44.
- **Special Feature:** Prominent callout annotation on Reddit Seed 43 ($ASR = 34.82\%$, $\text{Attack Effect} = 34.39\%$), ensuring full visual transparency of this challenging partition.
- **Proposed Caption:**
  > *Figure D: Multi-seed robustness comparison between unmitigated Attacked FedAvg and ETD-FGL across Seeds 42, 43, and 44. Bars represent sample means; error bars denote sample standard deviations; white circles display individual random seeds. On Reddit, Seed 43 is explicitly highlighted with a red triangular marker and annotation ($ASR = 34.8\%$), reflecting elevated backdoor vulnerability in highly heterogeneous graph partitions, while still achieving a 40.9% absolute reduction compared to Attacked FedAvg (75.7%).*

---

### Figure E: Federated Learning Dynamics
- **Filename:** `Fig_E_Learning_Dynamics.png`
- **Layout:** 2×3 panels (Rows: Clean Accuracy, Backdoor ASR; Columns: Cora, PubMed, Reddit) across 50 communication rounds.
- **Methods:** Clean FedAvg, Attacked FedAvg, FedTGE, ETD-FGL.
- **Proposed Caption:**
  > *Figure E: Federated learning dynamics over 50 communication rounds on Cora, PubMed, and Reddit (Seed 42). Top row: Clean test accuracy convergence. Bottom row: Backdoor Attack Success Rate (ASR). While unmitigated Attacked FedAvg rapidly assimilates the backdoor trigger within the first 10 rounds, ETD-FGL suppresses backdoor injection from round 1 while maintaining convergence speed and final accuracy identical to Clean FedAvg.*

---

### Figure F: Trust and Defense Mechanism Dynamics
- **Filename:** `Fig_F_Trust_Defense_Mechanisms.png`
- **Layout:** 2×2 panels:
  - (a) Dynamic Attacker Aggregation Weight ($w_0$) over 50 rounds across Cora, PubMed, Reddit.
  - (b) Risk decomposition for the malicious client on Cora ($A_0^{\text{topo}}$, $A_0^{\text{upd}}$, $R_0$).
  - (c) Trust factor trajectory comparing benign clients ($T_{1..4}$) against the attacker ($T_0$).
  - (d) Theoretical and empirical proof of the 5-client normalization scale-invariance ($z_0 \equiv 2.5$, $A_0^{\text{topo}} \equiv 0.8483$, $w_0 \equiv 4.12\%$).
- **Proposed Caption:**
  > *Figure F: ETD-FGL defense mechanism dynamics and mathematical invariants. (a) Dynamic suppression of malicious client aggregation weight ($w_0$) below 5% across all communication rounds. (b) Attacker risk decomposition on Cora showing persistent elevation of topological anomaly and model-update anomaly. (c) Benign client trust factor preservation ($T_{1..4} > 0.85$) contrasted with severe attacker trust penalization ($T_0 < 0.20$). (d) Scale-invariance property in a 5-client federation where four clients have zero topological drift: regardless of the raw drift magnitude $d > 0$, the robust outlier z-score is identically $z_0 = d / (0.4d) \equiv 2.5$, yielding a constant topological anomaly score $A_0^{\text{topo}} \approx 0.8483$ and a fixed attacker weight of 4.12% under Fixed No Update.*

---

### Figure G: Trigger Attack Effect and Relative Defense Gains
- **Filename:** `Fig_G_Attack_Effect_and_Defense_Gain.png`
- **Layout:** 1×3 panels:
  - (a) Trigger Attack Effect across all 7 attacked methods (Seed 42) with a prominent zero reference line.
  - (b) Absolute ASR reduction ($\text{ASR}_{\text{FedAvg}} - \text{ASR}_{\text{ETDFGL}}$ in percentage points across seeds 42, 43, 44).
  - (c) Relative backdoor reduction rate ($(1 - \text{ASR}_{\text{ETDFGL}} / \text{ASR}_{\text{FedAvg}}) \times 100\%$).
- **Proposed Caption:**
  > *Figure G: Trigger Attack Effect and quantified defense improvements over unmitigated FedAvg. (a) Trigger Attack Effect ($ASR - \text{Clean Target Rate}$) on Seed 42; negative values for ETD-FGL demonstrate that the model classifies triggered test graphs into the target class no more frequently than clean graphs. (b) Absolute ASR reduction across three seeds: 56.8% on Cora, 8.3% on PubMed, and 60.3% on Reddit. (c) Relative backdoor suppression rate: ETD-FGL eliminates 91.6% of backdoor penetration on Cora, 90.3% on PubMed, and 81.1% on Reddit.*

---

### Figure H: Accuracy versus Robustness Trade-off
- **Filename:** `Fig_H_Accuracy_ASR_Tradeoff.png`
- **Layout:** 1×3 panels (separated by dataset: Cora, PubMed, Reddit) to eliminate visual clutter.
- **Features:** Single-seed baselines shown as individual scatter markers; multi-seed Attacked FedAvg and ETD-FGL shown with 2D error whiskers (Mean ± SD in both Clean Accuracy and ASR); green directional arrow pointing to the desirable region (High Accuracy, Low ASR).
- **Proposed Caption:**
  > *Figure H: Clean accuracy versus backdoor robustness (ASR) trade-off plotted separately for Cora, PubMed, and Reddit. Individual markers represent single-seed baseline methods (Seed 42); prominent markers with cross-whiskers represent multi-seed distributions (mean ± sample standard deviation across seeds 42, 43, 44). ETD-FGL decisively shifts the federated model into the optimal defense regime (bottom-right: high clean accuracy, near-zero ASR).*

---

### Figure I: Federated Training Loop Runtime Comparison
- **Filename:** `Fig_I_Training_Runtime_Comparison.png`
- **Layout:** 1×2 panels:
  - (a) Multi-dataset runtime comparison across all 8 methods plotted on a logarithmic scale ($10^0$ to $10^3$ seconds), with explicit callouts for FedTGE.
  - (b) Linear-scale runtime breakdown on PubMed showing all methods unclipped up to 900 seconds.
- **Defect Resolution:** Fixes the clipping defect in historical `fig_s03` where FedTGE was truncated at 110 seconds. FedTGE requires 177.0s on Cora, 773.3s on PubMed, and 399.9s on Reddit, all accurately displayed. Title and legend are cleanly separated.
- **Proposed Caption:**
  > *Figure I: Recorded federated training-loop runtime over 50 communication rounds on identical GPU hardware (Seed 42). (a) Logarithmic-scale comparison across all three benchmark datasets. (b) Linear-scale breakdown on PubMed. Timings measure the active local training and server aggregation loop; they do not measure offline graph partitioning or descriptor precomputation. ETD-FGL incurs minimal overhead ($\le 1.1\times$ FedAvg), whereas FedTGE requires orders-of-magnitude more compute (773.3 seconds on PubMed) due to iterative graph entropy calculations.*

---

### Supplementary Figures S1 & S2
- **`Fig_S_Reddit_Seed_Heterogeneity.png`:** In-depth 3-panel seed breakdown on Reddit across Seeds 42, 43, and 44, detailing why Seed 43 exhibits elevated vulnerability (ASR 34.82% vs 0.85% on Seed 42 and 6.58% on Seed 44) under heavy graph structural heterogeneity.
- **`Fig_S_Standard_vs_Controlled_Comparison.png`:** Side-by-side empirical comparison proving that normalizing ablated channel weights to 1.0 (Standard Ablation) inflated the topology coefficient from $9/13$ to $1.0$ (+44%), masking the contribution of the update channel. Under held-constant coefficients (Controlled Ablation), the necessity of both topology and update channels is rigorously demonstrated.
