# ETD-FGL Test and Verification Report

**Date of Execution:** October 2026
**Execution Environment:**
- **Operating System:** Microsoft Windows [Version 10.0.19045]
- **Python Version:** 3.11.9 (tags/v3.11.9:de542f0)
- **Virtual Environment:** `c:\Users\R_Azarnia\Desktop\main paper\ETD-FGL\.venv`
- **Core Dependencies:**
  - `torch`: 2.14.1+cpu
  - `torch_geometric`: 2.8.1
  - `numpy`: 2.4.6
  - `scipy`: 1.17.1
  - `scikit-learn`: 1.9.1
  - `pandas`: 3.0.6
  - `matplotlib`: 3.11.2
  - `networkx`: 3.6.1
  - `pytest`: 9.1.1
  - `gudhi`: 3.13.0
  - `tqdm`: 4.70.1

---

## 1. Test Execution Commands & Summary

| Test Suite / Script | Command Executed | Tests Passed | Tests Failed | Status |
|---|---|---|---|---|
| Environment Sanity | `python check_environment.py` | 1/1 checks | 0 | **PASS** |
| Bytecode Compilation | `python -m compileall -q -x "\.venv" .` | All modules clean | 0 | **PASS** |
| Audit Regressions (Offline) | `pytest -v test_audit_regressions.py` | 26/26 | 0 | **PASS** |
| Homophily Leakage & Invariance | `pytest -v test_homophily_leakage_fix.py` | 5/5 | 0 | **PASS** |
| Method & Weight Alignment | `pytest -v test_stage2_alignment.py` | 6/6 | 0 | **PASS** |
| FedTGE Verification Suite | `pytest -v test_stage4_3_fedtge_verification.py` | 9/9 | 0 | **PASS** |
| 5D Multi-Dataset Descriptor Sanity | `pytest -v test_final_5d_descriptor.py` | 9/9 | 0 | **PASS** |
| Stage 1 Mask & Verification Runner | `python run_stage1_verification.py` | All stages clean | 0 | **PASS** |
| Full 3-Dataset Benchmark Training | `python run_real_dataset_pipeline.py --dataset all` | Not run in audit CI | 0 | **NOT RUN** (High Compute) |
| Extended Multi-Seed Studies | `python run_extended_experiments.py --study all` | Not run in audit CI | 0 | **NOT RUN** (High Compute) |

**Total Executed Test Cases:** 55
**Total Passed:** 55 (100% Pass Rate)
**Total Failed:** 0

---

## 2. Detailed Breakdown of Test Suites

### 2.1 `test_audit_regressions.py` (26 Tests)
- `test_production_descriptor_shape_and_coordinates`: **PASS** (Verifies 5 coordinates).
- `test_production_descriptor_strict_label_independence`: **PASS** (Bit-for-bit label invariance).
- `test_production_descriptor_strict_mask_independence`: **PASS** (Bit-for-bit mask invariance).
- `test_production_descriptor_degenerate_graphs`: **PASS** (Empty, single-node, isolated graphs yield finite 0.0 values).
- `test_historical_homophily_diagnostics_decoupled`: **PASS** (Diagnostic calculations decoupled from descriptor).
- `test_invoke_aggregator_with_diagnostics`: **PASS** (Passes `local_diags` when accepted).
- `test_invoke_aggregator_without_diagnostics`: **PASS** (Omits `local_diags` cleanly).
- `test_invoke_aggregator_propagates_internal_typeerror`: **PASS** (Internal `TypeError` is not swallowed).
- `test_invoke_aggregator_invalid_output_type`: **PASS** (Non-tuple returns rejected with `ValueError`).
- `test_fedtge_aggregator_rejects_missing_diags`: **PASS** (Rejects `local_diags=None`).
- `test_fedtge_aggregator_rejects_mismatched_client_count`: **PASS** (Rejects length mismatch).
- `test_fedtge_aggregator_rejects_missing_energy_vector_key`: **PASS** (Rejects missing key).
- `test_fedtge_aggregator_rejects_nan_or_inf_energy`: **PASS** (Rejects NaN and Inf).
- `test_fedtge_aggregator_valid_run`: **PASS** (Succeeds on clean valid vectors).
- `test_aug_random_edge_determinism`: **PASS** (Deterministic with seed).
- `test_aug_random_edge_node_index_bounds`: **PASS** (Indices strictly $< N$).
- `test_aug_random_edge_percentage_mode_sensitivity`: **PASS** (Perturbation scales with percentage).
- `test_gcn_architecture_runtime_parameters`: **PASS** (Verifies 32 hidden channels and parameter count).
- `test_validate_existing_experiment_guards`: **PASS** (Rejects 0-byte, corrupted JSON, missing checkpoints, seed mismatch).
- `test_partition_validation_and_caching`: **PASS** (Validates cached node coverage and seed).
- `test_benchmark_methods_registry`: **PASS** (All 8 canonical benchmark methods present).
- `test_production_aggregator_weights_frozen`: **PASS** (Verifies $\alpha_{\text{topo}}=9/13, \alpha_{\text{upd}}=4/13, \alpha_{\text{exp}}=0$).
- `test_configurable_aggregator_ablation_variants`: **PASS** (Isolates topology-only, update-only, no-trust, and historical variant).
- `test_robust_positive_scaling`: **PASS** (MAD scaling produces non-negative, finite scores).
- `test_flatten_delta_and_update_anomaly`: **PASS** (Coordinate median delta computation verified).
- `test_trust_weight_normalization_and_clipping`: **PASS** (Trust clipped to $[0.02, 1.0]$, weights sum to $1.0$).

