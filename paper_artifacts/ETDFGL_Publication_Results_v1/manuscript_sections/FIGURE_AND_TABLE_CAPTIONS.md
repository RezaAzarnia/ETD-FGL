# ETD-FGL Publication Figure and Table Captions

## Figure Captions

### Main Figures

**Figure 1: Overall Performance Comparison across Cora, PubMed, and Reddit (Seed 42)**
Comprehensive benchmark evaluation of clean test accuracy (%) [top panel] and backdoor attack success rate (ASR %) [bottom panel] across eight evaluated methods on Cora, PubMed, and Reddit (Seed 42). Clean FedAvg defines the non-attacked empirical performance ceiling. Attacked FedAvg demonstrates severe backdoor vulnerability (58–76% ASR). While purification baselines degrade clean accuracy (FLPurifier-GNN drops Cora accuracy by 19.2% pts) or fail entirely on Reddit (DMGNN-FL prunes 0 edges, matching Attacked FedAvg), ETD-FGL eliminates backdoor penetration (<4.3% ASR) while fully preserving clean classification accuracy.

**Figure 2: Multi-Seed Robustness Evaluation: Attacked FedAvg vs. ETD-FGL (Seeds 42, 43, 44)**
Multi-seed robustness comparison between unmitigated Attacked FedAvg and ETD-FGL across three independent random seeds (42, 43, 44). Bars display sample mean; error bars indicate sample standard deviation ($ddof=1$); individual points plot granular seed outcomes. Reddit Seed 43 acts as an outlier where ETD-FGL ASR reaches 34.82% due to community partition overlap, yet remains 39.6% points below Attacked FedAvg (74.42%).

**Figure 3: Clean Accuracy versus Backdoor ASR Trade-off (Seed 42)**
Trade-off visualization between Clean Classification Accuracy (%) [x-axis, higher is better] and Backdoor Attack Success Rate (%) [y-axis, lower is better] across Cora, PubMed, and Reddit (Seed 42). The optimal operating quadrant is the bottom-right (high accuracy, zero ASR). ETD-FGL resides firmly in the optimal quadrant across all benchmarks, whereas baselines either exhibit excessive vulnerability (top-right) or sacrifice clean utility (bottom-left).

**Figure 4: Controlled Component Ablation with Held-Constant Coefficients (Seeds 42, 43, 44)**
Controlled ablation evaluating Full ETD-FGL ($R = rac{9}{13} A_{topo} + rac{4}{13} A_{upd}$) against Fixed No Update ($R = rac{9}{13} A_{topo}$) and Fixed No Topology ($R = rac{4}{13} A_{upd}$) with coefficients strictly held constant across Seeds 42, 43, 44. Removing topology triggers catastrophic defense failure (42.5% ASR on Cora, 66.3% on Reddit). Removing update increases ASR across all datasets (+1.19% on Cora, +0.28% on PubMed, +11.11% on Reddit), isolating the non-redundant dynamic role of both channels.

**Figure 5: Federated Learning Dynamics over 50 Communication Rounds (Seed 42)**
Learning dynamics across 50 communication rounds on Cora, PubMed, and Reddit (Seed 42). Top row: Clean test accuracy convergence. Bottom row: Backdoor ASR convergence. Unmitigated FedAvg and FedTGE rapidly converge to high ASR within 15 rounds, while ETD-FGL continuously suppresses backdoor injection from early rounds without retarding clean convergence.

**Figure 6: Attacker Aggregation Weight Suppression Dynamics (Seed 42)**
Evolution of malicious client aggregation weight ($w_0$) across 50 communication rounds under controlled ablation variants (Seed 42). Horizontal line represents the uniform baseline share ($1/K = 20\%$). Full ETD-FGL and Fixed No Update rapidly suppress attacker weight to $\le 4.7\%$, while Fixed No Topology leaves attacker weight elevated at 13–19%, permitting backdoor infiltration.

---

### Supplementary Figures

