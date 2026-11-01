# ETD-FGL Figure Comparison and Quality Audit Report (v3 vs. v4)

**Document Purpose:** Systematic scientific audit comparing Revision v3 and Revision v4 across all visual elements, typography, coordinate placements, units, and mathematical qualifications.

---

## 1. Evolution and Defect Resolution Matrix (v3 to v4)

| Figure / Component | Revision v3 Implementation | Revision v4 Final Targeted Repair | Visual & Scientific Verification Status |
| :--- | :--- | :--- | :--- |
| **Figure H (Accuracy–Robustness Scatter)** | Retained "Optimal Defense Region" box and arrow; included text callout boxes next to multi-seed points; asserted cross-dataset Pareto shift. | Completely removed "Optimal Defense Region" box and arrow; removed all point text callout boxes; clean scatter points for baselines, 2D error whiskers on multi-seed centroids; exact numerical coordinates reported in figure caption. | **RESOLVED & VERIFIED:** Visual inspection confirmed zero overlapping annotations; clean scatter points and 2D whiskers; no cross-dataset Pareto assertions. |
| **Figure I (Training Runtime Comparison)** | Legend, suptitle, and panel titles had tight vertical clearance; potential visual crowding at print size. | Decoupled vertical hierarchy: suptitle at $y=0.985$, horizontal legend at $y=0.910$, subplots adjusted with `top=0.81`. Disjoint vertical zones verified. FedTGE bars unclipped at 177s, 773s, 400s. | **RESOLVED & VERIFIED:** Visual inspection confirmed clear separation between title, legend, and subplot headings at print resolution. |
| **Figure A (Baseline Comparison Overview)** | Suptitle and legend were in close vertical proximity; subplots had potential collision at certain display scalings. | Decoupled vertical layout: suptitle at $y=0.980$, legend at $y=0.925$, subplot grid top constrained to $0.85$. Non-overlapping vertical hierarchy confirmed. | **RESOLVED & VERIFIED:** Confirmed distinct non-overlapping vertical zones across all 4 subpanels. |
| **Figure D (Multi-Seed Robustness)** | Reddit Seed 43 callouts placed at $x=1.60$, which visually encroached upon the top edge and error whisker of the Attacked FedAvg bar ($x=1.86$). | Moved callout box in Panel (b) to $x=2.14, y=88.0$ (straight vertical arrow down to seed point at $y=34.8\%$) and in Panel (c) to $x=2.28, y=52.0$ with $ha=\text{"left"}$ and $x \in [-0.45, 3.00]$. Completely off all bars and whiskers. | **RESOLVED & VERIFIED:** Visual inspection confirmed callouts are completely free of all error whiskers, bar edges, and adjacent labels. |
| **Figure F (Trust and Defense Mechanisms)** | Panel (d) asserted constant scale-invariance down to $d=0$ without qualifying the nonzero-drift regime or separating anomaly score from weight percentage. | Panel (d) fully qualified to $d > 10^{-8}$ regime ($K=5, M=1$); dual y-axis clearly separates dimensionless anomaly score ($A_0^{\text{topo}} \approx 0.8483$, left axis) from aggregation weight share ($w_0 = 4.12\%$, right axis); piecewise zero boundary at $d=0$ plotted cleanly ($A_0 = 0.0, w_0 = 20.0\%$). | **RESOLVED & VERIFIED:** Dual y-axis verified; clear visual distinction between dimensionless anomaly score and percentage weight share. |
| **Figure G (Attack Effect & Defense Gain)** | Numeric labels in Panel (b) used `% pts`; labels were close to error bar caps. | Replaced `% pts` with standard `pp` (`+56.8 pp`, `+8.3 pp`, `+60.3 pp`); placed numeric labels above error bar caps; verified clear positive reduction signs without whisker occlusion. | **RESOLVED & VERIFIED:** Visual inspection confirmed labels sit comfortably above caps with zero error bar occlusion. |
| **Figure C (Controlled Scientific Ablation)** | Axis titles and delta labels used `% pts`. | Standardized all paired difference labels and axis titles to `pp` (percentage points); preserved exact within-seed arithmetic deltas. | **RESOLVED & VERIFIED:** Clean typography, consistent `pp` units across all panels. |

---

## 2. Visual Inspection and Coordinate Verification

Each of the 14 finalized 600 DPI PNG images in `paper_artifacts/ETDFGL_Figure_Revision_v4/figures/` was visually inspected at 100% print resolution:

1. **`Fig_A_Baseline_Comparison_Overview.png`:**
   - Suptitle, legend, and panel headings occupy distinct vertical bands.
   - Panel (c) Attack Effect zero line is sharp and legible.
   - Panel (d) runtime values atop bars do not touch panel borders.
2. **`Fig_A1_Baseline_Comparison_Cora.png`, `Fig_A2_Baseline_Comparison_PubMed.png`, `Fig_A3_Baseline_Comparison_Reddit.png`:**
   - Exact numerical labels atop all bars have ample vertical clearance.
   - Attack effect zero reference lines cleanly separate positive vs negative values.
3. **`Fig_B_Standard_Ablation.png`:**
   - 6 variants clearly distinguishable via high-contrast palette.
   - Overlaid jittered seed points (Seeds 42, 43, 44) do not collide with bar borders or error whiskers.
4. **`Fig_C_Controlled_Ablation.png`:**
   - Paired deltas labeled with `+X.X pp` or `−X.X pp`.
   - Zero lines in delta panels clearly demarcate defense degradation vs improvement.
5. **`Fig_D_MultiSeed_Robustness.png`:**
   - Reddit Seed 43 callouts in Panels (b) and (c) are positioned in open canvas space.
   - Arrows point directly to the annotated red triangular markers without crossing any bars or error whiskers.
6. **`Fig_E_Learning_Dynamics.png`:**
   - 50 communication rounds plotted with clean step-wise curves.
   - Clean FedAvg and ETD-FGL trajectories overlap closely in Clean Accuracy, confirming utility preservation.
7. **`Fig_F_Trust_Defense_Mechanisms.png`:**
   - Panel (d) dual axis shows left y-axis in blue ($A_0^{\text{topo}} \in [0, 1]$) and right y-axis in dark gray ($w_0 \in [0, 25\%]$).
   - Zero-drift boundary ($d=0$) shows hollow markers at $A_0=0.0$ and $w_0=20.0\%$, with immediate step to plateau for $d > 0$.
8. **`Fig_G_Attack_Effect_and_Defense_Gain.png`:**
   - Panel (b) positive reduction bars labeled `+56.8 pp`, `+8.3 pp`, `+60.3 pp` positioned strictly above error bar caps.
   - No overlap between suptitle, legend, and subplot headings.
9. **`Fig_H_Accuracy_ASR_Tradeoff.png`:**
   - Zero text collision. All baseline points rendered as clean geometric markers without text clutter.
   - Multi-seed centroids show distinct 2D error whiskers in both dimensions.
   - Header legend clearly identifies all 8 methods.
10. **`Fig_I_Training_Runtime_Comparison.png`:**
    - Panel (a) logarithmic scale ($10^0$ to $3 \times 10^3$ s) displays all methods.
    - Panel (b) linear scale PubMed extends to 900s; FedTGE bar (773.3s) is fully unclipped.
    - Suptitle, legend, and panel headings occupy strictly disjoint vertical zones.
11. **`Fig_S_Reddit_Seed_Heterogeneity.png` & `Fig_S_Standard_vs_Controlled_Comparison.png`:**
    - Supplementary figures adhere to identical typography, resolution, and margin standards.
