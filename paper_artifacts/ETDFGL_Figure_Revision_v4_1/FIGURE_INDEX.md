# ETD-FGL Scientific Figure Index (Revision v4.1)

This index documents the complete suite of 14 publication-grade scientific figures produced for the ETD-FGL manuscript revision. All figures are generated at **600 DPI PNG** resolution, adhering strictly to academic typography, high contrast, clean white backgrounds, and colorblind-safe palettes.

### Revision v4.1 Targeted QA Repairs:
1. **Figure F (Defense Mechanisms & 5-Client Analytic Regime):**
   - Corrected numerical boundary: for drift vector $\mathbf{v} = [d, 0, 0, 0, 0]$, code uses `mad = max(0.4*d, 1e-8)`. The constant $0.848284$ anomaly plateau starts at $d \ge 2.5 \times 10^{-8}$ (where $0.4d \ge 10^{-8}$), NOT $d > 10^{-8}$.
   - Below $2.5 \times 10^{-8}$, $\text{MAD} = 10^{-8}$ and $z = d / 10^{-8}$ varies continuously, passing through $A_0 = 0.0$ at $d=0$.
   - Explicitly clarified that $w_0 \equiv 4.12\%$ represents the **Fixed No Update** example ($A^{\text{upd}} = 0$) under equal client sample sizes ($n_i = n$).
   - Corrected Panel (b) caption and interpretation: on Cora (Seed 42), the attacker's model update anomaly $A_0^{\text{upd}}$ is identically zero ($0.0000$) across all 50 rounds, showing that attacker downweighting on Cora is driven entirely by the structural topology channel ($A_0^{\text{topo}} \approx 0.8483$).
2. **Runtime Descriptions (Figures A, A1–A3, I):**
   - Corrected FedTGE timings (177s, 773s, 400s) to reflect the full 50-round federated training loop (averaging 3.5s to 15.5s per round), not per-round latency.
   - Removed generic "$\le 1.1\times$ FedAvg" and unsupported ratio range ("$1.02\times$ to $1.21\times$"); reported measured loop runtimes directly (all under 11 seconds across all suites).
3. **Multi-Seed Baseline Labeling and Accuracy Preservation (Figures A, D, H):**
   - Clarified that multi-seed baseline distributions ($75.00\%$, $74.80\%$, $84.90\%$) represent **Attacked FedAvg**, as no 3-seed Clean FedAvg control was run. Clean FedAvg is established on Seed 42 ($76.10\%, 76.30\%, 86.20\%$), preserving accuracy within **1.30 percentage points** (Cora 0.00 pp, PubMed +1.30 pp, Reddit -0.90 pp).
4. **Preservation of 14 PNG Figures:** All 14 PNG figures are preserved unchanged.

---

## Summary of Figure Suite (14 Finalized PNGs)

