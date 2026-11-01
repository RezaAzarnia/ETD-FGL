# Claude Code Task: NEW ETD-FGL Code Audit, Review Compliance, Git Commits, and Manuscript Evidence Handoff

## Mission
The ETD-FGL implementation has been substantially rewritten since the prior manuscript and prior handoff. Treat the CURRENT CODE AND CURRENT TRACEABLE EXPERIMENT OUTPUTS as the primary evidence, not the old paper, old handoff ZIP, or earlier prose. We need two things, in this order:

1. Independently evaluate whether the current code actually addresses the available *ETD-FGL revision requirements*, identify missing or unsupported items, and make only clearly justified, low-risk implementation/reproducibility fixes.
2. Commit the necessary, verified changes in Git, and prepare a compact, highly precise evidence package that can be sent to ChatGPT to WRITE A COMPLETELY NEW MANUSCRIPT anchored to the latest method, results, and figures.

Do NOT write the manuscript in this task. Do NOT invent results, claim compliance without evidence, relabel old plots as new, alter numerical files to improve the story, or run expensive model training without permission. No destructive Git operations, no force push, no push unless separately requested.

## Essential context and identity safeguards
- Target paper: ETD-FGL, previously titled "Evidence-Based Topological Defense for Federated Graph Learning Against Backdoor Attacks." Cora, PubMed, and Reddit were used in the old paper. The rewritten code may implement a different method, and a new name/title may be necessary: assess this rather than assuming the old architecture survived.
- The prior ETD-FGL manuscript is believed to be `../old/main.tex` (verify the actual file). WARNING: a file called `../main.tex` was previously identified as a DIFFERENT IoT-routing manuscript; do not compare against it solely because it has the same filename.
- `InsightAI_HDQL_GTE_Readiness_Report_2026-10-01.docx` reviews a DIFFERENT paper (HDQL-GTE blockchain oracle selection). It is NOT an ETD-FGL reviewer letter. Never use its 20 comments as requirements for ETD-FGL.
- The actual formal journal referee/revision letter for ETD-FGL has not yet been independently established in this conversation. Search the repository and nearby provided project files for it. If not found, explicitly say **FORMAL REVIEWER COMPLIANCE CANNOT BE VERIFIED**. Keep a separate internal technical audit; do not misrepresent it as reviewer feedback.
- An old handoff ZIP, if found, is historical evidence only; create an entirely NEW handoff from current code and newest valid runs.

## Phase A: Preserve and identify the exact current state
1. Inspect `pwd`, Git repository root, current branch, HEAD SHA, `git status --short`, recent history, tracked/untracked files, current scripts, configs, test suite, experimental output folders, README/docs and manuscript/reviewer files. Record exact paths, SHA and audit timestamp.
2. Identify what is actually executable, what is dead/legacy code, and which entrypoints produce each current experiment. Find the last known pre-rewrite revision/commit if possible, without guessing. Create a changed/removed/new component map with `git diff`/history where genuinely available.
3. If the working tree is dirty, preserve all user work. Do not reset, clean, overwrite, rebase, or silently stash changes. Use a separate safe branch if appropriate and technically safe. Never commit unrelated existing edits or secrets. Stage only audited paths explicitly.
4. Identify the true authoritative output set: run IDs, seeds, timestamps, artifact hashes, configuration digests, matching source versions, and raw metric manifests. Distinguish current runs from older ones. A recent file modification time is not sufficient proof that an artifact came from the current code.

## Phase B: Evaluate actual revision compliance BEFORE making claims
Build a row-by-row compliance matrix for EACH authentic ETD-FGL reviewer point found in source files. For each row provide:
- Original reviewer comment ID and verbatim requirement (or short exact excerpt) and its document path;
- Required behavior/evidence;
- Current implementation status: VERIFIED / PARTIAL / NOT IMPLEMENTED / NOT VERIFIABLE / NOT APPLICABLE;
- Evidence: precise source `path:line`, relevant config key, test name/result, raw run path and metric/figure;
- Whether the fix needs code changes, new experiments, manuscript qualification, or no action;
- Remaining blocker and the proposed defensible manuscript response.

If no authentic reviewer letter exists, create `FORMAL_REVIEW_NOT_PROVIDED.md`, leave the formal matrix ungraded, and perform the separate internal scientific audit below. Never claim "all reviewer comments addressed" merely because tests pass.

## Phase C: Deep scientific and implementation audit (separate from formal reviewer comments)
Inspect the current implementation, NOT merely docstrings or README, for the following questions. Where old behavior no longer applies, mark REPLACED and document the new design.

