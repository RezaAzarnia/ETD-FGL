### Client Risk and Attacker Aggregation Weight Dynamics Under Controlled Defense Variants

| Dataset | Configuration     | Attacker Weight ($w_0$ %) ↓ | Attacker Risk ($R_{attacker}$) ↑ | Benign Risk ($R_{benign}$) ↓ | Trust Discrimination Ratio ($w_{benign} / w_0$) ↑ |
| ------- | ----------------- | --------------------------- | -------------------------------- | ---------------------------- | ------------------------------------------------- |
| Cora    | Full ETD-FGL      | 4.76 ± 0.03                 | Recorded in History              | 0.0577 ± 0.0007              | 5.00x                                             |
| Cora    | Fixed No Update   | 4.12 ± 0.00                 | Recorded in History              | 0.0000 ± 0.0000              | 5.82x                                             |
| Cora    | Fixed No Topology | 18.41 ± 0.60                | Recorded in History              | 0.0610 ± 0.0032              | 1.11x                                             |
| PubMed  | Full ETD-FGL      | 4.55 ± 0.04                 | Recorded in History              | 0.0487 ± 0.0054              | 5.24x                                             |
| PubMed  | Fixed No Update   | 4.12 ± 0.00                 | Recorded in History              | 0.0000 ± 0.0000              | 5.82x                                             |
| PubMed  | Fixed No Topology | 15.76 ± 0.59                | Recorded in History              | 0.0281 ± 0.0058              | 1.34x                                             |
| Reddit  | Full ETD-FGL      | 2.53 ± 0.08                 | Recorded in History              | 0.0203 ± 0.0012              | 9.63x                                             |
| Reddit  | Fixed No Update   | 4.12 ± 0.00                 | Recorded in History              | 0.0000 ± 0.0000              | 5.82x                                             |
| Reddit  | Fixed No Topology | 13.24 ± 1.03                | Recorded in History              | 0.0223 ± 0.0024              | 1.64x                                             |

**Notes:**
- Uniform aggregation weight baseline without defense is $w_k = 20.0\%$ per client ($1/K$).
- Trust Discrimination Ratio represents the average benign client weight divided by the attacker weight ($w_{benign}/w_0$).
- In Full ETD-FGL, benign clients receive $5.0\times$ to $9.6\times$ greater aggregation weight than the malicious client.
- Without the topology channel, the discrimination ratio collapses to $1.1\times - 1.6\times$, explaining why parameter defense alone fails.