| Figure Identifier | Filename | Layout | Focus / Purpose | Suggested Manuscript Section |
| :--- | :--- | :--- | :--- | :--- |
| **Figure A (Overview)** | `Fig_A_Baseline_Comparison_Overview.png` | 2×2 Multi-panel | 8-method baseline comparison across Cora, PubMed, Reddit (Acc, ASR, Attack Effect, Loop Runtime) | Section 5.2 (Main Results) |
| **Figure A1 (Cora)** | `Fig_A1_Baseline_Comparison_Cora.png` | 2×2 Multi-panel | In-depth 8-method baseline evaluation on Cora dataset | Section 5.2 / Supplementary |
| **Figure A2 (PubMed)** | `Fig_A2_Baseline_Comparison_PubMed.png` | 2×2 Multi-panel | In-depth 8-method baseline evaluation on PubMed dataset | Section 5.2 / Supplementary |
| **Figure A3 (Reddit)** | `Fig_A3_Baseline_Comparison_Reddit.png` | 2×2 Multi-panel | In-depth 8-method baseline evaluation on Reddit dataset | Section 5.2 / Supplementary |
| **Figure B** | `Fig_B_Standard_Ablation.png` | 2×2 Multi-panel | Standard multi-seed ablation of 6 original variants across Cora, PubMed, Reddit | Section 5.3 (Ablation Studies) |
| **Figure C** | `Fig_C_Controlled_Ablation.png` | 2×2 Multi-panel | Controlled scientific ablation with held-constant coefficients; paired deltas in pp | Section 5.3 (Controlled Ablation) |
| **Figure D** | `Fig_D_MultiSeed_Robustness.png` | 1×3 Multi-panel | Multi-seed robustness (Seeds 42, 43, 44) with collision-free Reddit Seed 43 callouts | Section 5.2 (Multi-Seed Robustness) |
| **Figure E** | `Fig_E_Learning_Dynamics.png` | 2×3 Multi-panel | 50-round convergence trajectories for Clean Accuracy and Backdoor ASR | Section 5.4 (Convergence Dynamics) |
| **Figure F** | `Fig_F_Trust_Defense_Mechanisms.png` | 2×2 Multi-panel | Dynamic client risk breakdown, trust factor, attacker weight, and qualified scale-invariance ($d \ge 2.5 \times 10^{-8}$) | Section 4 / Section 5.4 (Defense Analysis) |
| **Figure G** | `Fig_G_Attack_Effect_and_Defense_Gain.png` | 1×3 Multi-panel | Trigger Attack Effect (zero line), absolute ASR drop (+X.X pp), and relative % gain | Section 5.2 (Defense Effectiveness) |
| **Figure H** | `Fig_H_Accuracy_ASR_Tradeoff.png` | 1×3 Multi-panel | Clean Accuracy vs Robustness scatter with 2D error whiskers; exact coordinates in caption | Section 5.2 (Trade-off Analysis) |
| **Figure I** | `Fig_I_Training_Runtime_Comparison.png` | 1×2 Multi-panel | Training-loop runtime comparison fixing FedTGE clipping (log-scale + linear PubMed) | Section 5.5 (Computational Overhead) |
| **Figure S1** | `Fig_S_Reddit_Seed_Heterogeneity.png` | 1×3 Multi-panel | Per-seed breakdown on Reddit highlighting elevated retention on Seed 43 | Supplementary Material |
| **Figure S2** | `Fig_S_Standard_vs_Controlled_Comparison.png` | 1×2 Multi-panel | Empirical demonstration of how topology coefficient inflation ($9/13 \to 1.0$) masked update channel | Supplementary Material |

---

## Detailed Captions and Technical Specifications

### Figure A: Comprehensive Baseline Comparison Overview
- **Filename:** `Fig_A_Baseline_Comparison_Overview.png`
- **Layout:** 2×2 panels: (a) Clean Test Accuracy (%), (b) Backdoor Attack Success Rate (ASR %), (c) Trigger Attack Effect (percentage points), (d) Training Loop Runtime (seconds, log scale).
- **Methods:** Clean FedAvg, Attacked FedAvg, PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE, ETD-FGL.
- **Datasets:** Cora, PubMed, Reddit.
- **Evaluation Scope:** Single-seed (Seed 42), explicitly noted without fictitious error bars.
- **Caption:**
  > *Figure A: Baseline evaluation of ETD-FGL against seven comparison federated learning and defense methods on Cora, PubMed, and Reddit (evaluated on Seed 42). Distinct vertical spacing separates the title, top legend, and panel headings. (a) Clean test classification accuracy shows that ETD-FGL maintains performance comparable to unattacked Clean FedAvg (within 1.30 pp: Cora 0.00 pp, PubMed +1.30 pp, Reddit -0.90 pp). (b) Backdoor Attack Success Rate (ASR) demonstrates that ETD-FGL restricts backdoor penetration to below 5% on Cora, 1.3% on PubMed, and 1% on Reddit (Seed 42). (c) Trigger Attack Effect ($ASR - \text{Clean Target Rate}$) confirms substantial suppression of the 3-node clique backdoor trigger, dropping to or below zero for ETD-FGL. (d) Recorded training-loop execution runtime across the complete 50 communication rounds plotted on a logarithmic scale; FedTGE incurs 25×–117× greater loop runtime (up to 773s on PubMed) due to dense structural graph entropy calculations.*

---

### Figures A1, A2, A3: Dataset-Specific Baseline Comparisons
- **Filenames:** `Fig_A1_Baseline_Comparison_Cora.png`, `Fig_A2_Baseline_Comparison_PubMed.png`, `Fig_A3_Baseline_Comparison_Reddit.png`
- **Layout:** 2×2 panels per dataset: (a) Clean Test Accuracy, (b) Backdoor ASR, (c) Trigger Attack Effect with zero line, (d) Training Runtime with exact second annotations.
- **Caption (Template for A1/A2/A3):**
  > *Figure A[1/2/3]: Detailed baseline comparison on the [Cora / PubMed / Reddit] benchmark dataset (Seed 42). Panels illustrate: (a) Clean test accuracy, (b) Backdoor Attack Success Rate (ASR), (c) Trigger Attack Effect with a zero reference line, and (d) Recorded training-loop runtime over 50 rounds. Numeric values above bars indicate exact empirical measurements.*

