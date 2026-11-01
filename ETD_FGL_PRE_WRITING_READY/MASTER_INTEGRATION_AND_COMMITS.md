# Master integration and commits

**No push occurred.** `origin/master` was not touched and still equals `953e250578ee028882c1e6edc7a68edaa8ef35f9` (verified with `git ls-remote origin` before integration; `git status` reports local `master` ahead of origin).

| Step | Result |
|---|---|
| Pre-integration state | branch `revision-audit-2026-11` @ `3084163`; `master` = `origin/master` = `953e250`; working tree: only untracked user files |
| Ancestry check | `git merge-base --is-ancestor master revision-audit-2026-11` → **true** (master is an ancestor; no divergence) |
| Backup ref (non-destructive) | `backup/master-pre-integration-953e250` → `953e250578ee028882c1e6edc7a68edaa8ef35f9` |
| Integration | `git switch master` + `git merge --ff-only revision-audit-2026-11` → **fast-forward succeeded**; master @ `3084163031c9e535eedf044ab555c9e26fbd45d7`; three audited commits are in master history |
| Untracked files | untouched (build_figure_revision_v2/v3/v4.py, paper_artifacts/, earlier handoff folders and zips, instruction files) |
| Figure work | committed directly on `master` (no extra branch kept; an accidental empty branch created at the same SHA was deleted with `git branch -d`, no commits lost) |
| Checked-out branch at end | `master` |

## Commits on master since `953e250` (oldest → newest)
| SHA | Subject | Paths | Invalidates results? |
|---|---|---|---|
| `80a321027b26853eee1c2c4f415e1ec9c1f4961c` | research: finalize ETD-FGL results… (pre-existing) | results code, tables | – |
| `28340f89448a654dcff491c2e15a8a11b9a2fc10` | fix(provenance): record runtime environment and timing scope | `multidata_suite/core.py`, `test_audit_regressions.py` | No |
| `7a1cc1fc11144a8824b52e3061a3716791a2fbc4` | fix(baselines): persist DMGNN-FL edge-removal counts and label implementation | `multidata_suite/defenses.py`, `run_real_dataset_pipeline.py`, `test_audit_regressions.py` | No |
| `3084163031c9e535eedf044ab555c9e26fbd45d7` | results: add read-only raw-output recomputation and figure rendering tools | `tools/raw_recompute/*` | No |
| `33472ff44ec8111064fbbe0c25a5514002c644f6` | figures: add verified CSV inputs, publication figure generator and fidelity tests | `figures/publication/tables/*.csv`, `tools/publication_figures/make_publication_figures.py`, `test_publication_figures.py` | No |
| `a1ac03b6c295a72d326249e727d8b501a02f8cd6` | figures: regenerate and validate publication plots | `figures/publication/*.pdf`, `previews/`, `supplementary/`, `plotted_data.json`, `FIGURE_MANIFEST.md` | No |

Final master HEAD: **`a1ac03b6c295a72d326249e727d8b501a02f8cd6`**. The branch `revision-audit-2026-11` still points to `3084163` (kept); `audit-fix-verification` remains at `80a3210`.

## Tests
`pytest -q`: 80 passed before any change; 82 after the provenance/baseline fixes; **88 passed** after the figure tests (CPU, Python 3.11.9, torch 2.14.1+cpu). Figure checks: `pdfinfo`/`pdffonts` on all 8 PDFs (1 page, fonts embedded), every figure PNG inspected visually.

## Uncommitted
Untracked only: instruction `.md` files, `ETD_FGL_PAPER_HANDOFF*`, `ETD_FGL_NEW_CODE_HANDOFF*`, `ETD_FGL_PRE_WRITING_READY*`, `build_figure_revision_v2/v3/v4.py`, `paper_artifacts/ETDFGL_Figure_Revision_*`.