**Figure S1: Standard vs. Controlled Ablation: Impact of Coefficient Normalization**
Comparison between standard ablation (where ablated channel weights were re-normalized to 1.0) and controlled ablation (where coefficients were held constant at 9/13 and 4/13). In standard Topology-only, inflating the topology coefficient from 9/13 to 1.0 (+44%) artificially strengthened trust suppression, yielding lower ASR than Full ETD-FGL. The controlled comparison isolates channel removal under held-constant penalty.

**Figure S2: Trigger Attack Effect across Benchmark Datasets (Seed 42)**
Trigger Attack Effect (defined as ASR minus clean target rate) across Cora, PubMed, and Reddit (Seed 42). The solid black line marks the zero reference threshold. Negative values confirm that target-class prediction on triggered test nodes is lower than clean prior probability, verifying complete neutralization of backdoor triggers.

**Figure S3: Timed Federated Training-Loop Runtime Comparison (Seed 42)**
Timed 50-round federated training loop runtime across benchmark datasets on identical GPU hardware. Timings reflect active training and aggregation; offline partitioning and server reference precomputation are excluded. ETD-FGL adds minimal aggregation overhead (+10.5% average) over standard FedAvg.

**Figure S4: Per-Seed Breakdown of Reddit Controlled Ablation (Seeds 42, 43, 44)**
Granular per-seed breakdown of Backdoor ASR on Reddit across controlled ablation variants. Seed 43 exhibits elevated vulnerability across all variants (34.82% Full, 43.52% No Update, 70.59% No Topology), illuminating Reddit's structural heterogeneity.

**Figure S5: Benign-Client Risk and Attacker Aggregation Weight Preservation**
Benign client risk and attacker aggregation weight across controlled ablation variants. In Fixed No Update, benign risk is 0.0000. In Full ETD-FGL, benign risk remains very low (<0.06), preserving over 85% trust. Attacker weight is compressed from 20% down to 2.5–4.8% by Full ETD-FGL.

---

## Table Captions

- **Table 1: Dataset Characteristics and Federated Experimental Configurations**: Benchmark dataset topology statistics, node feature dimensions, client counts, local training hyperparameters, and targeted clique backdoor attack parameters.
- **Table 2: Performance and Defense Effectiveness Comparison Across Benchmark Datasets (Seed 42)**: Clean test accuracy (%), Backdoor ASR (%), Attack Effect (% pts), and training runtime (s) across eight evaluated methods on Seed 42.
- **Table 3: Multi-Seed Robustness Evaluation: Attacked FedAvg vs. ETD-FGL (Seeds 42, 43, 44)**: Multi-seed mean and sample standard deviation ($ddof=1$) comparing Attacked FedAvg and ETD-FGL across Seeds 42, 43, 44.
- **Table 4: Standard Component Ablation Study Across Benchmark Datasets (Seeds 42, 43, 44)**: Historical standard ablation comparing Full ETD-FGL against single-channel variants normalized to coefficient 1.0.
- **Table 5: Controlled Component Ablation Study with Held-Constant Coefficients (Seeds 42, 43, 44)**: Rigorous controlled ablation isolating component removal with coefficients held constant at 9/13 and 4/13.
- **Table 6: Paired Within-Seed Component Contributions ($\Delta = 	ext{Variant} - 	ext{Full ETD-FGL}$)**: Within-seed paired difference statistics isolating marginal performance changes from removing each evidence channel.
- **Table 7: Client Risk and Attacker Aggregation Weight Dynamics Under Controlled Defense Variants**: Attacker weight suppression, benign client risk preservation, and trust discrimination ratios under controlled variants.
- **Table 8: Computational Runtime Comparison: 50 Communication Rounds on Identical GPU Hardware**: Timed training loop execution time (s) and relative computational overhead versus standard FedAvg.
- **Table 9: Complete Granular Per-Seed Experimental Results for All Evaluated Runs ($N=132$)**: Machine-readable master repository table providing granular outcomes for all 132 completed runs.