---

### Figure B: Standard Multi-Seed Ablation Study
- **Filename:** `Fig_B_Standard_Ablation.png`
- **Layout:** 2×2 panels: (a) Clean Test Accuracy, (b) Backdoor ASR, (c) Trigger Attack Effect, (d) Attacker Aggregation Weight Share (%).
- **Variants (6):** Full ETD-FGL, Topology-only ($c_{\text{topo}}=1.0$), Update-only ($c_{\text{upd}}=1.0$), No Trust Weighting (uniform 20%), Historical Three-Channel (0.45/0.35/0.20), Attacked FedAvg.
- **Seeds:** 42, 43, 44 (Mean ± sample standard deviation with overlaid jittered seed markers).
- **Caption:**
  > *Figure B: Standard multi-seed ablation study evaluating six original variants across Cora, PubMed, and Reddit (Seeds 42, 43, 44). Bars indicate sample means; error bars denote sample standard deviation ($ddof=1$); overlaid points show individual seed outcomes. (a) Clean accuracy remains stable across all variants. (b) Backdoor ASR reveals that removing trust weighting or relying strictly on update anomaly allows substantial backdoor injection. (c) Trigger Attack Effect displays trigger suppression for Full ETD-FGL and Topology-only. (d) Attacker aggregation weight share demonstrates that trust weighting downweights malicious client contribution from the 20% uniform baseline down to $\le 4.8\%$.*

---

### Figure C: Controlled Scientific Ablation
- **Filename:** `Fig_C_Controlled_Ablation.png`
- **Layout:** 2×2 panels: (a) Backdoor ASR under held-constant coefficients, (b) Paired ASR degradation ($\Delta \text{ASR} = \text{Variant} - \text{Full}$, in percentage points `pp`), (c) Clean Accuracy, (d) Paired Clean Accuracy difference ($\Delta \text{Acc} = \text{Variant} - \text{Full}$, in percentage points `pp`).
- **Variants (3):** Full ETD-FGL ($9/13$ Topo + $4/13$ Upd), Fixed No Update ($9/13$ Topo), Fixed No Topology ($4/13$ Upd).
- **Caption:**
  > *Figure C: Controlled scientific ablation isolating evidence channels with held-constant coefficients across Cora, PubMed, and Reddit (Seeds 42, 43, 44). (a) Backdoor ASR across the three controlled variants. (b) Paired ASR degradation ($\Delta = \text{Variant} - \text{Full ETD-FGL}$) computed seed-by-seed in percentage points (pp). Holding coefficients strictly constant demonstrates that removing the model-update channel results in an observed ASR increase (+1.2 pp on Cora, +0.3 pp on PubMed, and +11.1 pp on Reddit), while removing the topology channel leads to severe defense degradation (+37.3 pp on Cora, +3.6 pp on PubMed, +52.2 pp on Reddit). (c)–(d) Clean accuracy and paired clean accuracy differences confirm that robustness is achieved without compromising clean classification accuracy.*

---

### Figure D: Multi-Seed Robustness Evaluation
- **Filename:** `Fig_D_MultiSeed_Robustness.png`
- **Layout:** 1×3 panels: (a) Clean Test Accuracy, (b) Backdoor ASR, (c) Trigger Attack Effect.
- **Methods:** Attacked FedAvg vs Full ETD-FGL across Seeds 42, 43, 44.
- **Callout:** Reddit Seed 43 ($ASR = 34.82\%$, $\text{Attack Effect} = 34.39\text{ pp}$), positioned cleanly off all bars and error whiskers.
- **Caption:**
  > *Figure D: Multi-seed robustness comparison between unmitigated Attacked FedAvg and ETD-FGL across Seeds 42, 43, and 44. Bars represent sample means; error bars denote sample standard deviations; overlaid points display individual random seeds. Clean accuracy tracks Attacked FedAvg closely (Cora 75.57% vs 75.00%, PubMed 75.50% vs 74.80%, Reddit 84.87% vs 84.90%). On Reddit, Seed 43 is highlighted with an annotated triangular marker ($ASR = 34.8\%$, $\text{Effect} = 34.4\text{ pp}$), placed without colliding with error bars or adjacent labels. This reflects elevated backdoor vulnerability in highly heterogeneous graph partitions, while still achieving a 40.9 pp absolute reduction compared to Attacked FedAvg (75.7%).*

---

