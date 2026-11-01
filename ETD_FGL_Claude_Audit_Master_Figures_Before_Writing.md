# ETD-FGL: scientific revision gate -> safe master integration -> camera-ready figures

You are working inside the local ETD-FGL repository. Perform the work in THIS ORDER. Do not write or edit the manuscript at any point. The author and ChatGPT will write it interactively later, section by section.

## Authoritative context and evidence

- Current investigated method: commit `80a321027b26853eee1c2c4f415e1ec9c1f4961c`.
- Existing working audit branch: `revision-audit-2026-11`, last reported HEAD `3084163031c9e535eedf044ab555c9e26fbd45d7`.
- Existing three commits to preserve:
  - `28340f89448a654dcff491c2e15a8a11b9a2fc10` (runtime provenance).
  - `7a1cc1fc11144a8824b52e3061a3716791a2fbc4` (DMGNN-FL diagnostics).
  - `3084163031c9e535eedf044ab555c9e26fbd45d7` (raw recompute and figure tools).
- Previously master/origin/master: `953e250` (REVERIFY in the working repo; do not assume remote has not moved).
- Source-of-truth handoff: `ETD_FGL_NEW_CODE_HANDOFF/README.md`, `SCIENTIFIC_REVISION_AUDIT.md`, `ETD_FGL_COMPLETE_CODE_TRUTH.md`, `EQUATIONS_AND_PSEUDOCODE.md`, `CLAIMS_EVIDENCE_MATRIX.md`, `RESULTS_AND_STATISTICS.md`, `FIGURE_MANIFEST.md`, and `TABLES/*.csv`.
- The old ETD-FGL manuscript is `old/main.tex`. Do not assume `../main.tex` is that manuscript; it may be an unrelated IoT-routing article.
- The InsightAI HDQL-GTE assessment concerns a different manuscript. Do not treat it as formal ETD-FGL reviewer comments.
- No authentic referee letter has been located. Explicitly mark FORMAL REVISE COMPLIANCE = NOT VERIFIABLE until that letter is supplied.

## Non-negotiable safeguards

1. Preserve all tracked, modified, untracked and ignored user work. In particular, never delete or overwrite `build_figure_revision_v2.py`, `v3.py`, `v4.py`, `paper_artifacts/`, earlier handoff directories/zips, or instruction files. Inspect them if useful, but do not stage them blindly.
2. NEVER run `git reset --hard`, `git clean -fd`, force push, interactive history rewrite, `git push --force`, destructive checkout or automatic `git add .`.
3. Do not modify `main.tex`, `old/main.tex`, `.bib` files, article sections, abstract, captions in manuscripts, or PDF manuscripts. You may create separate caption recommendations as Markdown.
4. Do not retrain or rerun full experiments just to improve figures. Regenerate figures solely from auditable recorded raw results and derived CSVs. New scientific claims that require experiments must be flagged PENDING, not claimed as proven.
5. Do not invent seed 45/46 results, 5-seed bootstrap CIs, hardware metadata for old runs, significance, GNNExplainer use, or a causal explanation of Reddit seed 43.
6. If a proposed algorithm/protocol fix changes run semantics, do not mix old result figures with it. Identify the result invalidation and isolate the change for author review rather than silently applying it.

## Phase A: revision adequacy and code correctness BEFORE master/figure work

A1. Read the current authoritative source files, tests, and `ETD_FGL_NEW_CODE_HANDOFF` audit. Check the code against the 31-row internal audit matrix with line-level evidence. Also check repository state (HEAD, branches, status, reflog, recent commits, differences since `80a3210`). Inspect any local formal referee letter if one newly exists; otherwise report that formal referee compliance cannot be determined.

