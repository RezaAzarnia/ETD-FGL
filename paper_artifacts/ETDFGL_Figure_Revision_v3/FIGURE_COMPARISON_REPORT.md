# ETD-FGL Figure Comparison and Quality Audit Report (Historical vs. v2 vs. v3)

This report provides a systematic scientific audit comparing the historical figures (in `1/images/etdfgl/`), the intermediate revision (`ETDFGL_Figure_Revision_v2`), and the final publication-ready figures in `ETDFGL_Figure_Revision_v3/figures/`.

---

## 1. Evolution and Multi-Generation Defect Resolution Matrix

| Evaluation Area | Historical Figure (in `1/images/etdfgl/`) | Revision v2 Figure | Final Redesigned Figure (Revision v3) | Status & Major Fix in Revision v3 |
| :--- | :--- | :--- | :--- | :--- |
| **Figure G (Attack Effect & Defense Gain)** | *None (Scattered metrics)* | `Fig_G_Attack_Effect_and_Defense_Gain.png`<br>*(Defects: Negative signs printed on positive reduction panel; legend collided with suptitle)* | `Fig_G_Attack_Effect_and_Defense_Gain.png`<br>*(Explicit positive percentage points `+56.8% pts`, `+8.3% pts`, `+60.3% pts`; clean suptitle clearance)* | **CRITICAL DEFECT RESOLVED:** Corrected sign convention on Panel (b) to positive percentage points; relocated legend below suptitle with generous margin. |
| **Figure H (Accuracy–ASR Trade-Off)** | `accuracy_robustness_tradeoff.png`<br>*(Single cramped plot, overlapping text annotations, crowded legend)* | `Fig_H_Accuracy_ASR_Tradeoff.png`<br>*(1×3 dataset layout, but text labels collided on Reddit baseline cluster; legend overlapped title)* | `Fig_H_Accuracy_ASR_Tradeoff.png`<br>*(De-cluttered markers; unified header legend below title; clean centroid callouts with 2D error whiskers)* | **READABILITY RESTORED:** Removed colliding text annotations from clustered baseline points (Reddit PD-FL, GSP-FL, DMGNN-FL, FedAvg); decoupled header legend safely below suptitle. |
| **Figure C (Controlled Scientific Ablation)** | `controlled_ablation.png`<br>*(Basic 2-panel chart without paired difference statistics)* | `Fig_C_Controlled_Ablation.png`<br>*(2×2 layout with Backdoor ASR and Clean Acc, but delta panels labeled with ambiguous `%`)* | `Fig_C_Controlled_Ablation.png`<br>*(2×2 layout with paired differences strictly labeled in `% pts` / `% points`)* | **SCIENTIFIC RIGOR STANDARDIZED:** Standardized units on Panels (b) and (d) to percentage points (`% pts`) to prevent confusion with relative percentage changes. |
| **Figure I (Training Runtime Comparison)** | `fig_s03_training_runtime_comparison.png`<br>*(Clipped FedTGE bars at 110s; title overlapped legend)* | `Fig_I_Training_Runtime_Comparison.png`<br>*(Unclipped FedTGE bars up to 773s; decoupled title/legend)* | `Fig_I_Training_Runtime_Comparison.png`<br>*(Preserved full 600 DPI rendering, unclipped bars, high contrast)* | **MAINTAINED:** FedTGE runtime fully unclipped (Cora 177.0s, PubMed 773.3s, Reddit 399.9s). |
| **Figure B (Standard Multi-Seed Ablation)** | *Omitted or conflated with Controlled Ablation* | `Fig_B_Standard_Ablation.png`<br>*(2×2 multi-panel with 6 original variants across 3 seeds)* | `Fig_B_Standard_Ablation.png`<br>*(Preserved full 6-variant multi-seed visualization)* | **MAINTAINED:** Full ETD-FGL, Topology-only, Update-only, No Trust Weighting, Historical Three-Channel, and Attacked FedAvg all fully visualized. |
| **Figure A & A1–A3 (Baseline Comparison)** | `overall_baselines.png`<br>*(8 bars crowded together; lacked runtime and attack effect)* | `Fig_A` + `Fig_A1`, `Fig_A2`, `Fig_A3`<br>*(2×2 multi-panel layouts with runtime & attack effect)* | `Fig_A` + `Fig_A1`, `Fig_A2`, `Fig_A3`<br>*(Preserved 600 DPI publication quality and reference-style bar values)* | **MAINTAINED:** Added Trigger Attack Effect (with zero line) and Runtime. Exact bar values displayed. |
| **Figure D (Multi-Seed Robustness)** | `multiseed_robustness.png`<br>*(Reddit Seed 43 was plotted without contextual callout)* | `Fig_D_MultiSeed_Robustness.png`<br>*(1×3 multi-panel with prominent Reddit Seed 43 callout)* | `Fig_D_MultiSeed_Robustness.png`<br>*(Preserved Reddit Seed 43 callout: ASR = 34.8%)* | **MAINTAINED:** Seed 43 explicitly annotated with a distinctive red triangular marker. Not hidden or smoothed. |
| **Figure E (Learning Dynamics)** | `learning_dynamics.png`<br>*(2×3 panel chart)* | `Fig_E_Learning_Dynamics.png`<br>*(600 DPI, refined typography, preserved convergence curves)* | `Fig_E_Learning_Dynamics.png`<br>*(Preserved step-wise 50-round convergence)* | **MAINTAINED:** Authentic step-wise dynamics over 50 rounds. |
| **Figure F (Defense Mechanisms & Proof)** | `attacker_weight_dynamics.png`<br>*(Lacked client risk breakdown and scale-invariance proof)* | `Fig_F_Trust_Defense_Mechanisms.png`<br>*(2×2 multi-panel combining weight, risk, trust, and invariant)* | `Fig_F_Trust_Defense_Mechanisms.png`<br>*(Preserved weight suppression, risk decomposition, invariant)* | **MAINTAINED:** Risk decomposition ($A^{\text{topo}}, A^{\text{upd}}, R$), benign trust preservation, and mathematical proof of the 5-client constant invariant. |