### Figure E: Federated Learning Dynamics
- **Filename:** `Fig_E_Learning_Dynamics.png`
- **Layout:** 2×3 panels (Rows: Clean Accuracy, Backdoor ASR; Columns: Cora, PubMed, Reddit) across 50 communication rounds.
- **Methods:** Clean FedAvg, Attacked FedAvg, FedTGE, ETD-FGL.
- **Caption:**
  > *Figure E: Federated learning dynamics over 50 communication rounds on Cora, PubMed, and Reddit (Seed 42). Top row: Clean test accuracy convergence. Bottom row: Backdoor Attack Success Rate (ASR). While unmitigated Attacked FedAvg rapidly assimilates the backdoor trigger within the first 10 rounds, ETD-FGL suppresses backdoor injection from round 1 while maintaining convergence speed and final accuracy comparable to Clean FedAvg.*

---

### Figure F: Trust and Defense Mechanism Dynamics
- **Filename:** `Fig_F_Trust_Defense_Mechanisms.png`
- **Layout:** 2×2 panels:
  - (a) Dynamic Attacker Aggregation Weight ($w_0$) over 50 rounds across Cora, PubMed, Reddit.
  - (b) Risk decomposition for the malicious client on Cora ($A_0^{\text{topo}}$, $A_0^{\text{upd}}$, $R_0$).
  - (c) Trust factor trajectory comparing benign clients ($T_{1..4}$) against the attacker ($T_0$).
  - (d) 5-client analytic anomaly regime ($K=5, M=1, d_{1..4}=0$) showing dimensionless anomaly score $A_0^{\text{topo}} \approx 0.848284$ (left axis) and Fixed No Update weight share $w_0 \equiv 4.12\%$ under equal sample counts (right axis) for $d \ge 2.5 \times 10^{-8}$, with continuous transition down to $A_0 = 0.0, w_0 = 20.0\%$ at $d = 0$.
- **Caption:**
  > *Figure F: ETD-FGL defense mechanism dynamics and 5-client analytic anomaly regime. (a) Dynamic suppression of malicious client aggregation weight ($w_0$) below 5% across all communication rounds. (b) Attacker risk decomposition on Cora showing persistent elevation of topological anomaly ($A_0^{\text{topo}} \approx 0.8483$) while model-update anomaly remains near-zero ($A_0^{\text{upd}} \equiv 0.0000$ across all 50 rounds), demonstrating that defense on Cora is driven primarily by the structural channel. (c) Benign client trust factor preservation ($T_{1..4} > 0.85$) contrasted with attacker trust downweighting ($T_0 < 0.20$). (d) Analytic anomaly regime in a 5-client federation where four benign clients have zero topological drift: because code evaluates $\text{mad} = \max(0.4d, 10^{-8})$, the scale-invariant plateau starts at $d \ge 2.5 \times 10^{-8}$ (where $0.4d \ge 10^{-8}$), producing an invariant outlier z-score $z_0 = d / (0.4d) \equiv 2.50$, an invariant dimensionless anomaly score $A_0^{\text{topo}} \approx 0.848284$ (blue curve, left axis), and an invariant attacker weight share $w_0 \equiv 4.12\%$ under the Fixed No Update condition with equal sample counts (dashed red line, right axis). Below $2.5 \times 10^{-8}$, $\text{mad} = 10^{-8}$ and $z = d / 10^{-8}$ varies continuously, passing through $A_0 = 0.0$ and $w_0 = 20.0\%$ at $d = 0$.*

---

### Figure G: Trigger Attack Effect and Relative Defense Gains
- **Filename:** `Fig_G_Attack_Effect_and_Defense_Gain.png`
- **Layout:** 1×3 panels:
  - (a) Trigger Attack Effect across all 7 attacked methods (Seed 42) with a prominent zero reference line.
  - (b) Absolute ASR reduction ($\text{ASR}_{\text{FedAvg}} - \text{ASR}_{\text{ETDFGL}}$ in percentage points across seeds 42, 43, 44), annotated as positive percentage points (`+56.8 pp`, `+8.3 pp`, `+60.3 pp`) placed above error bar caps.
  - (c) Relative backdoor reduction rate ($(1 - \text{ASR}_{\text{ETDFGL}} / \text{ASR}_{\text{FedAvg}}) \times 100\%$).
