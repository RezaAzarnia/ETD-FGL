# Old vs current implementation

**There is no evidence of a substantial rewrite.** Git has 3 commits (05f070a → 953e250 → 80a3210); no other branch, stash, dangling algorithm code, or archive holds a different defense. The "old manuscript" (`../old/main.tex`, Oct 17) already described the 80a3210 results. What differs is mostly *documentation vs. code truth*. `../main.tex` is an unrelated IoT paper; `new version.zip` (Oct 9) is a manuscript bundle with no source and a typed 5-seed summary — not used as evidence.

## A. Verified code history (Git)
| Item | 05f070a (baseline) | 953e250 | 80a3210 | Revision branch (3084163) |
|---|---|---|---|---|
| Descriptor | 6-D incl. label-dependent homophily (reads `y`, `train_mask`) | **5-D label-free** (homophily only in a diagnostic function) | same | same |
| Fusion constants | 9/13, 4/13, β=3, floor 0.02 (production aggregator) | same + metadata constants | same | same |
| Fail-closed overwrite, manifests, partition-cache validation, aggregator dispatch, strict FedTGE input validation, controlled-ablation module | – | – | added | same |
| DMGNN edge-removal counts | not recorded | – | printed only | **persisted in run metadata (new runs)** |
| Runtime environment / timing scope | not recorded | – | not recorded | **recorded (new runs)** |

No algorithm, protocol, or stored metric changed after 953e250 other than documentation/infrastructure.

## B. Old manuscript text vs code truth
| Old manuscript statement | Code/result truth | Action |
|---|---|---|
| Fig. 1: attacker weight ≤4.7 %, benign trust ≥85 %, ASR <5 % (Cora), dense clique trigger on *test* nodes, "pairwise" drift | means 4.76/4.55/2.53 %; benign mean trust 0.86–0.95 (min 0.46); Cora ASR 5.21±0.88; trigger injected on poisoned *training* victims (test triggers only for evaluation); drift is client-vs-own-reference | redraw (new Fig. 1 provided) |
| s_j = max(Std, 1e-8) | s_j = population std, replaced by **1.0** if <1e-8 | fix equation |
| MAD with Std as "fallback" | `max(1.4826·MAD, std, 1e-8)` | fix |
| "labels of triggered training nodes reassigned" | victim labels → 0; trigger nodes labelled 0 but outside the train mask | clarify |
| DMGNN uses GNNExplainer saliency | leave-one-edge-out probability-drop heuristic | fix |
| Reddit seed-43 community-overlap explanation | contradicted/unsupported | delete |
| ASR <5 % from round 1 | false (Cora 75.4 %, PubMed 99.9 %) | delete |
| Within 0.5 % of unattacked FedAvg | seed 42: +0.00/+1.30/−0.90 pp; no multi-seed control | restate |
| <5 ms aggregation overhead | never measured | delete |
| Paired ΔClean-Acc ± (0.56, 1.63, …) | 1.28/1.17/1.27/2.10/0.83/0.50 | replace |
| "Best Round" column of seed-42 table | 16 of 24 entries differ from raw `best_round` | replace or drop |
| ETD-FGL faster than FedAvg on Reddit | timing artifact | delete |
| Tables of ASR/accuracy/effect/means/SD | reproduce exactly | keep |
