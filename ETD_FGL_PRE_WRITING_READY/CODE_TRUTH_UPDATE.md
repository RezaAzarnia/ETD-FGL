# Code-truth update (since `ETD_FGL_NEW_CODE_HANDOFF`)

The method, equations, protocol and stored results are unchanged. Read `ETD_FGL_NEW_CODE_HANDOFF/ETD_FGL_COMPLETE_CODE_TRUTH.md` and `EQUATIONS_AND_PSEUDOCODE.md` for the full description (still valid; line numbers cited there are at `3084163`, and `defenses.py`/`core.py` did not change afterwards).

Changes since then:
1. `master` now contains the three audited commits (fast-forward); figures and tests were added in `33472ff`, `a1ac03b`.
2. New run summaries (future runs only) additionally contain `runtime_environment` (device, torch/PyG/Python versions, GPU name if any) and `timing_scope`; DMGNN-FL metadata contains `purification.per_client[*].num_removed_edges` and the statement that it is a leave-one-edge-out heuristic. The 132 stored runs have neither.
3. Figure design: Fig 1 now follows the code (reference graphs = simulation assumption; all clients' current graphs and updates feed the two evidence channels; checkpoint selected on clean validation accuracy). Fig 8 (runtime) moved to a supplementary exploratory figure.
4. Additional measured facts used by the figures (all from raw logs): ETD-FGL round-1 ASR 75.4 % (Cora) / 99.9 % (PubMed) / 0.4 % (Reddit) (seed 42); Fixed-No-Topology attacker share peaks at 24.3–25.0 %; seed-43 Reddit ASR 37.8 % at round 50 vs 34.82 % at the selected round.
Not changed: any algorithm, hyperparameter, seed, raw output, or metric.
