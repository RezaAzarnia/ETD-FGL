# Git changes and tests

* Initial state: branch `audit-fix-verification`, HEAD `80a321027b26853eee1c2c4f415e1ec9c1f4961c` (tag `paper-results-v1.0.0`); tracked tree clean; untracked: `build_figure_revision_v2/v3/v4.py`, `paper_artifacts/ETDFGL_Figure_Revision_*`, earlier handoff folder/zip, instruction `.md` files (left untouched and uncommitted).
* Revision branch (created from 80a3210; no push, no history rewrite): `revision-audit-2026-11`.

| Commit | Subject | Paths | Invalidates results? |
|---|---|---|---|
| `28340f89448a654dcff491c2e15a8a11b9a2fc10` | fix(provenance): record runtime environment and timing scope in run summaries | `multidata_suite/core.py`, `test_audit_regressions.py` | No (additive keys; no effect on training or metrics) |
| `7a1cc1fc11144a8824b52e3061a3716791a2fbc4` | fix(baselines): persist DMGNN-FL edge-removal counts and label implementation | `multidata_suite/defenses.py`, `run_real_dataset_pipeline.py`, `test_audit_regressions.py` | No (pruning logic unchanged; existing runs remain without counts) |
| `3084163031c9e535eedf044ab555c9e26fbd45d7` | results: add read-only raw-output recomputation and figure rendering tools | `tools/raw_recompute/*` | No |

No documentation commit was made (package delivered as an untracked folder + zip); no empty commits.

## Tests
* `pytest -q` (CPU, `.venv`, Python 3.11.9, torch 2.14.1+cpu, PyG 2.8.1): **80 passed** before changes (17.4 s); **82 passed** after (18.2 s). Added: `test_run_method_records_runtime_environment_and_timing_scope` (2-round synthetic `run_method`; checks new keys on disk and compatibility with `validate_existing_experiment`) and `test_summarize_purification_diagnostics_persists_removed_edge_counts`.
* `py_compile` of changed modules: OK.
* Cross-checks (not unit tests): recomputed multi-seed table vs committed `multiseed_summary.csv` (max diff 4.8·10⁻⁵); logged R and T equal the formula applied to logged A_topo, A_upd (max diff 2·10⁻¹⁶ over 9 multi-seed runs); weights sum to 1.
* Software tests demonstrate code behaviour, **not** scientific validity.

## Results needing reruns
None are invalidated by these commits. Reruns are needed only to *support new claims*: controlled timing with device logged, DMGNN pruning counts, ≥10 seeds and 3-seed Clean FedAvg, non-IID, M≥2, reference-free variant, label-blind partition.

## Uncommitted
Only the untracked files listed above plus `ETD_FGL_NEW_CODE_HANDOFF/` and its zip.
