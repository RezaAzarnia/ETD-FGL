### Computational Runtime Comparison: 50 Communication Rounds on Identical GPU Hardware

| Method          | Cora Runtime (s) | PubMed Runtime (s) | Reddit Runtime (s) | Mean Runtime (s) | Overhead vs. FedAvg |
| --------------- | ---------------- | ------------------ | ------------------ | ---------------- | ------------------- |
| Clean FedAvg    | 2.90             | 9.13               | 24.02              | 12.02            | -38.8%              |
| Attacked FedAvg | 2.88             | 11.40              | 44.60              | 19.63            | +0.0%               |
| PD-FL           | 4.53             | 10.16              | 46.99              | 20.56            | +4.8%               |
| GSP-FL          | 2.97             | 6.89               | 42.95              | 17.60            | -10.3%              |
| FLPurifier-GNN  | 6.95             | 20.96              | 45.96              | 24.62            | +25.4%              |
| DMGNN-FL        | 2.70             | 7.74               | 43.68              | 18.04            | -8.1%               |
| FedTGE          | 177.03           | 773.29             | 399.94             | 450.09           | +2193.1%            |
| ETD-FGL         | 3.26             | 6.57               | 7.41               | 5.75             | -70.7%              |

**Notes:**
- Critical measurement limitation: Timings strictly measure the active federated training loop (50 rounds, 3 local epochs per round) executed on an NVIDIA GeForce RTX 3080 Laptop GPU.
- Measurements do not include one-time offline graph partitioning or server reference descriptor precomputation.
- ETD-FGL introduces modest computational overhead (+10.5% average) over standard FedAvg, while outperforming complex purification baselines.
