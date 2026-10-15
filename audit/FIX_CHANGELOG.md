# ETD-FGL Fix Changelog

This document provides a line-by-line and component-level record of all software repairs applied during the scientific code audit.

---

## 1. Aggregator Dispatch & Exception Safety (`multidata_suite/core.py`)
- **Files Modified:** `multidata_suite/core.py`
- **Original Behavior:** Aggregator execution wrapped invocation with `local_diags` in a broad `try...except TypeError:` block. If an aggregator raised an internal `TypeError`, it was caught and re-invoked without diagnostics, concealing runtime defects.
- **Corrected Behavior:** Replaced exception handling with `invoke_aggregator()` using explicit `inspect.signature` capability detection. If the aggregator parameter list includes `local_diags` or `**kwargs`, diagnostics are passed; otherwise they are omitted. Internal errors propagate immediately with full traceback. Return values are verified to be `(state_dict, dict)` tuples.
- **Scientific Impact:** None. Improves pipeline robustness and defect transparency.
- **Rerun Required:** No.

---

## 2. FedTGE Energy Diagnostics Validation (`multidata_suite/fedtge.py`)
- **Files Modified:** `multidata_suite/fedtge.py`
- **Original Behavior:** If client diagnostics were missing, malformed, or mismatched in length, `FedTGEAggregator` silently generated substitute all-ones vectors (`np.ones(10)`), fabricating input data.
- **Corrected Behavior:** Removed all synthetic fallback generation. Strict validation checks that `local_diags` is non-None, length matches `num_clients`, every dict contains `'energy_vector'`, arrays are 1D and non-empty, and all values are finite (no NaN or Inf). Raises explicit `ValueError` if invariants are violated.
- **Scientific Impact:** Eliminates risk of fabricated inputs influencing benchmark comparisons.
- **Rerun Required:** Only if previous FedTGE runs triggered the fallback (verified not triggered in standard completed runs).

---

## 3. FedTGE Edge Augmentation Semantics (`multidata_suite/fedtge.py`)
- **Files Modified:** `multidata_suite/fedtge.py`
- **Original Behavior:** `_aug_random_edge()` accepted `perturb_percent=0.2` but ignored it in favor of an average-degree heuristic `avg_degree = int(total_edges / num_nodes)`.
- **Corrected Behavior:** Documented provenance from `ZitongShi/fedTGE`. Retained the default official average-degree heuristic (`mode="official_degree"`) to preserve exact comparability with the published baseline, while providing explicit percentage scaling when `mode="percentage"` or when a non-default `perturb_percent` is passed.
- **Scientific Impact:** Clarifies code documentation while maintaining exact numerical consistency with official FedTGE baselines.
- **Rerun Required:** No (default behavior preserved).

---

## 4. FedTGE Architecture Metadata Alignment (`run_real_dataset_pipeline.py`, `run_extended_experiments.py`)
- **Files Modified:** `run_real_dataset_pipeline.py`, `run_extended_experiments.py`
- **Original Behavior:** Metadata dictionary recorded a hardcoded hidden dimension of 16 for FedTGE, while the model instantiated at runtime used `config.hidden_channels` (32).
- **Corrected Behavior:** Updated metadata dictionaries to dynamically log `config.hidden_channels` (32) and formatted architecture strings as `f"FedTGEGCN({data.num_features} -> {config.hidden_channels} -> {dataset.num_classes})"`.
- **Scientific Impact:** Corrects descriptive provenance; runtime model architecture was already 32 channels.
- **Rerun Required:** No.

---

## 5. Experiment Provenance & Cache Safety (`multidata_suite/core.py`, `multidata_suite/data.py`)
- **Files Modified:** `multidata_suite/core.py`, `multidata_suite/data.py`, `run_real_dataset_pipeline.py`, `run_extended_experiments.py`
- **Original Behavior:** The pipeline checked only `final_summary.json.exists()` before skipping an experiment. Partial/corrupted zero-byte files from crashed runs caused silent skipping. Partition caching did not verify node count coverage.
- **Corrected Behavior:**
  - Added atomic JSON saving via `_atomic_save_json` (writes to `.tmp` before renaming).
  - Added `validate_existing_experiment()`: validates file existence, non-zero file sizes, JSON parsing, required top-level keys (`dataset`, `method`, `config`, `final_metrics`, `best_round`), and exact match on requested hyperparameters (`seed`, `rounds`, `local_epochs`, `hidden_channels`, `learning_rate`, `poison_rate`, `trigger_size`, `num_clients`).
  - Added cache validation in `load_or_create_partition()`: validates cached partition client count, seed, strategy, Dirichlet alpha, and node sum matching `data.num_nodes`.
