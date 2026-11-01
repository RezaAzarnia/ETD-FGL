# Claude Code task: Prepare a compact, evidence-verified handoff for revising the ETD-FGL manuscript

You are working inside my CURRENT ETD-FGL code repository. I have already revised the implementation, but the repository is too large to transfer to another assistant. Your job is to examine the code, Git history (if available), existing experiment outputs, and plotting pipeline, and export a SMALL, SELF-CONTAINED, AUDITABLE package that a separate manuscript-editing assistant can use to revise the scientific paper accurately.

## Paper identity and scope

- Target paper: **ETD-FGL: Evidence-Based Topological Defense for Federated Graph Learning Against Backdoor Attacks**.
- Existing manuscript: `main.tex` (with `main.pdf` as the existing rendered reference), if these are present in the repository. If they are not present, use the names and figure map below; do not invent missing content.
- The file named `InsightAI_HDQL_GTE_Readiness_Report_2026-10-01.docx`, if present, analyzes a DIFFERENT paper (HDQL-GTE, blockchain-oracle selection). **Do not transfer its comments or results into ETD-FGL.**
- This is a transfer/inspection task, NOT a request to rewrite the manuscript yet.

## Non-negotiable rules

1. **Read-only for science and code.** Do NOT edit training code, experimental outputs, configuration, Git history, or `main.tex`. Only create the handoff directory described below. Do not delete, rename, or overwrite any existing assets.
2. Do NOT start expensive training, rerun all baselines, or download datasets. You MAY rerender plots from existing verified CSV/JSON/parquet/raw result files if the plotting step is lightweight. State clearly whether any plots were regenerated.
3. Never fabricate results, claim a change without evidence, backfill a missing seed, use unlogged manual values, or silently replace an unfavorable result. Mark missing items `MISSING` or `UNVERIFIED`.
4. Identify the authoritative CURRENT code/config/results. If Git baseline is available, compare against the last manuscript-associated commit/tag or the last documented version. If no reliable old version exists, say `PREVIOUS IMPLEMENTATION NOT AVAILABLE` rather than guessing from timestamps. Record current Git commit, dirty status, relevant commits/tags, and exact file locations.
5. Differentiate the code as implemented, results actually observed, claims in the old manuscript, and proposed explanations. Preserve an honest account of negative results/outliers and limitations.
6. Do not include datasets, checkpoints, virtual environments, caches, model weights, giant logs, or unrelated source code in the package. Do not include secrets, access tokens, or private credentials.
7. Prioritize a compact ZIP (ideally under 20 MB, but do not sacrifice essential readable figures or evidence to meet a size target).

## Required output directory and files

Create a new directory at repository root called `ETD_FGL_PAPER_HANDOFF/` with:

```
ETD_FGL_PAPER_HANDOFF/
  ETD_FGL_CODE_AND_CHANGES.md       # ONE authoritative, comprehensive but concise handoff document
  FIGURE_MANIFEST.csv               # one row for each of the 8 old figures, plus newly required figures
  FIGURES/                         # final usable figures, filenames unchanged where possible
  RESULTS/                         # small, provenance-backed tables / per-seed CSVs where available
  MISSING_AND_UNVERIFIED.md         # concise blocking gaps; no guessed data
  README.md                         # instructions, inventory, Git commit, and SHA256 checksums
```

Finally, create `ETD_FGL_PAPER_HANDOFF.zip` containing the directory. Make sure the Markdown reports and all CSV files open normally. If packaging cannot be completed, provide the absolute paths to the output directory and its components.

## Main document: ETD_FGL_CODE_AND_CHANGES.md

Organize it into these 9 sections. Favor precise tables and short paragraphs over massive code excerpts:

### 1. Executive technical summary
Explain what the current ETD-FGL system actually does, its input/output, the operational threat model, the main contribution, what has materially changed since the manuscript version, and which experimental results have been superseded. Include a 200-400 word editorial-ready overview in English.

### 2. Code architecture and traceability
Create a compact map: component; responsible source file; functions/classes; inputs; outputs; algorithmic role; evidence status. Trace the dataset loader, graph partitioner, poison/trigger injection, clean-reference capture, 5D topology descriptors, topology drift normalization, one-sided robust anomaly transform, model-update distances, risk fusion, trust weights, aggregation, baseline implementations, experiment runner, evaluation metrics, ablations, logging, and figure generators.

