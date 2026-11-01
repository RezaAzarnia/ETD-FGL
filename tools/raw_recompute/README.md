# Raw-output recomputation tools (read-only)

Recompute every manuscript table/figure input directly from `outputs/**/final_summary.json` and
`training_history.csv`, independent of `extract_and_consolidate_results.py`.

    python -I tools/raw_recompute/recompute_tables_from_raw.py . <out_tables_dir>
    python -I tools/raw_recompute/render_figures_from_tables.py <out_tables_dir> <out_figures_dir>

`render_figures_from_tables.py` expects `<out_figures_dir>/EXTRA/` to exist. Sample SD uses ddof=1.
Validated (2026-11): multi-seed means/SDs agree with `consolidated_data/multiseed_summary.csv`
to <5e-5 (float32 rounding). No training is performed; no outputs are modified.
