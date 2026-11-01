# ETD-FGL Figure Source Mapping (Revision v4.1)

This document provides a strict, reproducible audit trail connecting every figure and individual subpanel in Revision v4.1 to its underlying source data files, CSV row identifiers, verified git commit SHA, and repository directories.

### Repository Commit Reference:
- **Current Working-Tree Commit:** `80a321027b26853eee1c2c4f415e1ec9c1f4961c` (HEAD, branch `audit-fix-verification`).
- **Parent Frozen Archive Commit:** `953e2501a3571d4e08bf6ef6d7e008d19762144d` (pre-audit archive; line numbers in `multidata_suite/defenses.py` are offset by -15 lines relative to HEAD due to diagnostic logging added at lines 232–285).

### Revision v4.1 Audit Fixes:
- **Figure F:** Corrected mathematical regime in Panel (d) and text mapping: code uses `max(0.4*d, 1e-8)`, establishing the constant anomaly plateau $A_0^{\text{topo}} \approx 0.848284$ at $d \ge 2.5 \times 10^{-8}$ (where $0.4d \ge 10^{-8}$), NOT $d > 10^{-8}$. Below $2.5 \times 10^{-8}$, $\text{MAD} = 10^{-8}$ and $z = d / 10^{-8}$ varies continuously, passing through $A_0 = 0.0$ at $d=0$. Clarified that $w_0 \equiv 4.12\%$ represents the **Fixed No Update** example ($A^{\text{upd}} = 0$) under equal client sample sizes ($n_i = n$). In Panel (b), noted that on Cora (Seed 42), the attacker's model update anomaly $A_0^{\text{upd}}$ is identically zero ($0.0000$) across all 50 rounds, with risk driven entirely by topological anomaly ($A_0^{\text{topo}} \approx 0.8483$).
- **Runtime Wording (Figures A & I):** Timings (177s, 773s, 400s) map to the complete 50-round training loop (`elapsed_seconds`), not per-round latency. Removed generic "$\le 1.1\times$ FedAvg" and unsupported ratio range ("$1.02\times$ to $1.21\times$"); reported measured loop runtimes directly (all under 11 seconds across all suites).
- **Multi-Seed Accuracy Baseline (Figures D & H):** Multi-seed baseline points ($75.00\%, 74.80\%, 84.90\%$) map to **Attacked FedAvg**, as no 3-seed Clean FedAvg control was run. Clean FedAvg is mapped to Seed 42, preserving accuracy within 1.30 pp (Cora 0.00 pp, PubMed +1.30 pp, Reddit -0.90 pp).
- **Inventory Traceability & Checkpoint Hashes:** Mapped 132 directory records and 132 checkpoint file paths to exactly **99 distinct checkpoint SHA-256 hashes on disk** and 33 verified file-path reuses, distinguishing verified cryptographic properties on disk from assertions of proven independent training execution processes.

---

## Source Traceability Matrix

