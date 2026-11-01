# ETD-FGL Targeted QA Correction Log (Revision v3 to Revision v4)

**Audit Date:** October 17, 2026  
**Target Package:** `paper_artifacts/ETDFGL_Figure_Revision_v4/`  
**Output Deliverable:** `ETDFGL_Figure_Revision_v4.zip`  
**Governing Rule:** No retraining, no synthetic data generation, no modification of manuscript folder `1/`. All repairs derived strictly from frozen code and 132 validated experiment records and checkpoints.

---

## 1. Explicit Before / After Defect Correction Table

| # | Item / Component | Defect in Revision v3 | Correction Applied in Revision v4 | Verification Evidence & Location |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Figure H Annotations** | Retained "Optimal Defense Region" box and arrow; callout boxes adjacent to points caused crowding; implied cross-dataset Pareto dominance. | Removed "Optimal Defense Region" box and arrow completely. Removed all text callout boxes from points. Clean scatter points, 2D error whiskers on multi-seed centroids, simple top legend. Exact coordinates reported in figure caption. | Visual inspection of `Fig_H_Accuracy_ASR_Tradeoff.png`; caption updated in `FIGURE_INDEX.md`. |
| **2** | **Figure I & Figure A Vertical Spacing** | Suptitle, legend, and subplot title headings had tight vertical spacing; potential vertical overlap at print size. | Decoupled vertical layout: expanded top margins (`top=0.85` for Fig A, `top=0.81` for Fig I), anchored suptitles at $y=0.980–0.985$ and legends at $y=0.910–0.925$. FedTGE bars unclipped at 177s, 773s, 400s. | Visual inspection of `Fig_A_Baseline_Comparison_Overview.png` and `Fig_I_Training_Runtime_Comparison.png` at print scale. |
| **3** | **Figure D Callout Placement** | Reddit Seed 43 callouts placed at $x=1.60$ touched the top edge and error whisker of the Reddit Attacked FedAvg bar ($x=1.86$). | Repositioned callout in Panel (b) to $x=2.14, y=88.0$ with vertical arrow down to seed point at $y=34.8\%$; repositioned callout in Panel (c) to $x=2.28, y=52.0$ with $ha=\text{"left"}$ and $x \in [-0.45, 3.00]$. Completely clear of all bars and whiskers. | Visual inspection of `Fig_D_MultiSeed_Robustness.png`. Zero visual collisions confirmed. |
| **4** | **Figure F Scale-Invariance Qualification** | Asserted scale-invariance down to zero drift ($d=0$) without qualifying the regime or distinguishing dimensionless anomaly from weight share %. | Qualified to nonzero-drift, single-attacker, fixed-client ($K=5, M=1$), and numerical-floor ($d > 10^{-8}$) regime. Implemented dual y-axis: left axis shows dimensionless anomaly score $A_0^{\text{topo}} \approx 0.8483$, right axis shows weight percentage $w_0 = 4.12\%$. Plotted piecewise zero boundary at $d=0$ ($A_0=0.0, w_0=20.0\%$). | Visual inspection of `Fig_F_Trust_Defense_Mechanisms.png`; Section 9.3 of `ETDFGL_COMPLETE_RESEARCH_FACT_SHEET.md`. |
| **5** | **Figure G Numeric Labels and Units** | Panel (b) used `% pts`; numeric labels were placed close to error bar caps, risking whisker occlusion. | Replaced `% pts` with standard `pp` (`+56.8 pp`, `+8.3 pp`, `+60.3 pp`); placed numeric labels strictly above error bar caps; preserved positive reduction signs without whisker occlusion. | Visual inspection of `Fig_G_Attack_Effect_and_Defense_Gain.png`. |
| **6** | **Figure C Units** | Panels (b) and (d) used `% pts` in axis titles and annotations. | Standardized all paired difference labels and axis titles to `pp` (percentage points); preserved exact within-seed arithmetic deltas. | Visual inspection of `Fig_C_Controlled_Ablation.png`. |
| **7** | **Fact Sheet Substantive Content** | Only the header was revised in v3; unsubstantiated promotional language ("statistically significant", "proves necessity", "causal analysis", "first systematic", "state-of-the-art", "no clean accuracy sacrifice") remained across Sections 1, 6, 8, 9, 10, 14. | Comprehensive rewrite: purged all promotional buzzwords; replaced with objective descriptions of sample means, empirical deltas, and qualified mechanisms; standardized units to `pp`; corrected baseline runtime notes and DMGNN-FL Reddit notes. | Substantive rewrite of `ETDFGL_COMPLETE_RESEARCH_FACT_SHEET.md` in `paper_artifacts/ETDFGL_Figure_Revision_v4/`. |
| **8** | **Claim Matrix Audit** | DMGNN-FL 0-edge pruning was classified as verified without edge logs; observations vs mechanisms were insufficiently distinguished. | Audited all entries: observations and calculated quantities classified as **Verified**; proposed mechanisms (DMGNN-FL pruning count, PubMed citation sparsity, Reddit Seed 43 degree variance) classified as **Hypothesis**; hardware specifics and cross-dataset Pareto assertions classified as **Not verified**. | Audited `CLAIM_TO_EVIDENCE_MATRIX.md` in `paper_artifacts/ETDFGL_Figure_Revision_v4/`. |
| **9** | **Metrics-Availability Report** | Stated that missing prediction arrays logically requires model retraining to obtain F1 scores. | Corrected: missing saved predictions prevents deriving F1 from current scalar summaries, but does NOT logically require retraining because 132 `best_model.pt` checkpoints exist on disk for an approved inference-only evaluation. | Section 3 of `MISSING_EXPERIMENTAL_EVIDENCE.md` and row 32 of `CLAIM_TO_EVIDENCE_MATRIX.md`. |
| **10**| **Experiment Records and Checkpoints** | Ambiguity between 132 completed runs and repeated citations; checkpoint count unverified. | Audited and verified on disk: exactly 132 completed experiment records (`final_summary.json`) and exactly 132 matching saved checkpoint files (`best_model.pt`) exist across the 4 experiment suites. | Section 1 of `MISSING_EXPERIMENTAL_EVIDENCE.md` and `FIGURE_SOURCE_MAPPING.md`. |
| **11**| **Validation of Artifacts** | Risk of visual text collision or manuscript contamination. | All 14 PNGs generated at 600 DPI, visually inspected, numerical values verified against raw data, and manuscript directory `main paper/1/` verified completely untouched. | Visual inspection log below; git status confirming `1/` untouched. |
| **12**| **Final Deliverable** | Previous delivery was Revision v3. | Compact `ETDFGL_Figure_Revision_v4.zip` packaged with 14 finalized PNGs, complete report suite, and explicit audit trail. | Deliverable zip created in `paper_artifacts/`. |