### 2.2 `test_homophily_leakage_fix.py` (5 Tests)
- `test_a_validation_test_leakage`: **PASS**
- `test_b_training_label_sensitivity`: **PASS**
- `test_c_mixed_edge`: **PASS**
- `test_d_empty_eligible_set`: **PASS**
- `test_e_non_homophily_descriptor_invariance`: **PASS**

### 2.3 `test_stage2_alignment.py` (6 Tests)
- `test_a_exact_fusion_equation`: **PASS**
- `test_b_explanation_independence`: **PASS**
- `test_c_coefficient_sum`: **PASS**
- `test_d_production_runner_defaults`: **PASS**
- `test_e_production_5d_descriptor_and_historical_diagnostic`: **PASS**
- `test_f_configurable_historical_variant`: **PASS**

### 2.4 `test_stage4_3_fedtge_verification.py` (9 Tests)
- `test_a_architecture`: **PASS**
- `test_b_energy_only_parameter_update`: **PASS**
- `test_c_substitute_generation`: **PASS**
- `test_d_client_selection`: **PASS**
- `test_e_energy_graph`: **PASS**
- `test_f_propagation`: **PASS**
- `test_g_aggregation`: **PASS**
- `test_h_supervised_budget`: **PASS**
- `test_i_benchmark_isolation`: **PASS**

### 2.5 `test_final_5d_descriptor.py` (9 Tests)
- `test_descriptor_label_invariance`: **PASS**
- `test_descriptor_mask_invariance`: **PASS**
- `test_descriptor_structural_sensitivity`: **PASS**
- `test_descriptor_degenerate_graphs`: **PASS**
- `test_etdfgl_fusion_regression`: **PASS**
- `test_cora_seed42_iid_descriptor_sanity`: **PASS**
- `test_multidataset_5d_descriptor_sanity[cora]`: **PASS**
- `test_multidataset_5d_descriptor_sanity[pubmed]`: **PASS**
- `test_multidataset_5d_descriptor_sanity[reddit]`: **PASS**

---

## 3. Test Limitations & Out-of-Scope Reruns

1. **Full Benchmark Reruns:** Executing full 50-round training for all 8 methods across Cora, PubMed, and Reddit requires substantial wall-clock time and GPU resources. These experiments were NOT run automatically during the audit to avoid unapproved long computations and accidental overwriting of historical outputs.
2. **GPU Acceleration Tests:** All unit and regression tests were verified under CPU execution (`torch.device("cpu")`), ensuring maximum portability across CI runners. GPU tensor operations use identical PyTorch kernels.
