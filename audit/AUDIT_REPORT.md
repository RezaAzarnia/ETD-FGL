# ETD-FGL Scientific Code Audit Report

**Repository:** [https://github.com/RezaAzarnia/ETD-FGL](https://github.com/RezaAzarnia/ETD-FGL)
**Project:** ETD-FGL — Federated Graph Learning Against Backdoor Attacks Using Topology-aware Defense
**Audited Commit / Working Branch:** `953e250578ee028882c1e6edc7a68edaa8ef35f9` (`audit-fix-verification`)
**Auditor:** Senior Machine Learning Research Engineer & Scientific Code Auditor
**Date:** October 2026
**Audit Objective:** Rigorous code audit, software defect verification and minimal repair, mathematical invariance verification, and experimental reproducibility readiness for journal-level review.

---

## 1. Executive Summary

A comprehensive source-code and mathematical audit of the ETD-FGL repository was performed. The scope was strictly isolated to ETD-FGL (Cora, PubMed, and sampled Reddit datasets for federated graph learning against structural backdoor attacks). No code, datasets, or concepts from external IoT intrusion detection or blockchain oracle projects were introduced.

All nine confirmed software defects (Issues 1–9) were independently reproduced, repaired with minimal and surgical modifications, and validated using an automated test suite comprising 55 test cases across 5 test suites (`test_audit_regressions.py`, `test_homophily_leakage_fix.py`, `test_stage2_alignment.py`, `test_stage4_3_fedtge_verification.py`, and `test_final_5d_descriptor.py`). All 55 tests pass cleanly.

---

## 2. Scope & Repository Architecture

### 2.1 Production vs Historical Method
- **Production ETD-FGL Defense**: The security-critical risk calculation uses a frozen, two-channel formulation combining label-free topology drift and round-wise model update anomalies:
  $$\mathcal{R}_i^{(t)} = \frac{9}{13} \mathcal{A}_i^{\text{topo}} + \frac{4}{13} \mathcal{A}_i^{\text{upd}, t}, \quad \text{with } \mathcal{A}_i^{\text{exp}} = 0$$
  Trust mapping: $\tau_i = \text{clip}\left(\exp(-3.0 \cdot \mathcal{R}_i^{(t)}), 0.02, 1.0\right)$.
- **Production Topology Descriptor**: Strictly 5-dimensional, label-free, and mask-invariant:
  1. Graph Density
  2. Mean Node Degree
  3. Normalized Degree Variance (Dispersion)
  4. Average Clustering Coefficient
  5. Triangles per Node
- **Historical Development Variants**:
  - The three-channel development variant ($\alpha_{\text{topo}}=0.45, \alpha_{\text{exp}}=0.35, \alpha_{\text{upd}}=0.20$) remains available in `ConfigurableETDFGLAggregator` solely for historical component ablation.
  - Node label homophily was historically evaluated as a diagnostic descriptor coordinate but was decoupled to `compute_homophily_diagnostics()` to eliminate label leakage.

---

## 3. Confirmed Software Defects, Root Cause Analysis & Fix Verification

| ID | Module / Function | Severity | Nature | Status |
|---|---|---|---|---|
| **Issue 1** | `test_homophily_leakage_fix.py`, `run_stage1_verification.py` | High | Test Crash / Outdated 6D Indexing | **FIXED & VERIFIED** |
| **Issue 2** | `multidata_suite/core.py::run_method` | High | Exception Swallowing / Broad `TypeError` | **FIXED & VERIFIED** |
| **Issue 3** | `multidata_suite/fedtge.py::FedTGEAggregator` | High | Silent Synthetic Data Injection (`np.ones`) | **FIXED & VERIFIED** |
| **Issue 4** | `multidata_suite/fedtge.py::_aug_random_edge` | Medium | Misleading Unused Parameter in Baseline | **FIXED & VERIFIED** |
| **Issue 5** | `run_real_dataset_pipeline.py`, `run_extended_experiments.py` | Low | Metadata Mismatch (Hidden Dim 16 vs 32) | **FIXED & VERIFIED** |
| **Issue 6** | `multidata_suite/core.py`, `multidata_suite/data.py` | High | Unsafe Experiment & Partition Reuse | **FIXED & VERIFIED** |
| **Issue 7** | `build_real_comparisons_and_figures.py`, `build_section4_extra_figures.py` | Medium | Missing Baseline in Figures / Inconsistent Registry | **FIXED & VERIFIED** |
| **Issue 8** | `docs/EXTENDED_EXPERIMENTS.md`, `README.md` | Medium | Documentation Contradiction (Weights) | **FIXED & VERIFIED** |
| **Issue 9** | `.github/workflows/syntax-check.yml` | Medium | Incomplete CI Workflow | **FIXED & VERIFIED** |

---

### Detailed Analysis of Repaired Defects

#### Issue 1: Obsolete Six-Dimensional Descriptor Tests
- **Symptom:** Tests and scripts expected `_graph_descriptor()` to return 6 coordinates including homophily, or accessed `ref_desc[5]`, causing `IndexError` or referencing nonexistent dict keys.
- **Root Cause:** When homophily was removed from the production descriptor to prevent label leakage, older verification scripts were not updated to use the dedicated diagnostic function.
- **Repair:**
  - Preserved the production 5D label-free descriptor (`_graph_descriptor()`) strictly intact.
  - Updated `test_homophily_leakage_fix.py` and `run_stage1_verification.py` to route homophily checks through `compute_homophily_diagnostics(graph)`.
  - Added regression tests verifying 5D dimensionality, label invariance, mask invariance, and degenerate graph stability (empty, isolated, single-node).

#### Issue 2: Broad `TypeError` Handling in Aggregation Dispatch
- **Symptom:** `run_method()` used a broad `try...except TypeError:` block when invoking aggregators with `local_diags`. If an aggregator encountered an internal `TypeError` (e.g., incorrect tensor operation or type mismatch), the error was silently caught and the aggregator was retried without diagnostics.
- **Root Cause:** Naive argument-signature compatibility checking via runtime exception catching.
- **Repair:**
  - Implemented `invoke_aggregator(aggregate_fn, ...)` in `multidata_suite/core.py`.
  - Uses `inspect.signature` capability detection to inspect whether the aggregator explicitly accepts `local_diags` or `**kwargs`.
  - Dispatches with or without `local_diags` accordingly, ensuring any internal `TypeError` propagates immediately with full traceback.
  - Added return type validation ensuring a `(state_dict, dict)` tuple is returned.

#### Issue 3: Artificial Energy Fallback in FedTGE
- **Symptom:** `FedTGEAggregator` would catch missing or malformed client diagnostics and substitute an artificial array of ones (`np.ones(10)`).
- **Root Cause:** Overly permissive fallback logic designed for prototype robustness that violates scientific integrity.
- **Repair:**
  - Removed all artificial data synthesis fallbacks.
  - Added strict validation: verifies non-None `local_diags`, exact client count matching, presence of `'energy_vector'`, 1D dimensionality, non-empty size, and finiteness (rejects NaN and Inf with explicit `ValueError`).

#### Issue 4: Unused Edge Perturbation Parameter in FedTGE Augmentation
- **Symptom:** `_aug_random_edge()` in `multidata_suite/fedtge.py` accepted `perturb_percent=0.2`, but the perturbation count was governed by an average-degree heuristic `avg_degree = int(total_edges / num_nodes)`.
- **Root Cause:** Direct provenance from the official `ZitongShi/fedTGE` repository, which contains the unused parameter in its signature.
- **Repair:**
  - Documented official provenance and algorithm rationale.
  - Added explicit mode support: `mode="official_degree"` (default, preserving exact comparability with published baseline) and `mode="percentage"` (scaling perturbation proportionally when specified).
  - Verified determinism given fixed seeds, node index validity, and symmetry.

#### Issue 5: FedTGE Architecture Metadata Mismatch
- **Symptom:** Experiment metadata logged `"GCN(1433 -> 16 -> 7)"` while runtime configuration instantiated hidden channels = 32.
- **Root Cause:** Hardcoded strings in runner metadata dictionaries.
- **Repair:**
  - Updated `run_real_dataset_pipeline.py` and `run_extended_experiments.py` to dynamically construct model metadata using `config.hidden_channels` (32).
  - Preserved runtime network architecture intact (no retraining invalidated).

#### Issue 6: Unsafe Reuse of Existing Experimental Results and Partitions
- **Symptom:** An existing `final_summary.json` was sufficient to skip an experiment, even if incomplete (0 bytes from interrupted runs) or incompatible with requested seeds/hyperparameters. Partition caching did not verify node coverage.
- **Root Cause:** Simple `.exists()` checks and missing cache manifest validation.
- **Repair:**
  - Added `_atomic_save_json` using temporary files (`.tmp` -> replace) preventing corrupted zero-byte files on crash.
  - Implemented `validate_existing_experiment(context, slug)` validating file existence, non-zero size, valid JSON, required top-level keys, and exact hyperparameter compatibility (`seed`, `rounds`, `local_epochs`, `hidden_channels`, `learning_rate`, `poison_rate`, `trigger_size`, `num_clients`).
  - Added partition cache validation in `load_or_create_partition()` checking client count, seed, strategy, Dirichlet alpha, and node count matching `data.num_nodes`.

#### Issue 7: Missing FedTGE in Figure Scripts & Inconsistent Registry
- **Symptom:** FedTGE was executed by `run_real_dataset_pipeline.py` but excluded from primary method lists and hatching/coloring routines in `build_real_comparisons_and_figures.py` and `build_section4_extra_figures.py`.
- **Root Cause:** FedTGE was integrated into the training pipeline later than other baselines.
- **Repair:**
  - Established canonical `BENCHMARK_METHODS` registry in `multidata_suite/config.py` defining all 8 methods: Clean FedAvg, Attacked FedAvg, PD-FL, GSP-FL, FLPurifier-GNN, DMGNN-FL, FedTGE, ETD-FGL.
  - Updated both figure scripts with dedicated styles, colors, markers, and hatches for FedTGE.
  - Made figure generation resilient to subsets of executed methods without crashing.

#### Issue 8: Documentation Contradiction Regarding Component Weights
- **Symptom:** `docs/EXTENDED_EXPERIMENTS.md` and `README.md` described Full ETD-FGL as a three-channel configuration (0.45, 0.35, 0.20), contradicting the production frozen code (9/13 topology, 4/13 update, 0 explanation).
- **Root Cause:** Documentation lagged behind the ablation findings that eliminated GNNExplainer from production risk.
- **Repair:**
  - Updated documentation to clearly distinguish Production ETD-FGL ($\alpha_{\text{topo}}=9/13, \alpha_{\text{upd}}=4/13, \alpha_{\text{exp}}=0$) from the Historical Three-Channel Variant (0.45, 0.35, 0.20).
  - Verified that ablation runners correctly isolate components: topology-only (1.0, 0, 0), update-only (0, 0, 1.0), and unweighted aggregation (w/o trust weighting).

#### Issue 9: Incomplete Continuous Integration Workflow
- **Symptom:** GitHub Actions workflow only ran `python -m compileall -q .`, providing no verification of numerical routines, invariant stability, or aggregator dispatch.
- **Root Cause:** Minimal initial CI stub.
- **Repair:**
  - Configured `pytest.ini` with registered markers (`unit`, `integration`, `slow`) and warning filters.
  - Created `test_audit_regressions.py` providing 26 deterministic, offline unit tests (<5s execution).
  - Updated `.github/workflows/syntax-check.yml` to compile Python code and run offline unit tests with CPU PyTorch on every push and pull request.

---

## 4. Unresolved Scientific Observations (Non-Defects)

The following research considerations were audited in Phase 3 and are detailed in `audit/SCIENTIFIC_REVIEW.md`:
1. **Privileged Clean Reference Graph:** Production ETD-FGL assumes server access to exact pre-attack clean client graphs. In real-world deployments, a historical trusted initialization period or temporal drift tracking is required.
2. **Class-Stratified Partitioning:** Federated client partitioning relies on class labels across train/val/test splits to ensure non-empty classes per client. A label-blind partition protocol is proposed for future ablation.
3. **Client Scalability Confounding:** Increasing client count from 5 to 50 with 1 fixed malicious client reduces adversary fraction from 20% to 2%. Two separate studies (fixed attacker count vs fixed attacker fraction) are recommended.

These items represent methodological modeling assumptions rather than coding bugs. Per strict research integrity rules, no scientific protocols were altered without author authorization.
