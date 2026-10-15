# Extended ETD-FGL Experiments

This document describes the five additional studies used to strengthen the experimental evaluation.

## 1. Multi-seed evaluation

Seeds: 42, 43, 44.

The main comparison is repeated for all implemented methods. For sampled Reddit, the 8,000-node sample is held fixed with `reddit_sample_seed=42`; the training and client-partition seed changes across runs. This avoids conflating model stochasticity with a different Reddit sample.

Final metrics are aggregated as mean ± sample standard deviation (`ddof=1`).

## 2. Non-IID Dirichlet evaluation

Dirichlet alpha values: 0.1, 0.5, 1.0.

Partitioning is label-skewed and split-aware: train, validation, test, and unused nodes remain identifiable, while class membership is distributed across clients according to independent Dirichlet draws. Every node is assigned exactly once. A minimal repair procedure guarantees at least one training node per client and at least one non-target training node for the designated malicious client when mathematically possible.

The default comparison includes Attacked FedAvg, PD-FL, FLPurifier-GNN, and ETD-FGL.

## 3. Real component ablation

The following variants are trained from scratch under the same attacked setting:

- **Production ETD-FGL (Full final)**: Frozen two-channel formulation using topology drift (9/13 ≈ 0.6923) and model-update anomaly (4/13 ≈ 0.3077), with explanation weight = 0.0.
- **ETD-FGL Topology-only (w/o Update)**: Model-update anomaly removed (topology 1.0, update 0.0, explanation 0.0), isolating structural drift defense.
- **ETD-FGL Update-only (w/o Topology)**: Topology drift removed (topology 0.0, update 1.0, explanation 0.0), isolating gradient-space anomaly defense.
- **ETD-FGL w/o Trust Weighting**: Risk is computed using production weights (9/13, 4/13), but aggregation falls back to standard client sample-size weighting, directly isolating the benefit of trust-weighted aggregation.
- **Historical Three-Channel Variant (0.45 / 0.35 / 0.20)**: Preserved historical development baseline incorporating GNNExplainer explanation evidence (topology 0.45, explanation 0.35, update 0.20).

The ablation study uses real training runs from scratch without synthetic or hand-entered values.

## 4. Sensitivity analysis

Two independent one-factor-at-a-time studies are included:

- Poisoning rate: 0.05, 0.10, 0.20, 0.30 with trigger size fixed at 3.
- Trigger size: 2, 3, 4, 5 with poisoning rate fixed at 0.20.

Attacked FedAvg and ETD-FGL are retrained for every condition. Clean test accuracy, ASR, trigger effect, and runtime are recorded.

## 5. Number-of-clients scalability

Client counts: 5, 10, 20, 30, 50.

The IID partitioner uses rotating stratified assignment so that public Planetoid training nodes are spread across high client counts without producing empty training clients. The study records clean accuracy, ASR, trigger effect, and runtime.

The default comparison includes Attacked FedAvg, PD-FL, FLPurifier-GNN, and ETD-FGL. This can be changed through `--methods`.

## Reproducibility and fairness

- Each compared method resets the RNG to the condition seed before training.
- All methods within a condition share the same dataset, partition, attack configuration, number of rounds, local epochs, model architecture, and optimization settings unless the method itself requires a specific training procedure.
- Existing completed conditions are reused unless `--force` is supplied.
- Figure generation reads only completed `final_summary.json` files and never fills missing runs with estimated values.
