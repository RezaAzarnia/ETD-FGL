# ETD_FGL_PRE_WRITING_READY

Scientific foundation for writing the ETD-FGL paper section by section. **No manuscript text is included or edited.**

How ChatGPT should use this package
1. Read `PRE_WRITING_SCIENTIFIC_GATE.md` first: what is verified, what is open, which old claims are forbidden.
2. Read `CODE_TRUTH_UPDATE.md`; the full method description is in `REFERENCE/` (code truth, equations/pseudocode, claims-evidence matrix with IDs C01-C38, results/statistics) — copied unchanged from the earlier handoff and still valid.
3. Use only numbers from `TABLES/` (every value was recomputed from raw runs; sample SD ddof=1, n=3 seeds 42–44) and only figures from `FIGURES/` (see `FIGURE_MANIFEST.md`, `FIGURE_QA_REPORT.md`). `FIGURES/SUPPLEMENTARY_EXPLORATORY/` must not support claims.
4. Never write: significance statements, seeds 45/46 results, GNNExplainer for DMGNN-FL, causal explanations of Reddit seed 43, runtime/overhead superiority, ≤4.7 % attacker share, ASR<5 % from round 1, "within 0.5 pp", privacy/secure-aggregation claims.
5. Formal referee compliance is NOT VERIFIABLE (no letter). Treat open items in `OPEN_SCIENTIFIC_ITEMS.md` as limitations unless the author runs the experiments.
6. `MASTER_INTEGRATION_AND_COMMITS.md` lists all commit SHAs (master HEAD `a1ac03b6c295a72d326249e727d8b501a02f8cd6`; nothing pushed).

Contents: `PRE_WRITING_SCIENTIFIC_GATE.md`, `MASTER_INTEGRATION_AND_COMMITS.md`, `FIGURE_QA_REPORT.md`, `FIGURE_MANIFEST.md`, `FIGURES/` (7 main PDFs, `previews/` 300-dpi PNGs, `SUPPLEMENTARY_EXPLORATORY/`), `TABLES/` (15 CSVs), `CODE_TRUTH_UPDATE.md`, `OPEN_SCIENTIFIC_ITEMS.md`, `REFERENCE/` (4 reference documents), `SCRIPTS/` (figure generator + fidelity test; reproduce with the repo commands in the manifest).
