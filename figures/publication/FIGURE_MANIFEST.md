# Publication figure manifest (final)

Generator: `tools/publication_figures/make_publication_figures.py` (design v3). Reproduce: `python -I tools/publication_figures/make_publication_figures.py figures/publication/tables figures/publication`. CSV inputs in `figures/publication/tables/` are copies of `tools/raw_recompute` output (raw runs produced under commit 80a3210) and were verified equal to a fresh raw recomputation. Captions and limitations: `FIGURE_CAPTIONS.md`.

Final verification (2026-11-01): plotted arrays (`plotted_data.json`, 141 series) identical on regeneration; committed PDFs and PNGs identical on regeneration (PNG pixel-equal, PDF raster difference 0); Fig 2/4 values equal CSVs; sample SD ddof = 1; all PDFs one page, fonts embedded (Type 42), no Type 3 fonts; all PNGs viewed, no clipping; figure-fidelity tests 6/6, full suite 88 passed.

| Fig | PDF | PNG preview (300 dpi) | Size | Input CSV | Status | PDF sha256 (16) | PNG sha256 (16) |
|---|---|---|---|---|---|---|---|
| Fig S1 | `supplementary/FigS1_runtime_exploratory.pdf` | `previews/FigS1_runtime_exploratory.png` | 7.18 x 3.24 in | R02, R11 | EXPLORATORY ONLY - no overhead/speed claim | 74a9ab7d9149b35b | 3bf57e03d5df2c6b |
| Fig S2 | `supplementary/FigS2_accuracy_asr_scatter.pdf` | `previews/FigS2_accuracy_asr_scatter.png` | 7.28 x 2.99 in | R02, R03a | Supplementary only (largely redundant with Figs 2, 4) | d6e3283097286290 | d5baf738b01106ec |
| Fig 1 | `Fig1_etdfgl_architecture_workflow.pdf` | `previews/Fig1_etdfgl_architecture_workflow.png` | 7.40 x 4.50 in | none (schematic; box-to-code map below) | Camera-ready (double column) | 699b2b8f596940ad | 2ddeb7725b403e77 |
| Fig 2 | `Fig2_overall_baselines.pdf` | `previews/Fig2_overall_baselines.png` | 7.88 x 4.72 in | R02 (seed 42, single runs) | Camera-ready | c290fcb5462f45bc | c1a24500868ad781 |
| Fig 4 | `Fig4_multiseed_robustness.pdf` | `previews/Fig4_multiseed_robustness.png` | 7.24 x 4.63 in | R03a (seeds 42-44) | Camera-ready | a2127862d7688564 | c32d70ebd804b97e |
| Fig 5 | `Fig5_learning_dynamics_rounds.pdf` | `previews/Fig5_learning_dynamics_rounds.png` | 7.33 x 4.73 in | R07 (seed 42, 50 rounds) | Camera-ready | e95c5c89de5ffcdd | 9fafb74e4be23e6d |
| Fig 6 | `Fig6_controlled_ablation.pdf` | `previews/Fig6_controlled_ablation.png` | 7.24 x 4.96 in | R05a, R06a (seeds 42-44) | Camera-ready | 84c30127ecb12d27 | b03e02cf617724c8 |
| Fig 7 | `Fig7_attacker_weight_dynamics.pdf` | `previews/Fig7_attacker_weight_dynamics.png` | 7.25 x 3.06 in | R08 (seed 42, 50 rounds) | Camera-ready | 6220c10f4fce7599 | 951be26cb3d1757f |

Note: Fig 2 exports 7.88 in wide because bold y-axis labels extend the tight bounding box; scale to the journal column width on inclusion.

Scientific limitations carried by these figures: Figs 2, 5, 7 are seed 42 single runs; Figs 4, 6 use n = 3 seeds without any significance test; baselines are untuned adapted implementations (*); reference graphs are a simulation assumption; Reddit seed 43 (ASR 34.82 %) is unexplained; ETD-FGL round-1 ASR is 75.4 % (Cora) and 99.9 % (PubMed); final metrics use the best clean-validation checkpoint.

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