---

## 2. Visual Inspection Log (Print-Scale QA)

Every final PNG file in `paper_artifacts/ETDFGL_Figure_Revision_v4/figures/` was visually inspected at 100% scale using image rendering tools:

1. **`Fig_A_Baseline_Comparison_Overview.png` (600 DPI):**
   - *Suptitle clearance:* Generous breathing room ($y=0.980$) above top legend ($y=0.925$).
   - *Legend placement:* Completely disjoint from subplots ($top=0.85$).
   - *Panel text:* Clean Test Accuracy, Backdoor ASR, Trigger Attack Effect, and Runtime panels show zero text collisions.
   - *Verification:* **PASS**.
2. **`Fig_A1_Baseline_Comparison_Cora.png` (600 DPI):**
   - *Bar labels:* Exact numbers atop bars are clear of panel borders. Zero line in Panel (c) is distinct.
   - *Verification:* **PASS**.
3. **`Fig_A2_Baseline_Comparison_PubMed.png` (600 DPI):**
   - *Bar labels:* Clean and uncrowded.
   - *Verification:* **PASS**.
4. **`Fig_A3_Baseline_Comparison_Reddit.png` (600 DPI):**
   - *Bar labels:* Clean and uncrowded.
   - *Verification:* **PASS**.
5. **`Fig_B_Standard_Ablation.png` (600 DPI):**
   - *Jittered scatter markers:* Overlaid points for Seeds 42, 43, 44 are distinct and do not obscure error whiskers.
   - *Verification:* **PASS**.
