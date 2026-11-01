# Figure QA report

Method: regenerated from committed CSVs (`TABLES/`, commit `33472ff`); every PDF checked with `pdfinfo`/`pdffonts` (1 page, all fonts embedded, 24–43 KB); every 300-dpi PNG preview viewed after the final render (iterating until clipped text/overlaps were removed); automated tests compare plotted arrays with CSV values. A visual pass does not make a figure scientifically stronger — captions must keep the stated caveats.

| Fig | Size (pt) | Issues in old/previous version → fix | Residual issues | QA |
|---|---|---|---|---|
| 1 Architecture | 416×231 | cramped robust-map box, overflowing equations, false labels (≥85 %, ≤4.7 %, ASR<5 %, "test node poisoning", "pairwise"), reference box with arrows implying data flow → redrawn: reference graphs shown as SIMULATION ASSUMPTION inside the topology box; all 5 clients feed topology and update evidence; static (once) vs per-round; robust map; fusion/trust; sample-weighted aggregation; clean-VALIDATION checkpoint; broadcast arrow; poisoning on TRAIN nodes | text is 5.2–5.7 pt at 7.2 in width (readable at full width, small in one column); some empty box area | PASS (double-column only) |
| 2 Baselines | 516×273 | legend crowding, no single-run notice → 8-method legend with hatches, `*` for adapted baselines, note "seed 42, one run, no uncertainty" | none | PASS |
| 3 Accuracy vs ASR | 518×280 | overlapping labels, pooled axes → per-dataset panels, open seed-42 vs filled 3-seed mean±SD markers, legend below, "desirable: lower right", no Pareto line | Cora/Reddit points cluster by data (ETD-FGL and Clean FedAvg nearly coincide) | PASS with note |
| 4 Multi-seed | 516×340 | → per-seed dots labelled 42/43/44, mean bars, sample-SD whiskers, Reddit seed 43 annotated "cause not established", no significance marks | none | PASS |
| 5 Dynamics | 517×371 | → all 50 rounds unsmoothed, line styles + markers, round-1 ASR annotated (75.4 %, 99.9 %, 0.4 %), caption states best-validation checkpoint ≠ round 50 | dense; PubMed annotation arrow crosses curves | PASS with caveat |
| 6 Controlled ablation | 512×382 | tick-label overlap → fixed (two-line labels "9/13 + 4/13", "9/13 + 0", "0 + 4/13"); per-seed markers, seed-pairing lines, paired Δ in pp, "fixed-coefficient (not renormalized)", n=3 and "no test" | none | PASS |
| 7 Attacker weight | 516×253 | noisy no-topology trace → raw trace kept (thin) + labelled 5-round moving average, uniform 20 % line, y 0–27, no "≤4.7 %" | – | PASS |
| S Runtime | 580×250 | legend overlapped bars; claim risk → legend below, banner "SUPPLEMENTARY / EXPLORATORY – not evidence of overhead or speed advantage", panel (b) shows the same method's run-to-run spread | **not promotable** to a main figure | EXPLORATORY ONLY |

**Camera-ready for main text:** Figs 1, 2, 3, 4, 6, 7; Fig 5 with caveat (dense). **Caveated/exploratory:** Fig S. Not covered by any figure (no data): graded-drift sensitivity, non-IID, M≥2, trigger-size sweeps.

Traceability (all figures): input file, selection, aggregation, SD convention, axis limits, script SHA `33472ff`, reproduction command → `FIGURE_MANIFEST.md`. Plotted arrays → `plotted_data.json` (in repo `figures/publication/`). Tests: `SCRIPTS/test_publication_figures.py`.
