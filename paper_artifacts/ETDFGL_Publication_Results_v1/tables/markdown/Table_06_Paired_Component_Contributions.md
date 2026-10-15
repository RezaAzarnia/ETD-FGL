### Paired Within-Seed Component Contributions ($\Delta = \text{Variant} - \text{Full ETD-FGL}$)

| Dataset | Ablated Component                                      | Paired Seeds | $\Delta$ Clean Acc (% pts) | $\Delta$ Backdoor ASR (% pts) | $\Delta$ Attack Effect (% pts) | $\Delta$ Attacker Weight (% pts) | $\Delta$ Benign Risk |
| ------- | ------------------------------------------------------ | ------------ | -------------------------- | ----------------------------- | ------------------------------ | -------------------------------- | -------------------- |
| Cora    | Without Model Update Channel ($-\frac{4}{13} A_{upd}$) | 3            | 0.30 ± 1.28                | 1.19 ± 1.42                   | 0.34 ± 0.91                    | -0.64 ± 0.03                     | -0.0577 ± 0.0007     |
| Cora    | Without Topology Channel ($-\frac{9}{13} A_{topo}$)    | 3            | 0.53 ± 1.17                | 37.32 ± 15.35                 | 37.32 ± 15.92                  | 13.66 ± 0.58                     | 0.0033 ± 0.0027      |
| PubMed  | Without Model Update Channel ($-\frac{4}{13} A_{upd}$) | 3            | -0.93 ± 1.27               | 0.28 ± 0.19                   | -0.37 ± 0.21                   | -0.44 ± 0.04                     | -0.0487 ± 0.0054     |
| PubMed  | Without Topology Channel ($-\frac{9}{13} A_{topo}$)    | 3            | 0.20 ± 2.10                | 3.58 ± 3.07                   | 1.87 ± 3.78                    | 11.21 ± 0.56                     | -0.0206 ± 0.0082     |
| Reddit  | Without Model Update Channel ($-\frac{4}{13} A_{upd}$) | 3            | 0.13 ± 0.83                | 11.11 ± 5.60                  | 11.15 ± 5.57                   | 1.59 ± 0.08                      | -0.0203 ± 0.0012     |
| Reddit  | Without Topology Channel ($-\frac{9}{13} A_{topo}$)    | 3            | 0.40 ± 0.50                | 52.23 ± 14.61                 | 52.26 ± 14.45                  | 10.71 ± 1.02                     | 0.0020 ± 0.0018      |

**Notes:**
- Statistics report sample mean $\pm$ sample standard deviation of paired differences ($d_i = x_{i,\text{variant}} - x_{i,\text{full}}$) across matched seeds (42, 43, 44).
- A positive $\Delta$ ASR indicates that removing the channel increases backdoor vulnerability (i.e., the channel provides essential protection).
- Removing the update channel leads to a $+11.11 \pm 5.60$ percentage point surge in ASR on Reddit, while removing topology leads to $+37.32 \pm 15.35$ pts on Cora and $+52.23 \pm 14.61$ pts on Reddit.
