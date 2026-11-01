# ETD_FGL_NEW_CODE_HANDOFF

Purpose: let an author rewrite the ETD-FGL manuscript from scratch, strictly from verified code and raw results.
Read in this order: `SCIENTIFIC_REVISION_AUDIT.md` (verdict + traceability) -> `ETD_FGL_COMPLETE_CODE_TRUTH.md` -> `EQUATIONS_AND_PSEUDOCODE.md` -> `RESULTS_AND_STATISTICS.md` -> `CLAIMS_EVIDENCE_MATRIX.md` -> `MANUSCRIPT_REWRITE_BLUEPRINT.md`; supporting: `OLD_VS_CURRENT_IMPLEMENTATION.md`, `GIT_CHANGES_AND_TESTS.md`, `FIGURE_MANIFEST.md`, `TABLES/`, `FIGURES/`.

Key facts: authoritative code = commit 80a321027b26853eee1c2c4f415e1ec9c1f4961c; revision branch `revision-audit-2026-11` HEAD 3084163031c9e535eedf044ab555c9e26fbd45d7 (3 non-algorithmic commits). No rewritten implementation exists; no formal referee letter exists (formal compliance cannot be verified). Seeds 45/46 and the "new version.zip" 5-seed summary are NOT verified evidence. The earlier package `ETD_FGL_PAPER_HANDOFF` is superseded (it described the seed-42 table as fully unchanged; the "Best Round" column does not reproduce).
Rules: use only claims marked "yes" in the claims matrix; never turn n=3 differences into significance statements; do not reuse old figures or old prose that conflicts with the code.
Regeneration: `python -I tools/raw_recompute/recompute_tables_from_raw.py <repo> TABLES` and `render_figures_from_tables.py` (in the repo branch); Fig. 1: `SCRIPTS/fig1_architecture_current.py`.