A2. In `PRE_WRITING_SCIENTIFIC_GATE.md`, separate:
- CODE VERIFIED: 5-D label-free descriptor; one-sided robust map with `max(1.4826 * MAD, std, 1e-8)`; 9/13, 4/13 fusion; `clip(exp(-3R), 0.02, 1)` trust; sample weighting; checkpoint by clean validation accuracy.
- SCIENTIFIC LIMITATIONS STILL OPEN: server access to exact clean and attacked graphs; topological anomaly degeneracy (attacker ~0.848284, benign 0 in all 84 ETD-type audits); label-aware partitioning over all splits; induced-subgraph training versus full-graph evaluation; information-asymmetric and untuned adapted baselines; single static attacker, IID setting, only seeds 42-44; missing significance evidence; timing not comparable.
- OLD PAPER CLAIMS TO REMOVE: under-5% ASR from round 1, claimed cause of Reddit seed 43, within 0.5 pp of Clean FedAvg, <=4.7% attacker share, GNNExplainer for DMGNN-FL, under-5-ms overhead, and unsupported "robust/general/real-world" superiority.
- CORRECTABLE SOFTWARE DEFECTS vs DESIGN CHANGES REQUIRING RERUNS. Do not call a limitation fixed merely because the prose can disclose it.

A3. Test the current code (`pytest -q`, relevant integrity checks and scientific invariants) before and after any justified NON-SEMANTIC fix. If a clear, small reproducibility/plotting defect is confirmed, fix it and add a focused regression test. If no additional verified code fixes are needed, report that; do not create meaningless commits. Do not change the defense algorithm or experimental protocol without explicit scientific justification and clearly documented result invalidation.

A4. Deliver a compact PASS/FAIL/OPEN status for each relevant item. Distinguish "software tests pass" from "scientific revise is satisfied". Do not proceed to strong-claim manuscript writing; this task is only pre-writing preparation.

## Phase B: preserve the existing commits and integrate safely into local master

B1. Before changing branches, print and record `git status --short --branch`, `git branch -vv`, `git log --oneline --decorate -12`, `git remote -v`, and all file changes. Check whether the current `master` is an ancestor of `revision-audit-2026-11` and whether local `master`/`origin/master` have diverged. Create a non-destructive backup ref/branch pointing to the pre-integration master and record its SHA.

B2. On `revision-audit-2026-11`, make focused commits for any justified code/test/provenance corrections from Phase A, staging only named files. Keep old untracked work untouched.

B3. If ancestry allows, switch to local `master` safely and integrate the audited branch using a FAST-FORWARD merge only (`git merge --ff-only revision-audit-2026-11`). Verify the three existing commits are now in `master` history. If FF cannot succeed, branch switching would overwrite any user file, or a remote conflict exists: STOP the integration and report the issue. Never force an automatic merge or delete data.

B4. Do NOT push to GitHub; the request is to update local master. Report precisely whether local master moved and whether origin/master is unchanged. At the end of all phases, the checked-out branch must be `master` only if safe integration succeeded.

## Phase C: redesign/polish all journal figures ON master, then commit the figure work

C1. Use source scripts and the VERIFIED existing `TABLES`/raw logs, not screenshots or hand-typed numbers. Adopt a single publication-quality design system: consistent vector PDF exports (embedded fonts where possible), legible labels at single/double-column publication sizes, consistent unit notation, clean margins, non-overlapping legends, colorblind-conscious encoding with line styles/markers, no unnecessary gradients/decorations. Optionally export PNG previews at 300 dpi. Keep plotting source editable and rerunnable from CSV inputs. No actual axes, point values or error bars may be altered for appearance.

C2. Figure-specific corrections (follow `FIGURE_MANIFEST.md` mapping):

