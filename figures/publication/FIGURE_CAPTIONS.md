# Figure caption support (for later manuscript use; figures themselves carry no explanatory prose)

**Fig. 1.** ETD-FGL as implemented in the simulation (K = 5, one malicious client, IID partition). Both evidence channels receive information from all five clients: current client graphs G_i feed a static topology profile computed once, and per-round updates u_i feed a median-distance analysis. The topology profile compares each G_i with a clean reference G_i^0, which is a simulation assumption (the server has exact clean graphs). Both scores pass through the same one-sided robust map R, are fused as 9/13 and 4/13, converted to trust, and used for sample-weighted aggregation. The malicious client attaches a K3 clique to each victim training node and relabels it to the target class. The checkpoint is chosen by clean validation accuracy.

**Fig. 2.** Seed-42 comparison of eight methods (single run per bar, no uncertainty). (a) Backdoor ASR, lower is better. (b) Clean test accuracy, higher is better. * Adapted re-implementations, not exact reproductions of the original methods.

**Fig. 4.** Seeds 42, 43, 44 for Attacked FedAvg and ETD-FGL. Dots: individual seeds; bar: mean; whiskers: sample SD (ddof = 1, n = 3). Reddit seed 43 (ASR 34.82 %) is marked; no cause has been established. Accuracy axes are zoomed and differ per panel. No significance test was performed.

**Fig. 5.** Seed 42, all 50 rounds, unsmoothed, global-model evaluation each round. (b) ETD-FGL ASR in round 1 is 75.4 % (Cora) and 99.9 % (PubMed), i.e. the attack is not suppressed from round 1; Cora shows further spikes in rounds 6 and 12. Reported table values use the best clean-validation round, not round 50.

**Fig. 6.** Fixed-coefficient ablation (coefficients not renormalised): Full (9/13, 4/13), no update (9/13, 0), no topology (0, 4/13); three paired seeds. (a) ASR per variant, grey lines join the same seed. (b) Paired change in ASR relative to Full, in percentage points; bars/whiskers: mean ± sample SD (ddof = 1). No statistical test was run. Results hold for the tested setting (one static attacker, IID, K3 trigger).

**Fig. 7.** Attacker aggregation weight per round, seed 42. Raw traces are drawn; the thick orange line is a 5-round moving average of the no-topology trace (visual aid only). The dotted line is the uniform 20 % share. Lower attacker weight is not by itself evidence of lower ASR (e.g. Reddit seed 43; see Fig. 4). The no-update variant is constant at 4.12 % by construction (saturated topology score).

**Fig. S1 (supplementary, exploratory).** Single-run wall-clock times; hardware not recorded for the stored runs, the same Attacked FedAvg Reddit seed-42 run was timed 18.7 to 50.7 s in different suites. Not evidence of overhead or speed advantage.

**Fig. S2 (supplementary).** Seed-42 accuracy versus ASR per dataset (open markers) with 3-seed mean ± sample SD for Attacked FedAvg and ETD-FGL (filled). Adds little beyond Figs 2 and 4; no cross-dataset frontier is claimed.