- **Caption:**
  > *Figure G: Trigger Attack Effect and quantified defense improvements over unmitigated FedAvg. (a) Trigger Attack Effect ($ASR - \text{Clean Target Rate}$) on Seed 42; non-positive values for ETD-FGL indicate that the model classifies triggered test graphs into the target class at or below the clean baseline rate. (b) Absolute ASR reduction across three seeds: +56.8 pp on Cora, +8.3 pp on PubMed, and +60.3 pp on Reddit, with numeric labels placed above error bar caps to avoid obscuring whiskers. (c) Relative backdoor suppression rate: ETD-FGL achieves 91.6% relative suppression on Cora, 90.3% on PubMed, and 81.1% on Reddit.*

---

### Figure H: Accuracy versus Robustness Trade-off
- **Filename:** `Fig_H_Accuracy_ASR_Tradeoff.png`
- **Layout:** 1×3 panels (separated by dataset: Cora, PubMed, Reddit).
- **Features:** Clean scatter points for single-seed baselines (Seed 42); multi-seed centroids with 2D error whiskers; de-cluttered layout with all callout boxes and "Optimal Defense Region" annotations removed.
- **Caption:**
  > *Figure H: Clean classification accuracy versus backdoor robustness (ASR) trade-off plotted separately for Cora, PubMed, and Reddit. Individual markers denote single-seed baseline methods (Seed 42); prominent diamond and circular markers with 2D cross-whiskers denote multi-seed distributions (mean ± sample standard deviation across Seeds 42, 43, 44). Exact multi-seed centroid coordinates (Clean Accuracy %, ASR %) are: Cora Attacked FedAvg (75.00 ± 0.72%, 62.03 ± 15.38%), Cora ETD-FGL (75.57 ± 1.57%, 5.21 ± 0.88%); PubMed Attacked FedAvg (74.80 ± 3.18%, 9.23 ± 7.36%), PubMed ETD-FGL (75.50 ± 2.01%, 0.89 ± 0.56%); Reddit Attacked FedAvg (84.90 ± 0.80%, 74.42 ± 1.85%), Reddit ETD-FGL (84.87 ± 0.40%, 14.08 ± 18.19%). Note that multi-seed baseline distributions represent Attacked FedAvg (no 3-seed Clean FedAvg control was run). ETD-FGL shifts the model toward high clean accuracy and low ASR within each dataset.*

---

### Figure I: Federated Training Loop Runtime Comparison
- **Filename:** `Fig_I_Training_Runtime_Comparison.png`
- **Layout:** 1×2 panels:
  - (a) Multi-dataset runtime comparison across all 8 methods plotted on a logarithmic scale ($10^0$ to $3 \times 10^3$ seconds), with explicit callouts for FedTGE (Cora: 177s, PubMed: 773s, Reddit: 400s).
  - (b) Linear-scale runtime breakdown on PubMed showing all methods unclipped up to 900 seconds.
- **Vertical Spacing:** Suptitle, legend, and subplot headings occupy disjoint non-overlapping vertical zones.
- **Caption:**
  > *Figure I: Recorded federated training-loop runtime over 50 communication rounds (Seed 42). Suptitle, top legend, and panel headings occupy distinct vertical zones. (a) Logarithmic-scale comparison across all three benchmark datasets. (b) Linear-scale breakdown on PubMed with y-axis extended to 900s, ensuring FedTGE (773.3s) is fully visible and unclipped. Timings measure the active local training and server aggregation loop over 50 communication rounds, excluding offline dataset preparation. FedTGE incurs high compute overhead (177.0s Cora, 773.3s PubMed, 399.9s Reddit for 50 rounds, or ~3.5s to 15.5s per round) due to dense structural graph entropy calculations. ETD-FGL maintains training loop runtimes under 11s across all datasets and seeds (e.g., 3.26s vs 2.88s on Cora Seed 42, 10.53s vs 9.44s on PubMed multi-seed, 7.40s vs 11.07s on Reddit multi-seed), maintaining practical feasibility.*

---

### Supplementary Figures S1 & S2
- **`Fig_S_Reddit_Seed_Heterogeneity.png`:** In-depth 3-panel seed breakdown on Reddit across Seeds 42, 43, and 44, detailing how Seed 43 exhibits elevated backdoor retention (ASR 34.82% vs 0.85% on Seed 42 and 6.58% on Seed 44), illustrating empirical partition sensitivity across random seeds (without unlogged causal conjectures).
- **`Fig_S_Standard_vs_Controlled_Comparison.png`:** Side-by-side empirical comparison demonstrating that normalizing ablated channel weights to 1.0 (Standard Ablation) inflated the topology coefficient from $9/13$ to $1.0$ (+44%), masking the contribution of the update channel. Under held-constant coefficients (Controlled Ablation), both topology and update channels provide non-redundant mitigation.
