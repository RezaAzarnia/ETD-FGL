# ETD_FGL_PAPER_HANDOFF

Read `ETD_FGL_CODE_AND_CHANGES.md` first (START HERE section), then `FIGURE_MANIFEST.csv`, `MISSING_AND_UNVERIFIED.md`.

* Repo commit: 80a321027b26853eee1c2c4f415e1ec9c1f4961c (branch audit-fix-verification, tag paper-results-v1.0.0); tracked tree clean; this folder and `paper_artifacts/ETDFGL_Figure_Revision_v*` are untracked.
* Old manuscript used for comparison: `../old/main.tex` (NOT `../main.tex`, which is another paper).
* No training/experiments were run. No code, results or manuscript files were modified. All RESULTS are derived from `outputs/**/final_summary.json` + `training_history.csv` by `SCRIPTS/build_results.py`.
* Figures 2–8 were **re-rendered (plot only)** from RESULTS CSVs by `SCRIPTS/make_figures.py` (status REGENERATED_FROM_EXISTING_DATA). Fig 1 was re-rendered from `generate_etdfgl_architecture_figure.py` (outside repo) with two stale labels corrected and is not camera-ready. PNG previews are in `FIGURES/EXTRA/`.
* Regenerate: `python -I SCRIPTS/build_results.py <repo> RESULTS && python -I SCRIPTS/make_figures.py RESULTS FIGURES`.

## Inventory (size, SHA-256) 

