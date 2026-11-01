# Pre-writing scientific gate

Repository state audited: local `master` @ `a1ac03b6c295a72d326249e727d8b501a02f8cd6` (code identical in behaviour to `80a321027b26853eee1c2c4f415e1ec9c1f4961c` plus two provenance fixes). Date: 2026-11-01.

**FORMAL REFEREE COMPLIANCE = NOT VERIFIABLE.** No authentic referee/editor letter exists in the repository, `Downloads`, `Desktop` or the parent folder (filename search for referee/reviewer/decision/response-to-review: no hits). `audit/SCIENTIFIC_REVIEW.md` is an internal audit; the InsightAI HDQL-GTE report concerns another paper. Everything below is an independent technical audit, not reviewer compliance.

**Software tests pass (88 / 88, CPU) ≠ scientific revision satisfied.** Tests show the code does what it says; they do not validate the claims.

## 1. Repository check (A1)
HEAD/branches/reflog re-inspected before integration: single worktree, no stashes, `master` = `origin/master` = `953e250`, revision branch +3 commits, `origin` unchanged (`git ls-remote` returned `953e250`). No code difference between the working tree and the branch other than untracked user files (untouched). No newly appeared referee letter.

## 2. CODE VERIFIED (line-level; `multidata_suite/…` at master)
| Item | Evidence | Status |
|---|---|---|
| 5-D label-free descriptor | `defenses.py:344-393` reads only the edge list; tests `test_production_descriptor_strict_label_independence/_mask_independence` | PASS |
| Drift scale = population std, floor→1.0 | `defenses.py:530-534` | PASS |
| `max(1.4826·MAD, std, 1e-8)` one-sided map | `defenses.py:450-454` | PASS |
| Update anomaly: coordinate-wise median, L2 | `defenses.py:550-554` | PASS |
| 9/13, 4/13 fusion; `clip(exp(-3R),0.02,1)`; weights ∝ n_i·T_i | `defenses.py:555-567`; logged R,T reproduce the formula to 2·10⁻¹⁶ (9 multi-seed runs) | PASS |
| Checkpoint = best clean validation accuracy (strict >) | `core.py:554`; ASR/test unused for selection | PASS |
| Poisoning: train-node victims, label → 0, K3 trigger, 16-feature vector; evaluation triggers on all non-target test nodes simultaneously | `attack.py:91-250,257-`, `core.py:114-127` | PASS (disclose simultaneous evaluation) |
| Raw tables reproduce | recomputation from 132 runs matches committed CSVs (<5·10⁻⁵) | PASS |

## 3. SCIENTIFIC LIMITATIONS STILL OPEN
| # | Limitation | Evidence | Status |
|---|---|---|---|
| L1 | Server uses exact clean AND attacked graphs | `ETDFGLAggregator.__init__`; pipeline | OPEN (design) |
| L2 | Topology anomaly degenerate: attacker 0.848284, benign 0, in all 84 ETD-type runs | `TABLES/T14` | OPEN (measured; weakness) |
| L3 | Label-aware partition over train/val/test; induced-subgraph training vs full-graph evaluation; server-side validation set | `data.py:247-287`, `core.py:114-127` | OPEN (disclose; label-blind protocol = new experiments) |
| L4 | Baselines are untuned adaptations with information asymmetry (ETD-FGL, PD-FL calibration use clean reference; DMGNN reuses an attacked run) | `defenses.py:89-288` | OPEN |
| L5 | One static non-adaptive attacker, IID only, seeds 42-44 only, 2-layer GCN | configs; `outputs/` | OPEN |
| L6 | No significance evidence (n=3); Cora remove-update effect includes a 0.00 seed | `R06b` | OPEN |
| L7 | Runtime not comparable (same run 44.6/18.7/50.7 s; hardware unrecorded for stored runs) | `R11` | OPEN (future runs now record environment) |
| L8 | Reddit seed 43 (34.82 %) unexplained | `R03a`, `T14` | OPEN |
| L9 | Seeds 45/46, 5-seed bootstrap bundle: no raw data | filesystem | UNVERIFIABLE |

## 4. OLD CLAIMS TO REMOVE (all verified false/unsupported; see `TABLES/R13`)
"<5 % ASR from round 1" (round-1 ASR 75.4 % Cora, 99.9 % PubMed; Cora re-spikes 40.5 %/36.1 % at rounds 6/12) · community-overlap cause of Reddit seed 43 (attacker A_topo identical across seeds) · "within 0.5 pp of Clean FedAvg" (+1.30 PubMed, seed 42 only) · "≤4.7 %" attacker share (means 4.76/4.55/2.53 %; per-round max 5.38 %) · DMGNN-FL "uses GNNExplainer" · "<5 ms overhead" · ETD-FGL faster than FedAvg · "near-total elimination" / unsupported robustness, generality, real-world or privacy claims · paired ΔAcc SDs and "Best Round" column of the old tables.

## 5. Correctable software defects vs design changes
| Item | Class | Action |
|---|---|---|
| Runtime/device/version provenance missing | software defect (non-semantic) | FIXED `28340f8` (new runs only) |
| DMGNN-FL pruning counts only printed | software defect (non-semantic) | FIXED `7a1cc1f` (new runs only; old runs still lack counts) |
| Old manuscript table errors (ΔAcc SD, Best Round) | manuscript errors, no code defect | repo CSVs were correct |
| Reference-free topology, label-blind partition, non-IID, M≥2, adaptive attacks, controlled timing, more seeds | design/experiment changes | NOT done; would need reruns and would create new result sets — see `OPEN_SCIENTIFIC_ITEMS.md` |
No other verified non-semantic defect was found, so no further code commits were made. A limitation is not "fixed" by disclosure.

## 6. Compact status
| Gate item | Status |
|---|---|
| Code faithful to its documented/implemented algorithm | PASS |
| Stored results reproducible from raw files | PASS |
| Formal referee compliance | NOT VERIFIABLE |
| Strong robustness / generality claims | FAIL (unsupported) |
| Descriptive paper with limitations in main text | OPEN-but-feasible |
| Runtime claims | FAIL (do not use) |
| Statistical significance claims | FAIL (none exist) |
| Privacy / deployability claims | FAIL (not implemented) |
