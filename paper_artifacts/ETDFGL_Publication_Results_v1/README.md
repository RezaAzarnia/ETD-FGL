# ETD-FGL Publication Results Package (v1.0)

This directory contains the verified, publication-ready research package for the **Evidence-based Topological Defense for Federated Graph Learning (ETD-FGL)** project.

## Directory Structure

```
paper_artifacts/ETDFGL_Publication_Results_v1/
├── README.md                                  # This documentation file
├── RESULT_MANIFEST.json                       # Machine-readable master index and metadata
├── source_inventory.csv                       # Provenance inventory of all 132 validated experimental runs
├── figures/                                   # High-resolution figures (PDF, SVG, 600 DPI PNG)
│   ├── main/                                  # 6 Main article figures (Figs 1–6)
│   └── supplementary/                         # 5 Supplementary figures (Figs S1–S5)
├── tables/                                    # Publication tables
│   ├── csv/                                   # Tables 1–9 in CSV format
│   ├── latex/                                 # Tables 1–9 in publication-ready LaTeX (booktabs)
│   ├── markdown/                              # Tables 1–9 in Markdown format
│   └── tables_manifest.json                   # Metadata registry of all tables
├── consolidated_data/                         # Machine-readable verified datasets (Single Source of Truth)
│   ├── consolidated_experiments.csv           # Complete dataset of all 132 runs
│   ├── baseline_seed42.csv                    # Seed 42 baseline comparison runs
│   ├── multiseed_summary.csv                  # Multi-seed mean ± sample standard deviation
│   ├── standard_ablation_summary.csv          # Standard ablation summary
│   ├── controlled_ablation_summary.csv        # Controlled ablation summary (fixed coefficients)
│   └── paired_differences.csv                 # Paired within-seed component contribution statistics
├── manuscript_sections/                       # Standalone LaTeX sections ready for paper integration
│   ├── 01_experimental_setup.tex
│   ├── 02_datasets_and_preprocessing.tex
│   ├── 03_baselines.tex
│   ├── 04_implementation_details.tex
│   ├── 05_evaluation_metrics.tex
│   ├── 06_main_results.tex
│   ├── 07_multiseed_robustness.tex
│   ├── 08_standard_ablation.tex
│   ├── 09_controlled_ablation.tex
│   ├── 10_defense_mechanism.tex
│   ├── 11_computational_efficiency.tex
│   ├── 12_limitations.tex
│   ├── 13_summary_of_findings.tex
│   └── FIGURE_AND_TABLE_CAPTIONS.md           # Complete figure and table captions
└── scientific_review/                         # Exhaustive scientific critical review
    └── SCIENTIFIC_REVIEW.md                   # In-depth review of Reddit Seed 43, ablation, DMGNN-FL, etc.
```

## Reproduction Commands

All figures, tables, and consolidated datasets can be reproducibly re-extracted from original experimental outputs using:

```bash
# 1. Consolidate and validate original outputs
python extract_and_consolidate_results.py

# 2. Generate publication figures (PDF, SVG, PNG)
python generate_publication_figures.py

# 3. Build publication tables (CSV, LaTeX, Markdown)
python build_publication_tables.py

# 4. Generate manuscript sections and scientific review
python build_manuscript_sections.py
```

## Experimental Portfolio Summary

- **Benchmark Datasets**: Cora (2,708 nodes), PubMed (19,717 nodes), Reddit (8,000 nodes sampled).
- **Evaluated Methods**: Clean FedAvg, Attacked FedAvg, PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE, ETD-FGL.
- **Seeds Evaluated**: 42, 43, 44.
- **Total Validated Runs**: 132 runs across 4 suites (0 manifest SHA256 mismatches).