- **Fig 1 architecture (`etdfgl_architecture_workflow`)**: redraw completely for readability. Fix the cramped robust-map box and equation overflow. Ensure BOTH benign and attacker clients contribute current graphs to static topology evidence AND all clients contribute round-wise model deltas to update evidence. Display clean reference availability as an explicit SIMULATION ASSUMPTION and avoid implying privacy-preserving operation. Show one-time topology step, per-round update, robust map, fusion, sample-weighted aggregation, clean-VALIDATION checkpoint selection, with correct arrow direction. State training-node poisoning (not "test node poisoning"). Never display unsupported "ASR <5% from round 1", "<=4.7%", or "benign trust >=85% at every round".
- **Fig 2 baseline comparison**: improve the eight-method legend and distinguish seed-42 SINGLE-RUN evidence from n=3 summaries. Keep exact percentages and adapted-baseline labels. Avoid visual impression that original algorithm papers were exactly reproduced.
- **Fig 3 accuracy vs ASR**: no invented cross-dataset Pareto frontier; desirable region is lower-right. Resolve overlapping PubMed/Reddit points, make seed-42 markers versus 3-seed means +/- sample SD unambiguous, and move oversized legends outside panels.
- **Fig 4 multi-seed robustness**: show individual seeds 42/43/44 alongside mean and sample SD; clearly annotate Reddit seed 43 ASR 34.82% without attributing it to community overlap. No significance stars.
- **Fig 5 round dynamics**: show all 50 rounds and visually preserve large early spikes; clarify that the final paper result is evaluated at the best-clean-validation checkpoint, not necessarily round 50. Do NOT claim ASR was low from round 1. Improve line readability without hiding early events.
- **Fig 6 controlled ablation**: clearly distinguish fixed-coefficient variants (9/13 topo and 4/13 update) from renormalized standard ablation. Show paired per-seed differences when feasible; n=3, sample SD, and "no statistical test" are explicit. Do not imply statistical significance.
- **Fig 7 attacker weight**: clean up the noisy trace of the no-topology variant using line opacity/width or a clearly labelled secondary smoothed trend only if raw trace remains visible; keep uniform 20% reference and exact units. Do not state a false universal <=4.7% ceiling.
- **Fig 8 runtime**: do NOT use as evidence of low overhead or speed superiority. Mark as SUPPLEMENTARY / EXPLORATORY ONLY with the single-run, unrecorded-hardware and cross-suite inconsistency caveat; if no honest presentation is possible, produce the script and a "not publication ready" note instead of promoting it as a main figure.

C3. For every figure, test data-to-pixel traceability: list exact input file, selected methods/seeds, aggregation rule, SD convention, axis limits, labels, output filenames, source code SHA and reproducibility command. For chart 1, provide a source-code-to-box correspondence. Use `pdfinfo` and high-resolution rendering of all figure PDFs, inspect full-page PNG previews for clipped text, overlapping legends and tiny type; iterate until readable. Compare critical plotted values against CSVs with automated assertions. Do not claim a visual QA pass without looking at all figures.

C4. Commit figure-generation script changes, manifests, small final publication assets and QA tests using focused Git commits ON local master (e.g. `figures: rebuild faithful ETD-FGL architecture` and `figures: regenerate and validate publication plots`). Do not commit large raw data, old output archives or thousands of unrelated files. Preserve original plots in versioned separate filenames or directories, not destructive overwrites of user files.

## Phase D: final handoff and STOP before manuscript writing

Deliver a compact self-contained folder `ETD_FGL_PRE_WRITING_READY/` with:
- `PRE_WRITING_SCIENTIFIC_GATE.md` (scientific audit and honest status of formal referee compliance)
- `MASTER_INTEGRATION_AND_COMMITS.md` (old and new SHA; ancestry checks; branch; explicit list of commits; whether push occurred)
- `FIGURE_QA_REPORT.md` (per-figure corrected issues, evidence, dimensions, visual QA pass/fail)
- `FIGURE_MANIFEST.md` (exact source CSV and script provenance)
- `FIGURES/` (final PDFs and readable previews; Figure 8 clearly separated if exploratory)
- `TABLES/` (only the supporting small verified tables)
- `CODE_TRUTH_UPDATE.md` (any changes since the prior code-truth handoff)
- `OPEN_SCIENTIFIC_ITEMS.md` (items needing actual experiments/new code/author decisions)
- `README.md` (how ChatGPT should use this package)

Create `ETD_FGL_PRE_WRITING_READY.zip`, verify archive integrity, report its absolute path and size.

Final response must provide:
1. Is current code faithful to what was implemented? YES/NO with evidence.
2. Does it demonstrably satisfy a formal referee letter? UNVERIFIABLE unless an authentic letter is found.
3. Which substantive scientific concerns remain unresolved?
4. Did the local master integration succeed, and what is its exact HEAD SHA?
5. Every new commit SHA and the test results.
6. Which figures pass camera-ready QA and which are caveated?
7. Where is the new ZIP?

**STOP. DO NOT WRITE, REWRITE, OR EDIT ANY ARTICLE TEXT OR MANUSCRIPT FILE.** The author and ChatGPT will begin the actual scientific writing later, one section at a time.
