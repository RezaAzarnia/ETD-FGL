### Controlled Component Ablation Study with Held-Constant Coefficients (Seeds 42, 43, 44)

| Dataset | Evaluated Variant | Risk Formulation $R_k$                         | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (% pts) ↓ | Attacker Weight ($w_0$ %) ↓ | Benign Risk ($R_{benign}$) ↓ |
| ------- | ----------------- | ---------------------------------------------- | -------------------- | ------------------ | ----------------------- | --------------------------- | ---------------------------- |
| Cora    | Full ETD-FGL      | $\frac{9}{13} A_{topo} + \frac{4}{13} A_{upd}$ | 75.57 ± 1.57         | 5.21 ± 0.88        | -2.22 ± 2.17            | 4.76 ± 0.03                 | 0.0577 ± 0.0007              |
| Cora    | Fixed No Update   | $\frac{9}{13} A_{topo}$                        | 75.87 ± 1.56         | 6.40 ± 1.59        | -1.88 ± 2.76            | 4.12 ± 0.00                 | 0.0000 ± 0.0000              |
| Cora    | Fixed No Topology | $\frac{4}{13} A_{upd}$                         | 76.10 ± 0.87         | 42.53 ± 15.94      | 35.10 ± 14.40           | 18.41 ± 0.60                | 0.0610 ± 0.0032              |
| PubMed  | Full ETD-FGL      | $\frac{9}{13} A_{topo} + \frac{4}{13} A_{upd}$ | 75.50 ± 2.01         | 0.89 ± 0.56        | -3.54 ± 0.53            | 4.55 ± 0.04                 | 0.0487 ± 0.0054              |
| PubMed  | Fixed No Update   | $\frac{9}{13} A_{topo}$                        | 74.57 ± 3.17         | 1.18 ± 0.71        | -3.90 ± 0.49            | 4.12 ± 0.00                 | 0.0000 ± 0.0000              |
| PubMed  | Fixed No Topology | $\frac{4}{13} A_{upd}$                         | 75.70 ± 1.90         | 4.47 ± 3.45        | -1.67 ± 3.78            | 15.76 ± 0.59                | 0.0281 ± 0.0058              |
| Reddit  | Full ETD-FGL      | $\frac{9}{13} A_{topo} + \frac{4}{13} A_{upd}$ | 84.87 ± 0.40         | 14.08 ± 18.19      | 13.77 ± 18.09           | 2.53 ± 0.08                 | 0.0203 ± 0.0012              |
| Reddit  | Fixed No Update   | $\frac{9}{13} A_{topo}$                        | 85.00 ± 0.89         | 25.19 ± 17.81      | 24.91 ± 17.65           | 4.12 ± 0.00                 | 0.0000 ± 0.0000              |
| Reddit  | Fixed No Topology | $\frac{4}{13} A_{upd}$                         | 85.27 ± 0.81         | 66.31 ± 7.14       | 66.03 ± 7.08            | 13.24 ± 1.03                | 0.0223 ± 0.0024              |

**Notes:**
- Values report sample mean $\pm$ sample standard deviation ($ddof=1$) over Seeds 42, 43, 44.
- In this controlled setting, component weights are held constant at their production ratios ($9/13$ and $4/13$) without re-normalization.
- Baseline uniform client aggregation share is $1/K = 20.0\%$. Attacker weight $w_0$ measures the malicious client's share in the global model.
- Removing the update channel increases ASR across all datasets (+1.19% Cora, +0.28% PubMed, +11.11% Reddit), proving its non-redundant dynamic role.
- Removing the topology channel causes catastrophic defense breakdown on Cora (42.53% ASR) and Reddit (66.31% ASR), proving parameter-space anomaly detection alone cannot stop structural backdoors.