1. **Actual algorithm identity**: What is the new method? Main defense idea, novelty relative to named baselines, server/client responsibilities, information available to the server, execution order, state/update flow, and genuine independent contributions. Flag any former "dual-channel", 5D descriptor, MAD mapping, 9/13 vs 4/13 fusion, trust clipping or sample-weighted formula that has been changed or removed.
2. **Threat model and provenance**: Number and fraction of adversarial clients, access/capabilities, attack timing, poison fraction, target class, clique trigger size/features, train/test trigger insertion, label manipulation, assumptions, attacker adaptivity, collusion, and clean reference availability. Check for unjustified claims about private graphs, privacy, secure aggregation, authentic clean pre-attack graphs, and deployability.
3. **Data flow and leakage**: Reconstruct train/validation/test masks, per-client graph partitioning, feature normalization, label access, clean reference construction, topology statistics, checkpoint selection and evaluation. Specifically search for test-label or test-mask leakage into partitioning, tuning, defense scores, selection, threshold calibration, or training. Do not use ASR on the test set for checkpoint selection.
4. **Mathematics vs code**: Extract complete executable equations with variable names, normalization/clipping, threshold/fallback rules, edge cases, aggregation, losses, anomaly scores, sample weights, and tensor dimensions. Include minimal, directly quoted code snippets ONLY where needed to verify formulas; reference `path:line` throughout.
5. **Experiment integrity**: Dataset sources, Cora/PubMed/Reddit variants, preprocessing, class/features/nodes/edges, seeds, client partitioning, GNN backbone, optimizer, epochs/rounds, checkpoint criteria, threat parameters, hyperparameter tuning provenance, hardware/software and any cache/hash validation. Confirm that baselines receive comparable data and experimental budgets.
6. **Baselines**: Trace the real implemented algorithms and any approximations/adaptations for Clean and Attacked FedAvg, PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE, or CURRENT alternatives. Specifically check whether any prior "DMGNN-FL uses GNNExplainer" claim is false and whether it is actually a heuristic edge-ablation implementation. Examine any previously reported FedTGE/test inconsistencies. Do not call a custom adaptation an exact published reproduction.
7. **Reproducibility and code health**: Dependency versions, deterministic seed setup, run manifests, paths, accidental stale outputs, reused caches, test coverage, command reproducibility, result-table aggregation logic, confidence/statistics, and mismatches between saved logs and plots. Run lightweight tests and static checks; do not rerun the heavy federated training suite in this task.
8. **Ablation validity**: State exactly which components are removed and which coefficients remain fixed or are renormalized. Verify paired seeds and independent executions. Distinguish feature ablation from filter removal, and a changed algorithm from a comparable ablation.
9. **Outcome definitions**: Clean accuracy, ASR, clean target rate, net trigger attack effect (percentage points), poisoning success, attacker share, benign suppression, time/memory and any additional current metrics. Record numerators/denominators, whether metrics are per seed, per round, or aggregated, units and direction of improvement.
10. **Statistical and timing claims**: Establish actual independent sample count, report every seed (not only means), sample SD conventions and paired differences. Do not claim statistical significance with no test. Verify timing device, warm-up, GPU synchronization, included preprocessing/training/inference costs and comparisons on identical hardware. Remove unsupported "<5 ms overhead" style claims from proposed manuscript claims.
11. **Old observed contradictions**: Independently reassess (do not assume they persist): first-round ASR 75.4% Cora and 99.9% PubMed; unsupported Reddit Seed-43 "community overlap" causality; attacker topology anomaly previously constant at 0.8483 and benign drift zero; PubMed +1.30 percentage-point clean accuracy change; 4.76% vs "<=4.7%" attacker share; nonreproducing paired Delta Clean Acc SD; fixed clean reference graph assumptions; figure labeling/caption inconsistencies. Mark each RESOLVED / STILL PRESENT / NO LONGER APPLICABLE / NOT VERIFIABLE using current raw results.
12. **Research honesty**: Separate (a) what implementation demonstrably does, (b) what experiments actually show, (c) mechanistic interpretations without isolation, and (d) limitations/new experiments needed. Flag every strong new claim with no measurement.

## Phase D: Validated changes and Git commits
Only after the read-only audit:
1. Fix small, clearly demonstrated defects that do not silently change experimental meaning (e.g. broken metadata, wrong plot label, run-manifest mismatch, documentation, deterministic configuration export, robust table export, straightforward verified bug with regression tests). For algorithm-changing or result-changing fixes, report them as blocking scientific decisions instead of silently changing the method or numbers. If such a fix is explicitly justified and made, mark all earlier model results potentially STALE until revalidated.
2. Add/update lightweight regression tests for each safe code correction and run them. Never forge test success.
3. Make **separate focused commits** (as relevant), for example:
   - `fix: correct verified ETD-FGL implementation or export bug`
   - `test: guard train-test split and experiment provenance`
   - `docs: document current ETD-FGL architecture and assumptions`
   - `results: align verified metric exports and figure sources`
   Only commit items actually changed; do not create empty ceremonial commits. Do not mix unrelated pre-existing changes into the commits. Do not alter original raw run files or artificially improve metrics.
4. Record EVERY new commit SHA, subject, exact changed paths, relevant checks and whether it invalidates any existing experiment. Do not push to a remote or rewrite history. Finish with `git status --short` and clearly state any remaining uncommitted files.

## Phase E: New manuscript-ready evidence package
Produce `ETD_FGL_NEW_CODE_HANDOFF/` containing the files below. Use detailed but efficient technical English. Keep the archive compact (ideally under 15 MB). Exclude datasets, checkpoints/model weights, virtual environments, caches, secrets, large logs, duplicate figures and the full repo.