| Figure Filename | Subpanel | Metric(s) Plotted | Dataset(s) | Method(s) / Condition(s) | Seed(s) | Primary Source File / Directory |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`Fig_A_Baseline_Comparison_Overview.png`** | (a) Clean Acc | `clean_test_accuracy` | Cora, PubMed, Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (b) Backdoor ASR | `attack_success_rate` | Cora, PubMed, Reddit | 7 attacked baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (c) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | 7 attacked baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (d) Loop Runtime | `elapsed_seconds` | Cora, PubMed, Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (50-round loop) |
| **`Fig_A1_Baseline_Comparison_Cora.png`** | (a)–(d) | Acc, ASR, Effect, Loop Runtime | Cora | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (`dataset == 'Cora'`) |
| **`Fig_A2_Baseline_Comparison_PubMed.png`** | (a)–(d) | Acc, ASR, Effect, Loop Runtime | PubMed | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (`dataset == 'PubMed'`) |
| **`Fig_A3_Baseline_Comparison_Reddit.png`** | (a)–(d) | Acc, ASR, Effect, Loop Runtime | Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (`dataset == 'Reddit'`) |
| **`Fig_B_Standard_Ablation.png`** | (a) Clean Acc | `clean_test_accuracy` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| | (b) Backdoor ASR | `attack_success_rate` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| | (c) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| | (d) Attacker Weight | `attacker_weight_mean` | Cora, PubMed, Reddit | 6 standard ablation variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'standard_ablation'`) |
| **`Fig_C_Controlled_Ablation.png`** | (a) Backdoor ASR | `asr_display` (%) | Cora, PubMed, Reddit | 3 controlled variants | Seeds 42, 43, 44 | `consolidated_data/controlled_ablation_summary.csv` |
| | (b) Paired $\Delta$ ASR | `delta_asr` (pp) | Cora, PubMed, Reddit | Fixed No Upd, Fixed No Topo | Seeds 42, 43, 44 | `consolidated_data/paired_differences.csv` |
| | (c) Clean Acc | `clean_accuracy_display` (%) | Cora, PubMed, Reddit | 3 controlled variants | Seeds 42, 43, 44 | `controlled_ablation_summary.csv` |
| | (d) Paired $\Delta$ Acc | `delta_clean_accuracy` (pp) | Cora, PubMed, Reddit | Fixed No Upd, Fixed No Topo | Seeds 42, 43, 44 | `consolidated_data/paired_differences.csv` |
| **`Fig_D_MultiSeed_Robustness.png`** | (a) Clean Acc | `clean_test_accuracy` | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'multiseed'`) |
| | (b) Backdoor ASR | `attack_success_rate` | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'multiseed'`) |
| | (c) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | Attacked FedAvg, ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`suite == 'multiseed'`) |
| **`Fig_E_Learning_Dynamics.png`** | Row 0 (Acc vs Round) | `test_accuracy` | Cora, PubMed, Reddit | Clean (Seed 42), Attacked, FedTGE, ETD-FGL | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method}/training_history.csv` |
| | Row 1 (ASR vs Round) | `attack_success_rate` | Cora, PubMed, Reddit | Attacked, FedTGE, ETD-FGL | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method}/training_history.csv` |
| **`Fig_F_Trust_Defense_Mechanisms.png`** | (a) Weight Suppression | `etdfgl_weight_client_0`| Cora, PubMed, Reddit | ETD-FGL | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_{cora,pubmed,reddit}/defended_etdfgl/training_history.csv` |
| | (b) Risk Breakdown | `topology_risk`, `update_risk`, `fused_risk` | Cora | ETD-FGL Client 0 ($A_0^{\text{upd}} \equiv 0.0000$ across all 50 rounds) | Seed 42 (50 rounds) | `outputs/final_multidataset/federated_cora/defended_etdfgl/training_history.csv` |
| | (c) Trust Factor | `etdfgl_trust_client_k`| Cora | Benign (1..4) vs Malicious (0)| Seed 42 (50 rounds) | `outputs/final_multidataset/federated_cora/defended_etdfgl/training_history.csv` |
| | (d) Scale-Invariance | Qualified regime | Theoretical & Empirical | $K=5, M=1, d \ge 2.5 \times 10^{-8}$ | Analytical | `multidata_suite/defenses.py:428–432` (`_robust_positive` in `80a3210`) |
| **`Fig_G_Attack_Effect_and_Defense_Gain.png`** | (a) Attack Effect | `attack_effect` | Cora, PubMed, Reddit | 7 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` |
| | (b) Absolute ASR Reduction | $\Delta \text{ASR}$ (pp) | Cora, PubMed, Reddit | Attacked FedAvg vs ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/multiseed_summary.csv` |
| | (c) Relative Reduction | Relative % Reduction | Cora, PubMed, Reddit | Attacked FedAvg vs ETD-FGL | Seeds 42, 43, 44 | `consolidated_data/multiseed_summary.csv` |
| **`Fig_H_Accuracy_ASR_Tradeoff.png`** | Cora, PubMed, Reddit | Acc vs ASR | Cora, PubMed, Reddit | Baselines (Seed 42) + Multiseed Centroids | Seeds 42, 43, 44 | `consolidated_data/baseline_seed42.csv` & `consolidated_data/multiseed_summary.csv` |
| **`Fig_I_Training_Runtime_Comparison.png`** | (a) Multi-Dataset Log | `elapsed_seconds` | Cora, PubMed, Reddit | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (50-round loop) |
| | (b) PubMed Linear | `elapsed_seconds` | PubMed | 8 baseline methods | Seed 42 | `consolidated_data/baseline_seed42.csv` (50-round loop) |
| **`Fig_S_Reddit_Seed_Heterogeneity.png`** | Seeds 42, 43, 44 | `attack_success_rate` | Reddit | Controlled variants | Seeds 42, 43, 44 | `consolidated_data/consolidated_experiments.csv` (`dataset == 'Reddit' & suite == 'controlled_ablation'`) |
| **`Fig_S_Standard_vs_Controlled_Comparison.png`** | (a) Topo vs (b) Upd | `asr_display` | Cora, PubMed, Reddit | Standard vs Controlled | Seeds 42, 43, 44 | `consolidated_data/standard_ablation_summary.csv` & `controlled_ablation_summary.csv` |

---

## Raw Result Directory References (132 Directory Records, 132 Checkpoint Paths, 99 Unique Checkpoint Hashes)

1. **Baseline Suite (Seed 42, 24 runs):**  
   - Output Summaries: `ETD-FGL/outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method_slug}/final_summary.json`  
   - Checkpoints: `ETD-FGL/outputs/final_multidataset/federated_{cora,pubmed,reddit}/{method_slug}/best_model.pt` (24 unique checkpoint SHA-256 hashes on disk).
2. **Multi-Seed Robustness Suite (Seeds 42, 43, 44, 18 runs):**  
   - Output Summaries: `ETD-FGL/outputs/extended_experiments/multiseed/{cora,pubmed,reddit}/seed_{42,43,44}/{method_slug}/final_summary.json`  
   - Checkpoints: `ETD-FGL/outputs/extended_experiments/multiseed/{cora,pubmed,reddit}/seed_{42,43,44}/{method_slug}/best_model.pt` (12 unique SHA-256 hashes on disk, with 6 verified file reuses of Seed 42 baselines).
3. **Standard Ablation Suite (Seeds 42, 43, 44, 54 runs):**  
   - Output Summaries: `ETD-FGL/outputs/extended_experiments/ablation/{cora,pubmed,reddit}/seed_{42,43,44}/{variant_slug}/final_summary.json`  
   - Checkpoints: `ETD-FGL/outputs/extended_experiments/ablation/{cora,pubmed,reddit}/seed_{42,43,44}/{variant_slug}/best_model.pt` (45 unique SHA-256 hashes on disk, with 9 verified file reuses of Attacked FedAvg across 3 seeds and 3 datasets).
4. **Controlled Ablation Suite (Seeds 42, 43, 44, 36 runs):**  
   - Output Summaries: `ETD-FGL/outputs/extended_experiments/controlled_ablation_v1/{cora,pubmed,reddit}/seed_{42,43,44}/{variant_slug}/final_summary.json`  
   - Checkpoints: `ETD-FGL/outputs/extended_experiments/controlled_ablation_v1/{cora,pubmed,reddit}/seed_{42,43,44}/{variant_slug}/best_model.pt` (18 unique SHA-256 hashes on disk, with 9 verified reuses of Attacked FedAvg and 9 verified reuses of Full ETD-FGL).