### 3. Actual code changes (before -> after)
Use Git commits/diffs and old snapshots when available. For each material change show: affected files/functions; OLD behavior/formula; NEW behavior/formula; why it changed if documented; whether old experimental results are invalidated; specific manuscript sections/equations/tables/figures requiring update; evidence path/commit. Group cosmetic changes separately. If pre-change code is unavailable, write a CURRENT IMPLEMENTATION section and label historical comparisons unknown.

### 4. Exact currently implemented method
Write math in readable LaTeX notation and match every formula to its source-code function and parameter. In particular, verify rather than assume: the five topology coordinates (density, mean degree, normalized degree variance, clustering, triangles/node); graph simplification; authenticated clean reference; client-wise coordinate standardization; median/MAD or STD fallback; one-sided mapping; coordinate-wise median model update; update distance; topology/update mixing coefficients; exponential trust scaling and clipping; sample-count weighting; checkpoint selection; and exact ablation semantics. Record whether code still uses 9/13 and 4/13, exp(-3R), trust floor 0.02, and 5 clients. Never copy an equation from the manuscript if the current code differs.

### 5. Experiment protocols and provenance
Record dataset names and versions, Reddit sampling, partitioning method (IID/non-IID), train/validation/test splits, number of clients and attackers, attack trigger structure/feature vector, poisoning fraction, victim/target definition, number of rounds, local epochs, architecture, learning rates, hyperparameters, seeds, device/hardware, software versions if recorded, checkpoint selection, and evaluation procedures. Distinguish a clean reference graph from what a practical server can observe. Specify how ASR, clean accuracy, clean target rate, attack effect, runtime, attacker aggregation share, benign trust, and errors/uncertainty are computed. Identify paired-vs-unpaired comparisons and sample std convention (e.g. ddof=1).

### 6. VERIFIED current results only
For Cora, PubMed, and Reddit, extract current results across all available baselines, seeds, and ablation variants. Include clean accuracy, ASR, Attack Effect, active-loop runtime, attacker share, and other actually measured metrics. Give the precise data source and run identifier for every reported figure/table. Include a compact OLD MANUSCRIPT vs VERIFIED NEW RESULTS matrix, with `CHANGED`, `UNCHANGED`, `MISSING`, or `UNVERIFIED`; avoid mixing seed-42 results with multi-seed averages. Export small per-seed CSV(s) in RESULTS/ when possible. Do NOT infer per-seed data from rounded means and standard deviations. If a test, confidence interval, or control was not run, explicitly mark it unavailable.

### 7. Manuscript revision map
Map every substantive code/result change to the relevant `main.tex` section, equation/label, table, figure, abstract claim, discussion claim and conclusion claim. Clearly say: KEEP / REVISE / REMOVE / UNVERIFIED, with a replacement-ready factual statement where evidence supports one. Record all required updated captions and table column definitions.

### 8. Scientific consistency and limitation checks
Check at least these points against new evidence:
- Old paper reported Reddit Seed 43 ASR 34.82%; verify the current seed-specific outcome; do not hide an outlier.
- Old Table 6 reported Cora attacker weight 4.76%, whereas old prose and diagrams claimed <=4.7%; correct this discrepancy if it persists.
- Old Figure 3 called the desirable accuracy-ASR region 'upper-left', although higher accuracy is right and lower ASR is down; correct axes/wording. Verify whether a cross-dataset 'Pareto frontier' is scientifically justified.
- Old Figure 5 caption asserted suppression 'from round 1'; check every actual plotted curve before retaining that phrase.
- Distinguish STANDARD renormalized ablation from CONTROLLED fixed-production-coefficient ablation; do not combine their interpretations or label an effect statistically significant without supporting analysis.
- Old abstract and conclusion made strong near-total elimination claims while Reddit multi-seed ASR was 14.08 +/- 18.19%; verify wording against updated results.
- Verify source fidelity and fairness of PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL and FedTGE adaptations; preserve known failure modes and actual configurations.
- Verify reference-graph availability/privacy and secure aggregation assumptions; 1-attacker / static K3 / 20%-poisoning / IID partition assumptions; time measurement boundaries and fairness of runtime comparisons.
- Verify claims such as 'within 0.5% of clean FedAvg', '<5 ms aggregation overhead', and any dominance or statistical significance claims against actual logs.
- Flag all inconsistencies or unsupported causal interpretations without silently fixing the science.