---

## 2. In-Depth Analysis of Revision v3 Targeted Fixes

### Fix 1: Figure G Sign Convention and Suptitle Clearance
- **The Defect in v2:**
  - Panel (b) was titled `(b) Absolute ASR Reduction`, intended to quantify the drop in backdoor penetration achieved by ETD-FGL relative to unmitigated Attacked FedAvg ($\Delta \text{ASR} = \text{ASR}_{\text{FedAvg}} - \text{ASR}_{\text{ETDFGL}}$).
  - On Cora, ASR drops from 62.0% to 5.2% ($\Delta = +56.8\%$ pts). On PubMed, ASR drops from 9.2% to 0.9% ($\Delta = +8.3\%$ pts). On Reddit, ASR drops from 74.4% to 14.1% ($\Delta = +60.3\%$ pts).
  - However, in Revision v2, the bar annotations erroneously printed negative signs (`-56.8%`, `-8.3%`, `-60.3%`), creating a confusing double negative that implied the attack got worse.
  - Furthermore, the multi-column legend in the top header collided with the suptitle.
- **The Solution in Revision v3:**
  1. The calculation explicitly computes positive reduction: `abs_reductions = [fa_m - et_m for fa_m, et_m in ...]`.
  2. Value labels atop bars are explicitly formatted with a positive sign and percentage points: `f"+{val:.1f}% pts"`.
  3. The y-axis label is formally set to `Absolute Reduction (% points)`.
  4. The figure suptitle is anchored at `y=0.98`, the legend is positioned at `bbox_to_anchor=(0.5, 0.90)`, and subplot top margin is constrained to `top=0.82`, guaranteeing generous visual breathing room and zero overlap.

### Fix 2: Figure H De-Cluttering and Header Layout
- **The Defect in v2:**
  - On the Reddit benchmark, several baseline methods achieve almost identical performance: `PD-FL`, `GSP-FL`, and `DMGNN-FL` all cluster tightly around `Clean Acc ≈ 85.7%` and `ASR ≈ 72.3%`.
  - In Revision v2, each individual baseline point was labeled with a raw text string, causing overlapping text collisions that rendered the labels unreadable.
  - Additionally, the top legend collided with the suptitle.
- **The Solution in Revision v3:**
  1. Removed per-point text labels from individual baseline points. Baseline methods are now identified purely through distinct color palettes and geometric marker symbols (`o`, `s`, `^`, `v`, `D`, `P`, `*`).
  2. Prominent textual annotations are reserved strictly for the two primary multi-seed distributions: `Attacked FedAvg` and `ETD-FGL`.
  3. Both distributions are anchored by 2D error whiskers representing sample standard deviation in both Clean Accuracy ($x$-axis) and Backdoor ASR ($y$-axis).
  4. The unified 8-element horizontal legend is placed below the suptitle with `bbox_to_anchor=(0.5, 0.92)`, and subplots are adjusted with `top=0.80`, eliminating any collision.

