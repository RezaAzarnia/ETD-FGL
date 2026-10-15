### Multi-Seed Robustness Evaluation: Attacked FedAvg vs. ETD-FGL (Seeds 42, 43, 44)

| Dataset | Method          | Seeds Evaluated | Clean Accuracy (%) ↑ | Backdoor ASR (%) ↓ | Attack Effect (% pts) ↓ | Training Runtime (s) |
| ------- | --------------- | --------------- | -------------------- | ------------------ | ----------------------- | -------------------- |
| Cora    | Attacked FedAvg | 3               | 75.00 ± 0.72         | 62.03 ± 15.38      | 52.26 ± 14.25           | 2.73 ± 0.04          |
| Cora    | ETD-FGL         | 3               | 75.57 ± 1.57         | 5.21 ± 0.88        | -2.22 ± 2.17            | 2.85 ± 0.01          |
| PubMed  | Attacked FedAvg | 3               | 74.80 ± 3.18         | 9.23 ± 7.36        | 2.56 ± 7.73             | 9.44 ± 3.13          |
| PubMed  | ETD-FGL         | 3               | 75.50 ± 2.01         | 0.89 ± 0.56        | -3.54 ± 0.53            | 10.53 ± 3.64         |
| Reddit  | Attacked FedAvg | 3               | 84.90 ± 0.80         | 74.42 ± 1.85       | 74.06 ± 1.75            | 11.07 ± 6.58         |
| Reddit  | ETD-FGL         | 3               | 84.87 ± 0.40         | 14.08 ± 18.19      | 13.77 ± 18.09           | 7.40 ± 0.05          |

**Notes:**
- Values report sample mean $\pm$ sample standard deviation ($ddof=1$) over three independent runs (Seeds 42, 43, 44).
- Reddit ETD-FGL variance: Seed 42 achieved 0.85% ASR and Seed 44 achieved 6.58% ASR, while Seed 43 exhibited an outlier ASR of 34.82% due to community partition overlap.
- Even under outlier Seed 43, ETD-FGL reduces ASR by more than 39 percentage points compared to Attacked FedAvg (74.42%).
