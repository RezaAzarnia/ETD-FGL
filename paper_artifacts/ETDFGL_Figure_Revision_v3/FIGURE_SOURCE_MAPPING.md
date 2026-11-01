# ETD-FGL Figure Source Mapping (Revision v3)

This document provides a strict, reproducible audit trail connecting every figure and individual subpanel in Revision v3 to its underlying source data files, CSV row identifiers, and repository directories.

Revision v3 enhancements:
- **Figure G:** Panel (b) computes absolute ASR reduction $\Delta \text{ASR} = \text{ASR}_{\text{FedAvg}} - \text{ASR}_{\text{ETDFGL}}$ rendered with explicit positive percentage points (`+56.8% pts`, `+8.3% pts`, `+60.3% pts`) and axis label `Absolute Reduction (% points)`. Legend layout positioned safely below figure suptitle.
- **Figure H:** Baseline points encode methods strictly via distinct marker symbols and colors in the header legend, eliminating overlapping text collision. Text annotations are reserved for the two distribution centroids (`Attacked FedAvg` and `ETD-FGL`) with 2D error whiskers.
- **Figure C:** Panels (b) and (d) designate paired differences strictly in percentage points (`% pts` or `% points`).

---

## Source Traceability Matrix

| Figure Filename | Subpanel | Metric(s) Plotted | Dataset(s) | Method(s) / Condition(s) | Seed(s) | Primary Source File / Directory |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`Fig_A_Baseline_Comparison_Overview.png`** | (a) Clean Acc | `clean_test_accuracy` | Cora, PubMed, Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (b) Backdoor ASR | `attack_success_rate` | Cora, PubMed, Reddit | 7 attacked baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (c) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | 7 attacked baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (d) Training Runtime | `elapsed_seconds` | Cora, PubMed, Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| **`Fig_A1_Baseline_Comparison_Cora.png`** | (a)–(d) | Acc, ASR, Effect, Runtime | Cora | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (rows where `dataset == 'Cora'`) |
| **`Fig_A2_Baseline_Comparison_PubMed.png`** | (a)–(d) | Acc, ASR, Effect, Runtime | PubMed | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (rows where `dataset == 'PubMed'`) |
| **`Fig_A3_Baseline_Comparison_Reddit.png`** | (a)–(d) | Acc, ASR, Effect, Runtime | Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (rows where `dataset == 'Reddit'`) |
| **`Fig_B_Standard_Ablation.png`** | (a) Clean Acc | `clean_test_accuracy` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| | (b) Backdoor ASR | `attack_success_rate` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| | (c) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| | (d) Attacker Weight | `attacker_weight_mean` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| **`Fig_C_Controlled_Ablation.png`** | (a) Backdoor ASR | `asr_display` (%) | Cora, PubMed, Reddit | 3 controlled variants | Seeds 42, 43, 44 | `consolidated_data/controlled_ablation_summary.csv` |
| | (b) Paired $\Delta$ ASR | `delta_asr` (% pts) | Cora, PubMed, Reddit | Fixed No Upd, Fixed No Topo | Seeds 42, 43, 44 | `consolidated_data/paired_differences.csv` |
| | (c) Clean Acc | `clean_accuracy_display` (%) | Cora, PubMed, Reddit | 3 controlled variants | Seeds 42, 43, 44 | `controlled_ablation_summary.csv` |
| | (d) Paired $\Delta$ Acc | `delta_clean_accuracy` (% pts) | Cora, PubMed, Reddit | Fixed No Upd, Fixed No Topo | Seeds 42, 43, 44 | `consolidated_data/paired_differences.csv` |
| **`Fig_D_MultiSeed_Robustness.png`** | (a) Clean Acc | `clean_test_accuracy` | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'multiseed'`) |
| | (b) Backdoor ASR | `attack_success_rate` | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'multiseed'`) |
| | (c) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'multiseed'`) |
| **`Fig_E_Learning_Dynamics.png`** | Row 0 (Acc vs Round) | `test_accuracy` | Cora, PubMed, Reddit | Clean, Attacked, FedTGE, ETD-FGL | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method}/training_history.csv` |
| | Row 1 (ASR vs Round) | `attack_success_rate` | Cora, PubMed, Reddit | Attacked, FedTGE, ETD-FGL | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method}/training_history.csv` |
| **`Fig_F_Trust_Defense_Mechanisms.png`** | (a) Weight Suppression | `etdfgl_weight_client_0`| Cora, PubMed, Reddit | ETD-FGL | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_{cora,pubmed,reddit}/defended_etdfgl/training_history.csv` |
| | (b) Risk Breakdown | `topology_risk`, `update_risk`, `fused_risk` | Cora | ETD-FGL Client 0 | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_cora/defended_etdfgl/training_history.csv` |
| | (c) Trust Factor | `etdfgl_trust_client_k`| Cora | Benign (1..4) vs Malicious (0)| Seed 42 (50 rounds) | `outputs/final_multidataset/federated_cora/defended_etdfgl/training_history.csv` |
| | (d) Mathematical Proof | Theoretical & Empirical | Synthetic & Empirical | 5-Client Federation | Analytical | ETD-FGL Aggregator Algorithm (`_robust_positive`) |
| **`Fig_G_Attack_Effect_and_Defense_Gain.png`** | (a) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | 7 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (b) Absolute ASR Reduction | $\Delta \text{ASR}$ (% pts) | Cora, PubMed, Reddit | FedAvg vs ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/multiseed_summary.csv` |
| | (c) Relative Reduction | Relative % Reduction | Cora, PubMed, Reddit | FedAvg vs ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/multiseed_summary.csv` |
| **`Fig_H_Accuracy_ASR_Tradeoff.png`** | Cora, PubMed, Reddit | Acc vs ASR | Cora, PubMed, Reddit | Baselines (Seed 42) + Multiseed Centroids | Seeds 42, 43, 44 | `consolidated_data/baseline_seed42.csv` & `consolidated_data/multiseed_summary.csv` |
| **`Fig_I_Training_Runtime_Comparison.png`** | (a) Multi-Dataset Log | `elapsed_seconds` | Cora, PubMed, Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (b) PubMed Linear | `elapsed_seconds` | PubMed | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (rows where `dataset == 'PubMed'`) |
| **`Fig_S_Reddit_Seed_Heterogeneity.png`** | Seeds 42, 43, 44 | `attack_success_rate` | Reddit | Controlled variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`dataset == 'Reddit' & suite == 'controlled_ablation'`) |
| **`Fig_S_Standard_vs_Controlled_Comparison.png`** | (a) Topo vs (b) Upd | `asr_display` | Cora, PubMed, Reddit | Standard vs Controlled | Seeds 42, 43, 44 | `consolidated_data/standard_ablation_summary.csv` & `controlled_ablation_summary.csv` |

---

## Raw Result Directory References

1. **Baseline Suite (Seed 42, 24 runs):**  
   `ETD-FGL/outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method_slug}/final_summary.json`
2. **Multi-Seed Robustness Suite (Seeds 42, 43, 44, 18 runs):**  
   `ETD-FGL/outputs/extended_experiments/multiseed/{cora,pubmed,reddit}/seed_{42,43,44}/{method_slug}/final_summary.json`
3. **Standard Ablation Suite (Seeds 42, 43, 44, 54 runs):**  
   `ETD-FGL/outputs/extended_experiments/ablation/{cora,pubmed,reddit}/seed_{42,43,44}/{variant_slug}/final_summary.json`
4. **Controlled Ablation Suite (Seeds 42, 43, 44, 36 runs):**  
   `ETD-FGL/outputs/extended_experiments/controlled_ablation_v1/{cora,pubmed,reddit}/seed_{42,43,44}/{variant_slug}/final_summary.json`