6. **`Fig_C_Controlled_Ablation.png` (600 DPI):**
   - *Units:* All paired difference labels and titles use `pp` (percentage points).
   - *Annotations:* `+X.X pp` and `−X.X pp` clearly positioned.
   - *Verification:* **PASS**.
7. **`Fig_D_MultiSeed_Robustness.png` (600 DPI):**
   - *Callouts:* Reddit Seed 43 callouts are completely off all bars and whiskers. Panel (b) is centered at $x=2.14, y=88.0$ with vertical arrow; Panel (c) is placed at $x=2.28, y=52.0$ with $ha=\text{"left"}$.
   - *Whisker clearance:* Whiskers in Reddit Attacked FedAvg and ETD-FGL have zero overlap with text boxes.
   - *Verification:* **PASS**.
8. **`Fig_E_Learning_Dynamics.png` (600 DPI):**
   - *Curves:* 50 rounds plotted cleanly; step-wise trajectories legible.
   - *Verification:* **PASS**.
9. **`Fig_F_Trust_Defense_Mechanisms.png` (600 DPI):**
   - *Dual y-axis:* Panel (d) clearly separates left axis ($A_0^{\text{topo}} \approx 0.8483$, blue) and right axis ($w_0 = 4.12\%$, dashed gray).
   - *Zero boundary:* Piecewise transition at $d=0$ plotted cleanly with hollow baseline markers.
   - *Verification:* **PASS**.
10. **`Fig_G_Attack_Effect_and_Defense_Gain.png` (600 DPI):**
    - *Numeric labels:* Placed above error bar caps; `+56.8 pp`, `+8.3 pp`, `+60.3 pp` clear.
    - *Title/legend clearance:* Disjoint vertical zones confirmed.
    - *Verification:* **PASS**.
11. **`Fig_H_Accuracy_ASR_Tradeoff.png` (600 DPI):**
    - *De-cluttering:* "Optimal Defense Region" box and arrow removed. All point text callout boxes removed.
    - *Centroids:* Clean 2D whiskers on multi-seed centroids. Coordinates reported in caption.
    - *Header legend:* Clearly separates all 8 methods.
    - *Verification:* **PASS**.
12. **`Fig_I_Training_Runtime_Comparison.png` (600 DPI):**
    - *Vertical hierarchy:* Suptitle, legend, and panel headings occupy distinct non-overlapping zones.
    - *Bar visibility:* FedTGE bars unclipped at 177s, 773s, and 400s (PubMed axis extends to 900s).
    - *Verification:* **PASS**.
13. **`Fig_S_Reddit_Seed_Heterogeneity.png` (600 DPI):**
    - *Seed breakdown:* Panels for Seeds 42, 43, 44 clean and legible.
    - *Verification:* **PASS**.
14. **`Fig_S_Standard_vs_Controlled_Comparison.png` (600 DPI):**
    - *Comparison layout:* Clean bar charts showing effect of normalization.
    - *Verification:* **PASS**.

---

## 3. Manuscript Integrity Certification

- **Manuscript Directory (`main paper/1/`):** **ZERO FILES MODIFIED.**
  - `main paper/1/main.tex`: Unmodified.
  - `main paper/1/main.pdf`: Unmodified.
  - `main paper/1/references.bib`: Unmodified.
  - `main paper/1/images/`: Unmodified.
- **Experimental Code & Data:** **ZERO SOURCE FILES OR OUTPUT LOGS MODIFIED.**
  - All original filenames and source paths preserved exact.
  - No models retrained, no checkpoints altered, no fake data generated.