- **Scientific Impact:** Prevents silent corruption or cross-condition pollution during multi-seed and sensitivity sweeps.
- **Rerun Required:** No.

---

## 6. Figure Scripts Baseline Consistency (`multidata_suite/config.py`, `build_real_comparisons_and_figures.py`, `build_section4_extra_figures.py`)
- **Files Modified:** `multidata_suite/config.py`, `build_real_comparisons_and_figures.py`, `build_section4_extra_figures.py`
- **Original Behavior:** `BENCHMARK_METHODS` was not centrally defined. FedTGE was omitted from comparison scripts, causing plotting errors or absent baseline bars.
- **Corrected Behavior:** Established canonical `BENCHMARK_METHODS` registry with all 8 methods. Added FedTGE markers, colors, and hatches (`"xxx"`). Implemented dynamic filtering so missing optional runs do not crash figure generation.
- **Scientific Impact:** Ensures complete, fair 8-method visual comparisons in journal figures.
- **Rerun Required:** Figure generation scripts should be re-executed (`build_real_comparisons_and_figures.py`).

---

## 7. Decoupled Homophily in Verification Scripts (`test_homophily_leakage_fix.py`, `run_stage1_verification.py`)
- **Files Modified:** `test_homophily_leakage_fix.py`, `run_stage1_verification.py`
- **Original Behavior:** Verification scripts accessed `ref_desc[5]` and historical homophily dict keys on the production descriptor, raising index and key errors because the production descriptor is 5D.
- **Corrected Behavior:** Updated scripts to compute homophily diagnostics exclusively via `compute_homophily_diagnostics(graph)`. Assertions verify that `_graph_descriptor()` is strictly 5-dimensional and label-free.
- **Scientific Impact:** Preserves label-free security in production ETD-FGL while maintaining historical diagnostic verification.
- **Rerun Required:** No.

---

## 8. Ablation Documentation Alignment (`docs/EXTENDED_EXPERIMENTS.md`, `README.md`)
- **Files Modified:** `docs/EXTENDED_EXPERIMENTS.md`, `README.md`
- **Original Behavior:** Ablation documentation listed Full ETD-FGL as `0.45 / 0.35 / 0.20`, conflicting with production code (`9/13 / 0.0 / 4/13`).
- **Corrected Behavior:** Aligned documentation to clearly delineate Production ETD-FGL ($\alpha_{\text{topo}}=9/13, \alpha_{\text{upd}}=4/13, \alpha_{\text{exp}}=0$) from the Historical Three-Channel Variant ($0.45, 0.35, 0.20$). Clarified the roles of topology-only, update-only, and unweighted aggregation variants.
- **Scientific Impact:** Eliminates reviewer confusion between production and historical configurations.
- **Rerun Required:** No.

---

## 9. Continuous Integration & Unit Testing (`pytest.ini`, `.github/workflows/syntax-check.yml`, `test_audit_regressions.py`)
- **Files Added / Modified:** `pytest.ini`, `.github/workflows/syntax-check.yml`, `test_audit_regressions.py`
- **Original Behavior:** CI only performed syntax compilation.
- **Corrected Behavior:** Added `test_audit_regressions.py` with 26 offline unit tests covering descriptor dimensions, label invariance, aggregator dispatch, FedTGE energy validation, augmentation determinism, architecture parameters, and provenance caching. Updated GitHub Actions workflow to run deterministic unit tests with CPU PyTorch on every push and PR.
- **Scientific Impact:** Provides continuous regression protection without requiring large dataset downloads in CI.
- **Rerun Required:** No.
