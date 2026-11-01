# Manuscript rewrite blueprint (foundation only — not a draft)

Write from `ETD_FGL_COMPLETE_CODE_TRUTH.md`, `EQUATIONS_AND_PSEUDOCODE.md`, `RESULTS_AND_STATISTICS.md`; every number must carry a claim ID from `CLAIMS_EVIDENCE_MATRIX.md`. Do not reuse old manuscript prose that conflicts with the code. Tone: descriptive, with limitations in the main text, not hidden in an appendix.

**Title options (honest scope).** (1) "ETD-FGL: Reference-Anchored Topology and Update Evidence for Trust-Weighted Aggregation in Federated Graph Learning under Structural Backdoors". (2) "Topology-Drift and Update-Anomaly Trust Weighting against Clique Backdoors in Federated Graph Learning: A Controlled Study". Avoid "Evidence-Based"/"elimination" wording. If the reference assumption stays, say "reference-anchored".

## Section plan (KEEP / REPLACE / DELETE / ADD)
| Section | Content to write | Evidence | KEEP | REPLACE/DELETE | ADD |
|---|---|---|---|---|---|
| Abstract | problem; method in 2 sentences; setting (K=5, M=1 clique, 20 %, IID, 3 seeds); main numbers C08, C15; honest limits (Reddit seed 43, reference assumption, degenerate topology evidence) | C08,C09,C12,C15,C06 | headline ASR numbers | "within 0.5 %", "near-total elimination", "community overlap", "vital stabilization" | explicit one-sentence limitation |
| Introduction | FGL, structural backdoors, gap: parameter-space defenses vs topology evidence; contributions: (i) reference-anchored topology + update trust weighting, (ii) controlled-coefficient ablation, (iii) honest multi-dataset evaluation with failure cases | C01,C18 | motivation | claims of novelty for median/MAD/exp trust | statement that the topology channel is binary here |
| Related work | FGL; graph backdoors; Byzantine/robust FL; graph purification; compare to the five baselines as *adapted* | C29 | citations in old bib (verify) | "GNNExplainer" for DMGNN-FL | fairness note on information asymmetry |
| Threat model & assumptions | M=1/K=5, static, label-flip + K3 + 16 features; server capabilities; reference graph = simulation assumption; no privacy claim | Truth §2 | – | privacy/secure-aggregation implications | "oracle reference" explicit |
| Method | descriptor; drift; robust map; update anomaly; fusion/trust/aggregation; pseudocode; degenerate identity (z₀=2.5, 0.848284) | C01–C07 | equations (corrected s_j, max-MAD) | old eq. for s_j | Algorithm box; complexity statement without timings |
| Experimental setup | datasets/splits, partition (label-aware IID), training, metrics with denominators, seeds, checkpoint rule, baselines as implemented, ablation definitions, hardware = unrecorded | Truth §3–7 | hyperparameter table | Reddit/other fabricated details | victim counts; per-client sizes |
| Results | Table 1 seed-42 (single run); Table 2 multi-seed with per-seed ASR; trajectories; standard vs controlled ablation; paired ΔASR with per-seed values; attacker share and benign trust; baseline failure modes | R02–R08 | all numeric tables except Best-Round/ΔAcc SD | Pareto, round-1 claim | seed-wise reporting; "no tests were run" sentence |
| Discussion | what the data support: topology signal drives suppression; update channel helps on Reddit; seed-43 residual unexplained; PubMed weak attack; Fixed-No-Update saturation; why standard ablation misleads | C06–C18 | – | causal stories | alternatives (hypotheses labelled) |
| Limitations | reference graph; M=1; static non-adaptive; IID label-aware; full-graph evaluation; centralized validation; n=3; adapted baselines; runtime; no privacy | Audit table | old items 1–5 | – | the rest |
| Conclusion | measured results + future work (reference-free drift, non-IID, M≥2, adaptive attacks, ≥10 seeds, controlled timing) | – | – | "near-total elimination", ≤4.7 % | – |
| Code/data availability | repo commit `80a3210` (+ revision branch), raw summaries/histories to be archived (outputs/ is git-ignored) | Audit #27 | – | – | hashes |

## Tables / figures placement
T1 setup (datasets, victims, splits); T2 seed-42 baselines (single seed); T3 multi-seed with per-seed ASR; T4 standard vs controlled ablation (separate blocks); T5 paired differences (+ per-seed); T6 attacker share/benign trust; optional supplement: runtime (caveated). Figures: Fig 1 architecture (new), Fig 2 baselines, Fig 3 per-dataset trade-off, Fig 4 multi-seed, Fig 5 trajectories, Fig 6 controlled ablation, Fig 7 attacker weight; Fig 8 runtime → supplement.

## Pre-submission requirements (cannot be solved by writing)
Raw summaries archived; hardware statement or controlled re-timing; decide about the reference-graph assumption; ideally ≥10 seeds and non-IID/M≥2 before any strong claim.
