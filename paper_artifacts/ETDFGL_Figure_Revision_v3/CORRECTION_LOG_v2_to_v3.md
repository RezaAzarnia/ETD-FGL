# ETD-FGL Figure and Evidence Revision v3 — Targeted QA Correction Log

**Scope of Revision:** Targeted scientific corrections addressing the independent QA audit of `ETDFGL_Figure_Revision_v2`.  
**Execution Date:** October 17, 2026  
**Parent Output Directory:** `C:\Users\R_Azarnia\Desktop\main paper\ETD-FGL\paper_artifacts\ETDFGL_Figure_Revision_v3\`  
**Manuscript Integrity:** Manuscript directory `1/` (`main.tex`, `main.pdf`, `references.bib`) was **not modified**.  

---

## 1. Summary of Confirmed QA Defect Corrections

| QA Issue / Target Area | Status in Revision v2 | Corrected in Revision v3 | Verification / Code Resolution |
| :--- | :--- | :--- | :--- |
| **Figure G Signs & Labels** | Panel (b) bar labels had erroneous minus sign (`"−56.8%"`) on positive reduction bars; unit was labeled `%` instead of `% points`. | Erroneous minus sign eliminated. Bars are labeled with explicit positive reduction in percentage points: `+56.8% pts`, `+8.3% pts`, `+60.3% pts`. Y-axis is `Absolute Reduction (% points)`. | `build_figure_revision_v3.py:840` |
| **Figure G Legend Position** | Legend anchored at `y=1.28` caused severe collision with suptitle. | Legend placed cleanly at `y=0.93` below suptitle (`y=0.985`) with `top=0.82` margin. Zero overlap. | `build_figure_revision_v3.py:870` |
| **Figure H Clutter & Collisions** | Individual text labels for tightly clustered baselines collided on Reddit (`PD-FL`, `GSP-FL`, `DMGNN-FL`, `FedAvg`); legend collided with suptitle. | Individual scatter point text clutter eliminated. Unique color/marker encoding in clean header legend. Centroids (`ETD-FGL` and `Attacked FedAvg`) feature clean non-overlapping text boxes. | `build_figure_revision_v3.py:881–955` |
| **Figure C Units** | Panel (b) used `%` (`"+37.3%"`) instead of `% points` for paired differences ($\Delta$ ASR); Panel (d) lacked explicit `% pts` annotations. | All paired difference bars and axes in Panels (b) and (d) are strictly labeled in `% pts` (percentage points): e.g., `+1.2% pts`, `+37.3% pts`, `+0.3% pts`, `−0.9% pts`. | `build_figure_revision_v3.py:465–505` |
| **Trigger-Size Contradiction** | `MISSING_EXPERIMENTAL_EVIDENCE.md` erroneously stated $s = 5$ nodes in Section 3.2, contradicting `config.py` ($s = 3$). | Corrected across all reports: the implemented attack is strictly a **3-node clique ($K_3$, $s = 3$)** trigger. | Fact sheet, missing evidence, and claim matrix updated. |
| **Poisoning-Rate Contradiction** | `MISSING_EXPERIMENTAL_EVIDENCE.md` erroneously stated 10% poisoning rate, contradicting `config.py:20` (`poison_rate = 0.20`). | Corrected across all reports: the local poisoning budget is strictly **20% ($\rho = 0.20$)** of candidate non-target training nodes in Client 0's partition. | Fact sheet, missing evidence, and claim matrix updated. |
| **Figure Padding & Margins** | Several figures had subplots slightly tight against the top legend. | Increased figure heights and set explicit `plt.subplots_adjust(top=0.80..0.88)` across all figures to provide breathing room and professional journal aesthetics. | `build_figure_revision_v3.py` |

---

## 2. Detailed Technical Audit of Corrections

### Correction 1: Figure G Signs, Units, and Legend Placement
- **File:** `figures/Fig_G_Attack_Effect_and_Defense_Gain.png`
- **Defect in v2:**
  1. Panel (b) was titled `(b) Absolute ASR Reduction (FedAvg − ETD-FGL)` with positive values: Cora ($62.03 - 5.21 = +56.82$), PubMed ($9.23 - 0.89 = +8.34$), Reddit ($74.42 - 14.08 = +60.34$).
  2. The code had: `ax_b.annotate(f"−{val:.1f}%", ...)` which rendered a minus sign on top of positive bars (`−56.8%`, `−8.3%`, `−60.3%`).
  3. The unit was rendered as `%` rather than percentage points.
  4. The panel (a) legend was anchored at `(0.5, 1.28)`, colliding with the figure title at `y=1.05`.
- **Implementation in v3:**
  ```python
  # Panel (b): Positive absolute reductions in percentage points (% pts)
  for b, val in zip(bars_b, abs_reductions):
      ax_b.annotate(f"+{val:.1f}% pts", (b.get_x() + b.get_width()/2, val + 2.5),
                    ha="center", fontsize=8.5, fontweight="bold")
  ax_b.set_title("(b) Absolute ASR Reduction (FedAvg − ETD-FGL)", fontweight="bold", pad=8)
  ax_b.set_ylabel("Absolute Reduction (% points)")
  
  # Clean global legend in top header
  fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.93),
             ncol=7, frameon=True, edgecolor="#cccccc")
  fig.suptitle("Figure G: Trigger Attack Effect and Quantified Defense Improvements over FedAvg",
               fontweight="bold", fontsize=12.5, y=0.985)
  ```
- **Outcome:** Graphically consistent, mathematically correct, zero text collisions.

---

### Correction 2: Figure H De-Cluttering and Legend Separation
- **File:** `figures/Fig_H_Accuracy_ASR_Tradeoff.png`
- **Defect in v2:**
  1. Individual text strings were annotated on top of every baseline scatter point. On Reddit, four methods (`PD-FL` at 85.9%/73.1%, `GSP-FL` at 85.5%/73.1%, `DMGNN-FL` at 85.7%/72.3%, and `Attacked FedAvg` at 85.7%/72.3%) occupied virtually identical pixel coordinates, creating an illegible black ink blot.
  2. `axes[0].legend(...)` at `bbox_to_anchor=(-0.05, 1.25)` collided with the suptitle at `y=1.06`.
- **Implementation in v3:**
  1. Eliminated redundant text strings on individual baseline scatter points. Baseline identities are clearly distinguished by their unique color/marker pairs in the header legend.
  2. Placed clean, non-overlapping callout boxes on the two primary comparative centroids: `ETD-FGL (Mean ± SD)` and `Attacked FedAvg (Mean ± SD)`.
  3. Placed a unified header legend at `bbox_to_anchor=(0.5, 0.93)` with `ncol=5`, below the suptitle (`y=0.985`), with subplot `top=0.80`.
  4. Added a clean green directional arrow pointing to the `"Optimal Defense Region\n(High Acc, Low ASR)"`.
- **Outcome:** Clean, publication-ready scatter plot with zero overlapping annotations and zero legend collision.

---

### Correction 3: Figure C Percentage-Point Units
- **File:** `figures/Fig_C_Controlled_Ablation.png`
- **Defect in v2:**
  1. Panel (b) paired ASR differences were annotated as `+37.3%` instead of `+37.3% pts`.
  2. Panel (d) clean accuracy differences lacked explicit `% pts` annotations.
- **Implementation in v3:**
  1. In Panel (b), all bar annotations explicitly use `% pts`: `+1.2% pts`, `+37.3% pts`, `+0.3% pts`, `+3.6% pts`, `+11.1% pts`, `+52.2% pts`.
  2. In Panel (d), all bar annotations explicitly use `% pts`: `+0.3% pts`, `+0.5% pts`, `−0.9% pts`, `+0.2% pts`, `+0.1% pts`, `+0.4% pts`.
  3. Y-axis labels are strictly `Δ ASR (% points)` and `Δ Clean Accuracy (% points)`.
- **Outcome:** Complete unit consistency distinguishing absolute percentages (%) from differences (% points).

---

### Correction 4: Resolution of Trigger-Size and Poisoning-Rate Contradictions
- **Affected Documents:** `MISSING_EXPERIMENTAL_EVIDENCE.md`, `ETDFGL_COMPLETE_RESEARCH_FACT_SHEET.md`, `CLAIM_TO_EVIDENCE_MATRIX.md`.
- **Root Cause Analysis:**
  - In `multidata_suite/config.py`:
    `poison_rate: float = 0.20` (line 20)
    `trigger_size: int = 3` (line 21)
  - In `build_publication_tables.py:166`:
    `"client 0 injects a 3-node clique trigger with fixed sparse feature pattern into 20% of training nodes; target class is class 0."`
  - In `build_manuscript_sections.py:71`:
    `"injects a 3-node clique (K_3) trigger into 20% of training victim nodes assigned to malicious client 0"`
  - However, in `MISSING_EXPERIMENTAL_EVIDENCE.md`, Section 3.2 erroneously mentioned "$s = 5$ nodes" and Section 3.3 mentioned "10% of local training nodes".
- **Correction Applied in v3:**
  - Standardized all markdown documents to state strictly and consistently:
    1. **Trigger structure:** 3-node clique ($K_3$, $s = 3$ nodes).
    2. **Local poisoning budget:** 20% ($\rho = 0.20$) of candidate non-target training nodes in Client 0's partition.
- **Outcome:** 100% internal consistency across the codebase, experiment logs, tables, and documentation reports.
