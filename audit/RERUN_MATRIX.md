# ETD-FGL Rerun Matrix

This document defines the rerun requirements following the scientific code audit, classifying modifications into Class A, B, C, and D, and providing exact executable commands for reproducing all experimental studies.

---

## 1. Classification of Code Modifications

| Change / Issue | Category | Nature of Modification | Model Training Rerun Required? |
|---|---|---|---|
| **Issue 1 (6D -> 5D Descriptor Tests)** | Class B | Test / verification script assertion update | **No** (Production descriptor unchanged) |
| **Issue 2 (Broad TypeError Fix)** | Class B | Aggregator dispatch signature inspection | **No** (Numerical path unchanged) |
| **Issue 3 (FedTGE Fallback Removal)** | Class C | Strict validation of FedTGE energy inputs | **Targeted** (Only if prior run used fallback) |
| **Issue 4 (FedTGE Perturbation Param)** | Class B | Documentation & explicit mode parameter | **No** (Official behavior preserved as default) |
| **Issue 5 (Architecture Metadata)** | Class A | Runner metadata dictionary strings | **No** (Runtime model was already 32 channels) |
| **Issue 6 (Experiment Provenance)** | Class B | Validation guards & atomic file saving | **No** (Enforces cache safety on future runs) |
| **Issue 7 (Figure Generation Baseline)** | Class B | Figure scripts include FedTGE styles & hatch | **Figure Rerun Only** (No training needed) |
| **Issue 8 (Ablation Documentation)** | Class A | Documentation aligned with 9/13 + 4/13 weights | **No** (Production code was already frozen) |
| **Issue 9 (Continuous Integration)** | Class B | Added offline unit test suite & pytest config | **No** (Infrastructure only) |

---

## 2. Experimental Execution Matrix

### 2.1 Figure Generation Re-Execution (Recommended Immediate Step)
Because `build_real_comparisons_and_figures.py` and `build_section4_extra_figures.py` were updated to properly include FedTGE with dedicated markers and hatching, rerun the figure scripts over existing completed outputs:

#### Windows PowerShell:
```powershell
.\.venv\Scripts\python.exe build_real_comparisons_and_figures.py --dataset all
.\.venv\Scripts\python.exe build_section4_extra_figures.py
```

#### Linux Bash:
```bash
python build_real_comparisons_and_figures.py --dataset all
python build_section4_extra_figures.py
```
**Expected Outputs:**
- `outputs/final_multidataset/cross_dataset_figures/`
- `outputs/final_multidataset/section4_extra_figures/`
- `outputs/final_multidataset/federated_*/comparison.csv`

---

### 2.2 Main Benchmark Clean Replication (Optional Full Rerun)
If the authors wish to generate a completely fresh, end-to-end experimental run validating the verified codebase:

| Dataset | Methods | Rounds / Epochs | Est. Runtime (CPU) | Est. Runtime (CUDA) | Output Directory |
|---|---|---|---|---|---|
| **Cora** | All 8 Baselines | 50 R / 3 E | ~15 min | ~3 min | `outputs/final_multidataset/federated_cora/` |
| **PubMed** | All 8 Baselines | 50 R / 3 E | ~45 min | ~8 min | `outputs/final_multidataset/federated_pubmed/` |
| **Reddit** (Sampled) | All 8 Baselines | 50 R / 3 E | ~90 min | ~18 min | `outputs/final_multidataset/federated_reddit/` |

#### Windows PowerShell:
```powershell
# Force rerun all 8 methods from scratch
.\.venv\Scripts\python.exe run_real_dataset_pipeline.py --dataset cora --force
.\.venv\Scripts\python.exe run_real_dataset_pipeline.py --dataset pubmed --force
.\.venv\Scripts\python.exe run_real_dataset_pipeline.py --dataset reddit --force
```

#### Linux Bash:
```bash
python run_real_dataset_pipeline.py --dataset cora --force
python run_real_dataset_pipeline.py --dataset pubmed --force
python run_real_dataset_pipeline.py --dataset reddit --force
```

---

### 2.3 Extended Studies Execution Matrix

| Study | Command (PowerShell) | Conditions / Sweeps | Output Location |
|---|---|---|---|
| **Multi-Seed** | `.\.venv\Scripts\python.exe run_extended_experiments.py --study multiseed --force` | Seeds: 42, 43, 44 | `outputs/extended_experiments/multiseed/` |
| **Non-IID Dirichlet** | `.\.venv\Scripts\python.exe run_extended_experiments.py --study noniid --force` | $\alpha \in \{0.1, 0.5, 1.0\}$ | `outputs/extended_experiments/noniid/` |
| **Component Ablation** | `.\.venv\Scripts\python.exe run_extended_experiments.py --study ablation --force` | 5 ablation variants | `outputs/extended_experiments/ablation/` |
| **Poison Rate Sensitivity**| `.\.venv\Scripts\python.exe run_extended_experiments.py --study sensitivity_poison --force` | Rates: 0.05, 0.10, 0.20, 0.30 | `outputs/extended_experiments/sensitivity_poison/` |
| **Trigger Size Sensitivity**| `.\.venv\Scripts\python.exe run_extended_experiments.py --study sensitivity_trigger --force` | Sizes: 2, 3, 4, 5 nodes | `outputs/extended_experiments/sensitivity_trigger/` |
| **Client Scalability** | `.\.venv\Scripts\python.exe run_extended_experiments.py --study clients --force` | Clients: 5, 10, 20, 30, 50 | `outputs/extended_experiments/clients/` |

To build the extended journal summary figures and tables:
```powershell
.\.venv\Scripts\python.exe build_extended_experiment_figures.py
```
**Output Directory:** `outputs/extended_experiments/journal_summary/`