| file | bytes | sha256 |
|---|---|---|
| ETD_FGL_CODE_AND_CHANGES.md | 31595 | 57525cb8a6e96bc90b2808c1f9ff1f6a9d5cf09b346fb021251175a5e74f6c75 |
| FIGURE_MANIFEST.csv | 5351 | 470155a391c88ba5479a260f05814b82c6fa5de324b2b166a4a2ca06b41dfd18 |
| FIGURES/accuracy_robustness_tradeoff.pdf | 24975 | c83055ab855cf58c9b6f7f11d2ac9431c8393053cf9e78f7ced1ca55ca4bbd1f |
| FIGURES/attacker_weight_dynamics.pdf | 22242 | adef6f433f19ab4caf7d01efa46a97d5919881f002aac74009ebe99db4513d6a |
| FIGURES/controlled_ablation.pdf | 29131 | c77ff8227b093958b7e3816e0f6d6846a3dbfa828c17c31f031d87ab817447c9 |
| FIGURES/etdfgl_architecture_workflow.pdf | 105366 | 132c77ff2f30be902dbcd1ef6a8a7595d2be3afaf76789d70601c4fd70a111e6 |
| FIGURES/EXTRA/accuracy_robustness_tradeoff_preview.png | 84722 | 529ac65b912826b714e8c7234f371c7a6f2c2bd00c29e7db228c3ecfe4823939 |
| FIGURES/EXTRA/attacker_weight_dynamics_preview.png | 63678 | 8b63713b01a5237ca8b848e22cb24324f8cb488b5176d9978215188fd63bd989 |
| FIGURES/EXTRA/controlled_ablation_preview.png | 101235 | 74bf35ff610e660daa8c9a0720a2cdf48b743eda68fadc163fc3d509e477af8c |
| FIGURES/EXTRA/etdfgl_architecture_workflow_preview.png | 650746 | c9c55153d10a10a33f243f3d1ff1ce62cdc6bffddfa14c9974a0d4cb56b7c2da |
| FIGURES/EXTRA/fig_s03_training_runtime_comparison_preview.png | 32256 | 312657f322fd9228ed7878eca2c245e303099362cc55e71dfff38a694b62aba4 |
| FIGURES/EXTRA/learning_dynamics_rounds_preview.png | 218333 | 5949d98f4d4bb0106889b60a98ee7a4b5de75743756f6b3ba349017080cf17eb |
| FIGURES/EXTRA/multiseed_robustness_preview.png | 80645 | a95e2c7365c76f1142bc18b3848535ef046460db0f39a729b5e5c20dd12fe252 |
| FIGURES/EXTRA/overall_baselines_preview.png | 41482 | fac063a6d16198ff863f490b754ecdfd4849901a3b7aa6caeea1bbd9ef295bb9 |
| FIGURES/fig_s03_training_runtime_comparison.pdf | 18758 | 419780eaad69cef52dde96accfb105f5c5036157d4d2ec1cd1ff8ad92b730bd3 |
| FIGURES/learning_dynamics_rounds.pdf | 28681 | efca1e40d76987d8b8f4aeb3c1b13ba2b552180a26ab4322383e7d41a5d6b8ee |
| FIGURES/multiseed_robustness.pdf | 26068 | 098b1d3f05bd941a62b305623c9c4131091d52ce645f951819deb86d211648e8 |
| FIGURES/overall_baselines.pdf | 19146 | 6b4a408f828177de7614ee2bc3b70dc8d1189f99e71eee61483bce554f53e472 |
| MISSING_AND_UNVERIFIED.md | 2552 | bf71fad1b041c4f38badb672ee2a13da1c370b00bb63043edfa89f7f01d8f606 |
| RESULTS/R01_all_132_runs_raw.csv | 40293 | 3d9331e7f9b34bff8e1b17a9049c4151d0f9d9eaf2d4e7bc75a489589f5f3d2d |
| RESULTS/R02_seed42_baselines_tab_seed42_baselines.csv | 3422 | f24dd655af030c5eca56428a845285642fd7f07c1f0313f2a19e8508492df7fa |
| RESULTS/R03a_multiseed_per_seed.csv | 2999 | 52f7a6f8908b9a0aafe4210908f8a7e54cfc73c2d61a98c12a32c68004d7a7f1 |
| RESULTS/R03b_multiseed_summary_tab_multiseed_robustness.csv | 887 | c2a508e581efacfc02178d902f340529c2638e36352c384b5a9e628ad0c1c889 |
| RESULTS/R04a_standard_ablation_per_seed.csv | 10379 | 1d8af8a20e069d0860471fd953b8590b977e5f4ec87a62748544308eb17a04db |
| RESULTS/R04b_standard_ablation_summary.csv | 2117 | c0883fa0096915f980f210789c96c755f476cca85010b3462f8b90950e1bdb32 |
| RESULTS/R05a_controlled_ablation_per_seed.csv | 8944 | 221f9dff4fdd769686de730e3b961c8fb987e2fb07b4332e5db041b05ff89180 |
| RESULTS/R05b_controlled_ablation_summary_tab_ablation_comparison_tab_attacker_suppression.csv | 1906 | 48b7a62dea1ac30c6801238d3046c5755e4d1e10b06e39478d1a2201c68ce5e8 |
| RESULTS/R06a_paired_differences_per_seed.csv | 1931 | 24c70e9d3d8bf79017342437b12e01f1bc1c9355fbd06760a0c17cc90c8413cb |
| RESULTS/R06b_paired_differences_summary_tab_paired_contributions.csv | 1353 | 804601fe9922c8f6e8d487d11e56986d89414b7b2a350517e45ec3fdd4dc42c7 |
| RESULTS/R07_round_trajectories_seed42_baselines.csv | 58981 | 739682705e364243ff1a22bb1ada256a0d35b23b1610fcc0b668dcae956cbda4 |
| RESULTS/R08_attacker_weight_trajectories_seed42_controlled.csv | 39515 | 75dc8f15d9b0f80e70f95edac7ef1cddac388d2d9f8cdd8dd0481f5344c55a87 |
| RESULTS/R09_round_trajectories_multiseed_all_seeds.csv | 38725 | 7ee70a13d2f30144f585bc1892f2e403525c1bdd7b48a85ae7b60c73f14cafbe |
| RESULTS/R10_early_round_asr_check.csv | 2004 | d251b4bf634a039ead74fc6969a7fc466d82615ad5bdd8dddad3acf38a0d6403 |
| RESULTS/R11_runtime_same_method_across_suites.csv | 2493 | dbe6b35e322642c7b695eda2bc5bf8af219b04c27fb0fc12db1f9aba2c4488c9 |
| RESULTS/R12_dataset_partition_attack_metadata.csv | 2093 | f2f44a40224a7890e0a755363a22c8b0e901ef5b0e9a8a2f054851cf9a934f44 |
| RESULTS/R13_old_manuscript_vs_verified.csv | 4852 | e42f8c25e793759bd96da7b7ce67e63e4b741b7a6b5784f9694889228182cde3 |
| SCRIPTS/arch_corrected.py | 15681 | 81fbc25681bc2a0222e26320915c774e977a9296100d612f232a14d160e3a166 |
| SCRIPTS/build_results.py | 15860 | c934d959f535ecbef9be9f400787a927ac3143ac3d592762915efd7b1f6ed9f6 |
| SCRIPTS/make_figures.py | 9745 | b528ca0dc680fe57cbb80fa22d05886016de0b57bb78f4bc496ec77b5622db5e |