## Inventory (bytes, SHA-256)
| file | bytes | sha256 |
|---|---|---|
| CLAIMS_EVIDENCE_MATRIX.md | 4767 | c95c7717057ec26200486bd7ac34e06e0459f371f4f254b2ecc9d55452558986 |
| EQUATIONS_AND_PSEUDOCODE.md | 3037 | dcb4686c223de2cc7626803a90125ae3ed3c4632a0ac63253b871a97169a6494 |
| ETD_FGL_COMPLETE_CODE_TRUTH.md | 10764 | 75ac5d6a853d6af123709cf30979166fafd16b1c1e4acc4727586f33d9791579 |
| FIGURE_MANIFEST.md | 2460 | 33f0732d2d9c7aa940cd86ba9aa25bc0491ba896d20df1daac9d77df41d5e5b0 |
| FIGURES/accuracy_robustness_tradeoff.pdf | 24975 | 4247adc34ece4bfe5023042b5665e784a3605e1fed25a456d58ffacb9206708a |
| FIGURES/attacker_weight_dynamics.pdf | 22242 | f3e8a03fc181b30eec3d524e2e64a9ee344de13337999458302ae3bcf28cc55c |
| FIGURES/controlled_ablation.pdf | 29131 | 7b4d3e177123e9b2174d2f6a0797f249b2fe593f53ddfd47da2d7892d85fbd33 |
| FIGURES/etdfgl_architecture_workflow.pdf | 38217 | 8481b6ca1e6becacc527b6bf22bb51723d8c824b759d3303ed2a1fe3f90599de |
| FIGURES/EXTRA/accuracy_robustness_tradeoff_preview.png | 84722 | 529ac65b912826b714e8c7234f371c7a6f2c2bd00c29e7db228c3ecfe4823939 |
| FIGURES/EXTRA/attacker_weight_dynamics_preview.png | 63678 | 8b63713b01a5237ca8b848e22cb24324f8cb488b5176d9978215188fd63bd989 |
| FIGURES/EXTRA/controlled_ablation_preview.png | 101235 | 74bf35ff610e660daa8c9a0720a2cdf48b743eda68fadc163fc3d509e477af8c |
| FIGURES/EXTRA/etdfgl_architecture_workflow_preview.png | 145360 | 06f8779738b044628b0355d2d0e7f4ab22f5aa683eefb7d72efba406f2fd8e68 |
| FIGURES/EXTRA/fig_s03_training_runtime_comparison_preview.png | 32256 | 312657f322fd9228ed7878eca2c245e303099362cc55e71dfff38a694b62aba4 |
| FIGURES/EXTRA/learning_dynamics_rounds_preview.png | 218333 | 5949d98f4d4bb0106889b60a98ee7a4b5de75743756f6b3ba349017080cf17eb |
| FIGURES/EXTRA/multiseed_robustness_preview.png | 80645 | a95e2c7365c76f1142bc18b3848535ef046460db0f39a729b5e5c20dd12fe252 |
| FIGURES/EXTRA/overall_baselines_preview.png | 41482 | fac063a6d16198ff863f490b754ecdfd4849901a3b7aa6caeea1bbd9ef295bb9 |
| FIGURES/fig_s03_training_runtime_comparison.pdf | 18758 | 7f26df9e663cb8d824117cfa9d1590442c8270d2a4813d097cf7b259b77e92da |
| FIGURES/learning_dynamics_rounds.pdf | 28681 | 8ee45a9786b79adbb26a0822c1064cd7695d1a9abb4c128e4ad8a6da4c98f07e |
| FIGURES/multiseed_robustness.pdf | 26068 | a4da74af84a8606857ceca310ba92495669af7eccb00151c0db84f3650524b98 |
| FIGURES/overall_baselines.pdf | 19146 | a52b916d6553910e196e28dae102728b598c8a98016a5f425a789b66c890cdfc |
| GIT_CHANGES_AND_TESTS.md | 2481 | aef032d848bbab3480025653170df9a710d0bb362951c428e4bef4952771918a |
| MANUSCRIPT_REWRITE_BLUEPRINT.md | 4724 | 272f0d98fc58b71bc8137ef80cec4d3d134a95a6e771aae154adc84e5450e1cd |
| OLD_VS_CURRENT_IMPLEMENTATION.md | 2945 | e9e6eb4cf45328cf67a83d8f630069bc784db628a06c94b6febffcf5caa56a36 |
| RESULTS_AND_STATISTICS.md | 6960 | 056cfa3b99bb90b1ef39dae2c44d58e3ba3d80439224dd8ea34500aaf13f9e1b |
| SCIENTIFIC_REVISION_AUDIT.md | 11807 | 8e9a84dd6c76ca73e24ffa9a201b2f093e5e78d21f62fe78e68e16a19db0dd86 |
| SCRIPTS/fig1_architecture_current.py | 3174 | 3a53eb346b71022bb76c2563711d76803e245c411451dd0bcff58510429c7f02 |
| TABLES/R01_all_132_runs_raw.csv | 40293 | 3d9331e7f9b34bff8e1b17a9049c4151d0f9d9eaf2d4e7bc75a489589f5f3d2d |
| TABLES/R02_seed42_baselines_tab_seed42_baselines.csv | 3513 | c9fc557a090f1b35679fcc3a191f074a8d7b23027ff8886ba22b13362c614897 |
| TABLES/R03a_multiseed_per_seed.csv | 2999 | 52f7a6f8908b9a0aafe4210908f8a7e54cfc73c2d61a98c12a32c68004d7a7f1 |
| TABLES/R03b_multiseed_summary_tab_multiseed_robustness.csv | 887 | c2a508e581efacfc02178d902f340529c2638e36352c384b5a9e628ad0c1c889 |
| TABLES/R04a_standard_ablation_per_seed.csv | 10379 | 1d8af8a20e069d0860471fd953b8590b977e5f4ec87a62748544308eb17a04db |
| TABLES/R04b_standard_ablation_summary.csv | 2117 | c0883fa0096915f980f210789c96c755f476cca85010b3462f8b90950e1bdb32 |
| TABLES/R05a_controlled_ablation_per_seed.csv | 8944 | 221f9dff4fdd769686de730e3b961c8fb987e2fb07b4332e5db041b05ff89180 |
| TABLES/R05b_controlled_ablation_summary_tab_ablation_comparison_tab_attacker_suppression.csv | 1906 | 48b7a62dea1ac30c6801238d3046c5755e4d1e10b06e39478d1a2201c68ce5e8 |
| TABLES/R06a_paired_differences_per_seed.csv | 1931 | 24c70e9d3d8bf79017342437b12e01f1bc1c9355fbd06760a0c17cc90c8413cb |
| TABLES/R06b_paired_differences_summary_tab_paired_contributions.csv | 1353 | 804601fe9922c8f6e8d487d11e56986d89414b7b2a350517e45ec3fdd4dc42c7 |
| TABLES/R07_round_trajectories_seed42_baselines.csv | 58981 | 739682705e364243ff1a22bb1ada256a0d35b23b1610fcc0b668dcae956cbda4 |
| TABLES/R08_attacker_weight_trajectories_seed42_controlled.csv | 39515 | 75dc8f15d9b0f80e70f95edac7ef1cddac388d2d9f8cdd8dd0481f5344c55a87 |
| TABLES/R09_round_trajectories_multiseed_all_seeds.csv | 38725 | 7ee70a13d2f30144f585bc1892f2e403525c1bdd7b48a85ae7b60c73f14cafbe |
| TABLES/R10_early_round_asr_check.csv | 2004 | d251b4bf634a039ead74fc6969a7fc466d82615ad5bdd8dddad3acf38a0d6403 |
| TABLES/R11_runtime_same_method_across_suites.csv | 2493 | dbe6b35e322642c7b695eda2bc5bf8af219b04c27fb0fc12db1f9aba2c4488c9 |
| TABLES/R12_dataset_partition_attack_metadata.csv | 2093 | f2f44a40224a7890e0a755363a22c8b0e901ef5b0e9a8a2f054851cf9a934f44 |
| TABLES/R13_old_manuscript_vs_verified.csv | 5154 | b9e27c8e94d4cd45555bc982ad7bca55b0f75269c307870d0f6a1e2f3eb10c66 |
| TABLES/T14_topology_and_update_risk_audit.csv | 10557 | 9c59364c166b0d68aa5f0306a529247a062a82ce689146035e0241072484f0f5 |