### Fix 3: Figure C Percentage-Point Units Standardized
- **The Defect in v2:**
  - Panels (b) and (d) present paired differences: $\Delta \text{ASR} = \text{ASR}_{\text{Ablated}} - \text{ASR}_{\text{Full}}$ and $\Delta \text{Acc} = \text{Acc}_{\text{Ablated}} - \text{Acc}_{\text{Full}}$.
  - In Revision v2, these deltas were labeled with generic `%` signs. This created scientific ambiguity, as a reviewer could easily confuse an absolute difference of percentages (e.g., $14\% - 3\% = 11\%$ points) with a relative percentage change ($(14 - 3)/3 \times 100\% = 367\%$).
- **The Solution in Revision v3:**
  1. Y-axis labels on Panels (b) and (d) are standardized to `Paired Difference (% points)`.
  2. All numeric values atop delta bars are formatted as `f"{val:+.1f}% pts"`.
  3. Panel titles explicitly note `(% points)` to reinforce unit precision.

### Fix 4: Scientific Consistency Regarding Trigger Structure and Poisoning Rate
- **The Inconsistency in Prior Reports:**
  - In certain preliminary sections, trigger size was loosely described as "small clique (e.g., 3 to 5 nodes)" and poisoning rate as "10–20%", which conflicted with the verified codebase.
- **The Resolution in Revision v3:**
  1. In `multidata_suite/config.py` (lines 20–21) and `multidata_suite/backdoor.py` (lines 10–55), the frozen code truth is:
     - `poison_rate = 0.20` (exactly 20% of candidate non-target training nodes in Client 0).
     - `trigger_size = 3` (exactly 3 synthetic nodes per victim node, forming a complete 3-clique $K_3$).
  2. All Revision v3 documentation files (`ETDFGL_COMPLETE_RESEARCH_FACT_SHEET.md`, `CLAIM_TO_EVIDENCE_MATRIX.md`, `FIGURE_INDEX.md`, `MISSING_EXPERIMENTAL_EVIDENCE.md`) strictly standardize on 3-node clique and 20% poisoning budget, explicitly documenting that sensitivity sweeps across $s \in \{2, 4, 5\}$ and $\rho \in \{0.05, 0.10\}$ were not executed.

---

## 3. Summary of Deliverables in Revision v3

All 14 figures have been compiled into `ETD-FGL/paper_artifacts/ETDFGL_Figure_Revision_v3/figures/` at 600 DPI, conforming strictly to the highest standards of scientific reproducibility:

1. `Fig_A_Baseline_Comparison_Overview.png` (2×2 overview)
2. `Fig_A1_Baseline_Comparison_Cora.png` (2×2 Cora)
3. `Fig_A2_Baseline_Comparison_PubMed.png` (2×2 PubMed)
4. `Fig_A3_Baseline_Comparison_Reddit.png` (2×2 Reddit)
5. `Fig_B_Standard_Ablation.png` (2×2 Standard 6-variant ablation)
6. `Fig_C_Controlled_Ablation.png` (2×2 Controlled ablation, `% pts` units)
7. `Fig_D_MultiSeed_Robustness.png` (1×3 Multi-seed robustness, Reddit Seed 43 callout)
8. `Fig_E_Learning_Dynamics.png` (2×3 Dynamics over 50 rounds)
9. `Fig_F_Trust_Defense_Mechanisms.png` (2×2 Mechanism dynamics & scale-invariance)
10. `Fig_G_Attack_Effect_and_Defense_Gain.png` (1×3 Quantified defense gain, positive `+X.X% pts` signs)
11. `Fig_H_Accuracy_ASR_Tradeoff.png` (1×3 De-cluttered Pareto trade-off, 2D error whiskers)
12. `Fig_I_Training_Runtime_Comparison.png` (1×2 Unclipped training loop runtime)
13. `Fig_S_Reddit_Seed_Heterogeneity.png` (1×3 Supplementary Reddit seed breakdown)
14. `Fig_S_Standard_vs_Controlled_Comparison.png` (1×2 Supplementary ablation comparison)