- `00_START_HERE.md`: executive verdict; method identity; formal reviewer letter found/missing; which outputs are trustworthy; key results and limitations; audit branch/HEAD/commits; prioritized next steps. Include a 250-400-word precise executive summary.
- `01_FORMAL_REVIEW_COMPLIANCE.md` and `01_FORMAL_REVIEW_COMPLIANCE.csv`: exact source comments if present, requirement-by-requirement matrix; clearly indicate missing formal letter when applicable.
- `02_CURRENT_METHOD_CODEBOOK.md`: executable architecture, full algorithm and pseudocode, server-client data flow, threat model, key equations mapped to source file and lines, input/output schema, ablation definitions, what has substantively changed since the old paper.
- `03_CODE_CHANGELOG_AND_GIT.md`: known pre-/post-rewrite code comparison, added/deleted/replaced features, commit trail, tests, unexplained provenance and version hashes. If the previous code is unavailable, state that historical diff cannot be reconstructed.
- `04_EXPERIMENT_PROTOCOL.md`: exact datasets, partitioning, preprocessing, attacker setup, training evaluation protocol, seeds, configs, software/hardware, checkpoints, evaluation units, and reproducibility commands that DO NOT need to be executed by ChatGPT.
- `05_RESULTS/metrics_long.csv`: one row per dataset/method/seed/run with all measured final metrics; fields describing units and provenance. Add `round_metrics.csv`, `ablation_metrics.csv`, `paired_differences.csv`, and `provenance.csv` only where source evidence exists. Do not invent missing observations. Include `05_RESULTS/RESULTS_INTERPRETATION.md` specifying positive and negative findings, all calculation checks, sample SD and unsupported tests.
- `06_FIGURES/`: only camera-ready figures that map to current verified raw outputs. Keep source `.svg`/`.pdf` and readable `.png` where available, sensible naming and plot-generation scripts if small. Figure 1 must represent the NEW ACTUAL architecture; never reuse the old wrong labels or misleading claims. Prefer marked `NOT_READY` over a polished but scientifically false figure. Add `FIGURE_MANIFEST.csv` with slot, filename, script, input file/run, SHA, panels, units, main finding, exact proposed caption, and VERIFIED/STALE/MISSING status.
- `07_FULL_MANUSCRIPT_REWRITE_BLUEPRINT.md`: a SECTION-BY-SECTION plan for a new English academic manuscript (title options if method identity changed; abstract; introduction; related work; threat model; proposed method; algorithms and math; experimental setup; results and ablation; discussion; threats to validity; conclusion; code/data availability). For each section, list precise code/results evidence and claims to KEEP, REPLACE, DELETE, ADD. Include table and figure placement plan, but do NOT draft the full manuscript yet.
- `08_OPEN_ISSUES_AND_NEW_EXPERIMENTS.md`: blocking errors, unsupported claims, required reruns, missing baselines, fairness constraints, leakage concerns, unresolved reviewer requirements, missing measurements and a PRIORITIZED minimal experiment plan. Clearly separate mandatory from optional and distinguish already collected evidence from proposed future experiments.
- `09_GIT_COMMITS_AND_TESTS.md`: initial/final Git status; new commit SHAs/messages; test commands and results; changes not committed; which outputs must be regenerated if code changed.
- `10_CLAIM_TO_EVIDENCE_INDEX.csv`: one row per manuscript-relevant claim, with claim ID, statement, classification (CODE FACT / EMPIRICAL RESULT / INTERPRETATION / UNSUPPORTED), code path:line, raw result path and run/seed, output table/figure, confidence/reproducibility status. Include old claims explicitly rejected by new evidence.

Add `README.md` explaining how ChatGPT should use the files. Create `ETD_FGL_NEW_CODE_HANDOFF.zip` containing that directory. Validate archive integrity, ensure CSVs are parseable and no required source path is missing. Include a concise file inventory and archive size. If some figures require expensive runs or missing raw evidence, flag them; do not generate them by imagination.

## Required final console response
Report succinctly:
1. `FORMAL REVIEW COMPLIANCE: [VERIFIED/PARTIAL/FAILED/CANNOT DETERMINE - no authentic reviewer letter]` and why;
2. `CURRENT CODE SCIENTIFIC AUDIT: [PASS WITH LIMITATIONS / BLOCKED / FAIL]`, key evidence and important open risks;
3. Which old manuscript claims are obsolete and must be rewritten;
4. Git branch, initial/final SHA, each new commit SHA, test results, and uncommitted items;
5. Absolute path and size of the new ZIP, plus the main `00_START_HERE.md`;
6. Counts of verified/obsolete/missing figures and results;
7. A 10-15 sentence copy-ready summary to hand to ChatGPT as context.

**Priority order: scientific correctness > evidence provenance > faithful revised-code description > manuscript readiness > brevity.** Do the audit first. Never claim that code is compliant with a revision that has not been provided or verified.