### 9. Open questions and minimal next steps
List only the genuinely missing inputs that prevent paper revision. Prioritize the smallest additional export or experiment that would resolve each issue. Do not independently launch them.

## Exact existing figure map (from old main.tex)

Keep the ORIGINAL base filenames to permit direct LaTeX replacement. Use these as the required eight figure slots; do not presume old plots still match new results.

| Figure | LaTeX label | Required base filename | Content |
|---|---|---|---|
| Fig. 1 | fig:architecture | etdfgl_architecture_workflow.pdf | System workflow, topology and update evidence, risk/trust aggregation |
| Fig. 2 | fig:overall_baselines | overall_baselines.pdf | Seed-42 baseline comparison; clean accuracy and backdoor ASR |
| Fig. 3 | fig:tradeoff | accuracy_robustness_tradeoff.pdf | Clean accuracy versus ASR trade-off |
| Fig. 4 | fig:multiseed_robustness | multiseed_robustness.pdf | Seeds 42/43/44; accuracy and ASR, uncertainties |
| Fig. 5 | fig:learning_dynamics | learning_dynamics_rounds.pdf | 50-round accuracy and ASR trajectories |
| Fig. 6 | fig:controlled_ablation | controlled_ablation.pdf | Fixed-coefficient ablations and paired ASR differences |
| Fig. 7 | fig:attacker_weight_dynamics | attacker_weight_dynamics.pdf | Attacker aggregation weight across rounds |
| Fig. 8 | fig:runtime_figure | fig_s03_training_runtime_comparison.pdf | Measured training-loop runtime |

For each figure:
- Search the current repository for existing vector/source images and corresponding generation scripts and input CSV/JSON. Prefer latest VERIFIED result-linked exports, not newest file by modification time alone.
- Copy the final figure to `FIGURES/` with the exact filename above. Prefer vector PDF with legible embedded fonts; optional preview PNG may be included if helpful and size permits. Preserve necessary multipanel layout, axes, units, legend and uncertainty representation.
- If an existing figure is outdated but its verified input data and plotting script are available, rerender only the plot (not the training) and record it as `REGENERATED_FROM_EXISTING_DATA`.
- If a verified figure cannot be produced, mark it `MISSING` or `STALE` in FIGURE_MANIFEST.csv; do not substitute a misleading old chart. Include optional newly required figures in `FIGURES/EXTRA/`, clearly marked and mapped to requested new content, only if supported by real data.
- Provide one row per figure in `FIGURE_MANIFEST.csv`: `figure_number,latex_label,filename,status,source_script,input_data,run_ids,datasets,seeds,metrics,code_commit,sha256,manuscript_caption_issue,notes`.
- Check visible layout: old architecture figure was dense and the old trade-off plot had overlapping annotations; do not declare figures camera-ready without examining legibility.

## Existing manuscript table slots to update

Match code/results to the following `main.tex` table labels:
`tab:dataset_config`, `tab:seed42_baselines`, `tab:multiseed_robustness`, `tab:ablation_comparison`, `tab:paired_contributions`, `tab:attacker_suppression`, `tab:runtime_comparison`.
Store only small provenance-backed CSV/JSON exports in `RESULTS/`; keep old values clearly separate from current values.

## Final validation and final response

Before finishing:
- Verify all 8 figure slots have an explicit status; every INCLUDED figure opens and has a provenance trail.
- Verify key statistics in Markdown agree with included CSVs and figures; if not, add a prominent discrepancy note.
- Verify the compact package is reasonably small and excludes heavy files.
- In `README.md`, include an inventory with file sizes, current commit/hash, data-result provenance, and SHA256 checksums of packaged figures and data tables.
- Do not claim figures are publication-ready when text overlaps, labels are illegible, units are missing, or the figure does not match current experimental settings.
- The top of the main Markdown must contain a 1-page `START HERE` summary so another assistant can immediately begin editing the manuscript.

In your final chat response, give ONLY: (i) the absolute path of `ETD_FGL_PAPER_HANDOFF.zip`, (ii) the path of the main Markdown report, (iii) the number of verified figures out of 8, (iv) any critical missing evidence in up to five sentences. DO NOT paste the full repo or full report into chat.
