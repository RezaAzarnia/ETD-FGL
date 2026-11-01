# Publication figure manifest

Generator: `tools/publication_figures/make_publication_figures.py` (committed in `33472ff`).
Reproduce: `python -I tools/publication_figures/make_publication_figures.py figures/publication/tables figures/publication`
Regenerate the CSV inputs from raw runs: `python -I tools/raw_recompute/recompute_tables_from_raw.py . <dir>` (inputs here are copies of its outputs, 80a3210-era raw runs).
Tests: `test_publication_figures.py` (plotted arrays equal CSV values; recorded in `plotted_data.json`). SD = sample SD, ddof=1, n=3. No axis values, markers or error bars were altered for appearance. All PDFs: single page, Type-42 fonts embedded (`pdffonts`), 7.2 in wide (double column) unless noted.

| Fig | File | Input CSV (figures/publication/tables) | Selection / aggregation | Axis limits | Status |
|---|---|---|---|---|---|
| 1 | `Fig1_etdfgl_architecture_workflow.pdf` | none (schematic) | box-to-code map below | – | camera-ready (schematic; minor empty box space) |
| 2 | `Fig2_overall_baselines.pdf` | R02 | 8 methods x 3 datasets, seed 42, single run, no error bars | y 0-100 | camera-ready |
| S2 | `supplementary/FigS2_accuracy_asr_scatter.pdf` (was Fig 3; demoted to supplementary in design v3) | R02, R03a | seed-42 open markers (8 methods); 3-seed mean ± SD (ddof=1) filled for Attacked FedAvg and ETD-FGL; per-dataset panels | x auto per dataset, y -6..105 | camera-ready (dense cluster near Cora/Reddit corner; markers overlap by data, not by layout) |
| 4 | `Fig4_multiseed_robustness.pdf` | R03a | per-seed dots (labels 42/43/44), bar = mean, whisker = SD; Reddit seed 43 = 34.82 % annotated without cause | acc 0-100, ASR 0-105 | camera-ready |
| 5 | `Fig5_learning_dynamics_rounds.pdf` | R07 | seed 42, all 50 rounds, unsmoothed; Clean/Attacked FedAvg, FedTGE*, ETD-FGL | acc auto, ASR -3..103 | camera-ready with caveat: dense; ETD-FGL ASR 75.4 % / 99.9 % at round 1 (Cora/PubMed) annotated |
| 6 | `Fig6_controlled_ablation.pdf` | R05a, R06a | fixed-coefficient variants, per-seed markers, grey seed-pairing lines, paired Δ ASR | auto | camera-ready |
| 7 | `Fig7_attacker_weight_dynamics.pdf` | R08 | seed 42 raw per-round w0; moving average (5 rounds, centred) only for the noisy no-topology trace and labelled "visual aid only"; 20 % reference | y 0-27 | camera-ready |
| S | `supplementary/FigS1_runtime_exploratory.pdf` | R02, R11 | single-run wall-clock; same-method runs across suites | log y / auto | **EXPLORATORY ONLY** - not evidence of overhead/speed; hardware unrecorded |

Previews: `previews/*.png` (300 dpi). Plotted data dump: `plotted_data.json`.

## Fig. 1 box-to-code correspondence
| Box | Code |
|---|---|
| Clients 1-4 / Client 0 | `multidata_suite/core.py:run_method` local loop; `standard_local_train`; poisoning `attack.py:inject_clique_trigger` (victims from train mask, label -> target, K3) |
| Topology evidence (once) | `defenses.py:_graph_descriptor`, `ETDFGLAggregator.__init__` (clean and current graphs of all 5 clients; population-std scale; drift) |
| Update evidence (per round) | `ETDFGLAggregator.__call__` (`_flatten_delta`, coordinate-wise median, L2 distance) |
| Robust map | `defenses.py:_robust_positive` |
| Fusion and trust | `ETDFGLAggregator.__call__` (9/13, 4/13, `clip(exp(-3R),0.02,1)`, `n_i*T_i`) |
| Server | `_weighted_average`; `core.py:evaluate`, checkpoint on `validation_accuracy` |
| Simulation assumption note | `run_real_dataset_pipeline.py` passes `clean_graphs_cpu` to the aggregator |


## Design v3 (formal style)
Generator `tools/publication_figures/make_publication_figures.py`; no question subtitles, slogans or in-figure caveat prose (captions: `FIGURE_CAPTIONS.md`); Fig 1 redrawn (all five clients feed both channels, K3 attached to victim node, static vs per-round channels, clean references marked as simulation assumption); desirable-region shading removed; Fig 5 reduced to Clean/Attacked FedAvg and ETD-FGL (all 50 rounds, round-1 values annotated); Fig 7 legend now carries the uniform share and moving-average notes. All PDFs: Type-42 fonts embedded, no Type-3, 7.2 in design width. Source CSVs unchanged.
