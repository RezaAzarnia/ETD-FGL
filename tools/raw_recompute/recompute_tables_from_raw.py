"""Read-only derivation of handoff RESULTS/ tables from raw outputs/ files.
python -I build_results.py <repo_root> <results_out_dir>
All numbers come directly from outputs/**/final_summary.json and training_history.csv.
"""
import csv, json, sys, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

repo = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
DS = ["Cora", "PubMed", "Reddit"]

# ---------------------------------------------------------------- raw per-run table
recs = []
hist_cache = {}
for sp in sorted(repo.glob("outputs/**/final_summary.json")):
    s = json.loads(sp.read_text(encoding="utf-8"))
    parts = sp.relative_to(repo / "outputs").parts
    if parts[0] == "final_multidataset":
        suite, slug = "baseline_seed42", parts[2]
    else:
        suite, slug = parts[1], parts[4]
    fm = s["final_metrics"]
    h = pd.read_csv(sp.parent / "training_history.csv")
    key = (suite, s["dataset"], s["config"]["seed"], slug)
    hist_cache[key] = h
    w0 = h["etdfgl_weight_client_0"] if "etdfgl_weight_client_0" in h else None
    ben_risk = None; ben_trust_min = None; ben_trust_mean = None
    if w0 is not None:
        ben_risk = float(np.mean([h[f"etdfgl_fused_risk_client_{i}"].mean() for i in range(1, 5)]))
        bt = np.stack([h[f"etdfgl_trust_client_{i}"].values for i in range(1, 5)])
        ben_trust_min = float(bt.min()); ben_trust_mean = float(bt.mean())
    recs.append(dict(
        suite=suite, dataset=s["dataset"], seed=s["config"]["seed"], slug=slug, method_label=s["method"],
        best_round=s["best_round"], rounds_logged=len(h),
        clean_accuracy_pct=100 * fm["test_accuracy"], validation_accuracy_pct=100 * fm["validation_accuracy"],
        clean_target_rate_pct=100 * fm["clean_target_rate"], asr_pct=100 * fm["attack_success_rate"],
        attack_effect_pp=100 * fm["attack_effect"], active_loop_seconds=s["elapsed_seconds"],
        attacker_weight_mean_over_50_rounds_pct=(100 * w0.mean()) if w0 is not None else np.nan,
        attacker_weight_final_round_pct=(100 * w0.iloc[-1]) if w0 is not None else np.nan,
        attacker_weight_min_pct=(100 * w0.min()) if w0 is not None else np.nan,
        attacker_weight_max_pct=(100 * w0.max()) if w0 is not None else np.nan,
        benign_fused_risk_mean_over_rounds=ben_risk, benign_trust_mean=ben_trust_mean, benign_trust_min=ben_trust_min,
        attacker_topology_risk_mean=h["etdfgl_topology_risk_client_0"].mean() if w0 is not None else np.nan,
        attacker_update_risk_mean=h["etdfgl_update_risk_client_0"].mean() if w0 is not None else np.nan,
        attacker_update_risk_max=h["etdfgl_update_risk_client_0"].max() if w0 is not None else np.nan,
        attacker_trust_mean=h["etdfgl_trust_client_0"].mean() if w0 is not None else np.nan,
        source_summary=sp.relative_to(repo).as_posix(),
        source_summary_sha256=hashlib.sha256(sp.read_bytes()).hexdigest()[:16],
    ))
raw = pd.DataFrame(recs)
raw["dataset"] = pd.Categorical(raw["dataset"], DS, ordered=True)
raw = raw.sort_values(["suite", "dataset", "slug", "seed"]).reset_index(drop=True)
raw.round(6).to_csv(out / "R01_all_132_runs_raw.csv", index=False)

def ms(x, nd=2):
    x = np.asarray(x, float)
    return f"{x.mean():.{nd}f} ± {x.std(ddof=1):.{nd}f}" if len(x) > 1 else f"{x.mean():.{nd}f}"

# ---------------------------------------------------------------- R02 baseline seed 42
b = raw[raw.suite == "baseline_seed42"].copy()
order = ["fedavg_clean", "fedavg_structural_backdoor", "baseline_pdfl", "baseline_gsp", "baseline_flpurifier", "baseline_dmgnn", "baseline_fedtge", "defended_etdfgl"]
disp = {"fedavg_clean": "Clean FedAvg", "fedavg_structural_backdoor": "Attacked FedAvg", "baseline_pdfl": "PD-FL", "baseline_gsp": "GSP-FL",
        "baseline_flpurifier": "FLPurifier-GNN", "baseline_dmgnn": "DMGNN-FL", "baseline_fedtge": "FedTGE", "defended_etdfgl": "ETD-FGL"}
b["method"] = b.slug.map(disp)
b["o"] = b.slug.map({k: i for i, k in enumerate(order)})
b = b.sort_values(["dataset", "o"])
b[["dataset", "method", "seed", "clean_accuracy_pct", "asr_pct", "attack_effect_pp", "clean_target_rate_pct", "active_loop_seconds", "best_round", "source_summary"]].round(4).to_csv(out / "R02_seed42_baselines_tab_seed42_baselines.csv", index=False)

# ---------------------------------------------------------------- R03 multiseed
m = raw[raw.suite == "multiseed"].copy(); m["method"] = m.slug.map(disp)
m[["dataset", "method", "seed", "clean_accuracy_pct", "asr_pct", "attack_effect_pp", "clean_target_rate_pct", "active_loop_seconds", "best_round", "attacker_weight_mean_over_50_rounds_pct", "source_summary"]].round(4).to_csv(out / "R03a_multiseed_per_seed.csv", index=False)
rows = []
for (ds, meth), g in m.groupby(["dataset", "method"], observed=True):
    rows.append(dict(dataset=ds, method=meth, n_seeds=len(g), seeds="42,43,44",
        clean_acc_mean=g.clean_accuracy_pct.mean(), clean_acc_sd=g.clean_accuracy_pct.std(ddof=1),
        asr_mean=g.asr_pct.mean(), asr_sd=g.asr_pct.std(ddof=1), asr_min=g.asr_pct.min(), asr_max=g.asr_pct.max(),
        effect_mean=g.attack_effect_pp.mean(), effect_sd=g.attack_effect_pp.std(ddof=1),
        runtime_mean=g.active_loop_seconds.mean(), runtime_sd=g.active_loop_seconds.std(ddof=1),
        sd_convention="sample SD, ddof=1"))
pd.DataFrame(rows).round(4).to_csv(out / "R03b_multiseed_summary_tab_multiseed_robustness.csv", index=False)

# ---------------------------------------------------------------- R04 standard ablation
a = raw[raw.suite == "ablation"].copy()
sdisp = {"fedavg_structural_backdoor": "Attacked FedAvg", "etdfgl_full": "ETD-FGL (Full)", "etdfgl_no_update": "Topology-only (renormalized 1.0/0)",
         "etdfgl_no_topology": "Update-only (renormalized 0/1.0)", "etdfgl_no_trust": "No trust weighting (uniform)", "etdfgl_historical_three_channel": "Historical 3-channel (0.45/0.35/0.20)"}
a["variant"] = a.slug.map(sdisp)
a[["dataset", "variant", "slug", "seed", "clean_accuracy_pct", "asr_pct", "attack_effect_pp", "attacker_weight_mean_over_50_rounds_pct", "benign_fused_risk_mean_over_rounds", "active_loop_seconds", "source_summary"]].round(4).to_csv(out / "R04a_standard_ablation_per_seed.csv", index=False)
rows = []
for (ds, v, slug), g in a.groupby(["dataset", "variant", "slug"], observed=True):
    rows.append(dict(dataset=ds, variant=v, slug=slug, n_seeds=len(g), clean_acc_mean=g.clean_accuracy_pct.mean(), clean_acc_sd=g.clean_accuracy_pct.std(ddof=1),
        asr_mean=g.asr_pct.mean(), asr_sd=g.asr_pct.std(ddof=1), effect_mean=g.attack_effect_pp.mean(), effect_sd=g.attack_effect_pp.std(ddof=1),
        attacker_weight_mean=g.attacker_weight_mean_over_50_rounds_pct.mean(), attacker_weight_sd=g.attacker_weight_mean_over_50_rounds_pct.std(ddof=1)))
pd.DataFrame(rows).round(4).to_csv(out / "R04b_standard_ablation_summary.csv", index=False)

# ---------------------------------------------------------------- R05 controlled ablation
c = raw[raw.suite == "controlled_ablation_v1"].copy()
cdisp = {"etdfgl_full": "Full ETD-FGL (9/13 topo + 4/13 upd)", "etdfgl_fixed_no_update": "Fixed No Update (9/13 topo only)", "etdfgl_fixed_no_topology": "Fixed No Topology (4/13 upd only)", "fedavg_structural_backdoor": "Attacked FedAvg"}
c["variant"] = c.slug.map(cdisp)
c[["dataset", "variant", "slug", "seed", "clean_accuracy_pct", "asr_pct", "attack_effect_pp", "attacker_weight_mean_over_50_rounds_pct", "attacker_weight_final_round_pct", "benign_fused_risk_mean_over_rounds", "benign_trust_mean", "benign_trust_min", "attacker_topology_risk_mean", "attacker_update_risk_mean", "active_loop_seconds", "source_summary"]].round(5).to_csv(out / "R05a_controlled_ablation_per_seed.csv", index=False)
rows = []
for (ds, v, slug), g in c.groupby(["dataset", "variant", "slug"], observed=True):
    rows.append(dict(dataset=ds, variant=v, slug=slug, n_seeds=len(g), clean_acc_mean=g.clean_accuracy_pct.mean(), clean_acc_sd=g.clean_accuracy_pct.std(ddof=1),
        asr_mean=g.asr_pct.mean(), asr_sd=g.asr_pct.std(ddof=1), effect_mean=g.attack_effect_pp.mean(), effect_sd=g.attack_effect_pp.std(ddof=1),
        attacker_weight_mean=g.attacker_weight_mean_over_50_rounds_pct.mean(), attacker_weight_sd=g.attacker_weight_mean_over_50_rounds_pct.std(ddof=1),
        benign_risk_mean=g.benign_fused_risk_mean_over_rounds.mean(), benign_risk_sd=g.benign_fused_risk_mean_over_rounds.std(ddof=1),
        benign_trust_mean=g.benign_trust_mean.mean(), benign_trust_min_over_all=g.benign_trust_min.min()))
pd.DataFrame(rows).round(5).to_csv(out / "R05b_controlled_ablation_summary_tab_ablation_comparison_tab_attacker_suppression.csv", index=False)

# ---------------------------------------------------------------- R06 paired differences
rows = []
full = c[c.slug == "etdfgl_full"].set_index(["dataset", "seed"])
for slug, lab in [("etdfgl_fixed_no_update", "Remove update channel (Fixed No Update minus Full)"), ("etdfgl_fixed_no_topology", "Remove topology channel (Fixed No Topology minus Full)")]:
    var = c[c.slug == slug].set_index(["dataset", "seed"])
    for ds in DS:
        for sd in (42, 43, 44):
            f = full.loc[(ds, sd)]; v = var.loc[(ds, sd)]
            rows.append(dict(dataset=ds, seed=sd, comparison=lab, d_clean_acc_pp=v.clean_accuracy_pct - f.clean_accuracy_pct, d_asr_pp=v.asr_pct - f.asr_pct,
                d_attack_effect_pp=v.attack_effect_pp - f.attack_effect_pp,
                d_attacker_weight_pp=v.attacker_weight_mean_over_50_rounds_pct - f.attacker_weight_mean_over_50_rounds_pct,
                d_benign_risk=v.benign_fused_risk_mean_over_rounds - f.benign_fused_risk_mean_over_rounds))
pp = pd.DataFrame(rows)
pp.round(5).to_csv(out / "R06a_paired_differences_per_seed.csv", index=False)
rows = []
for (ds, comp), g in pp.groupby(["dataset", "comparison"], observed=True):
    rows.append(dict(dataset=ds, comparison=comp, n_pairs=len(g),
        d_asr_mean=g.d_asr_pp.mean(), d_asr_sd=g.d_asr_pp.std(ddof=1), d_asr_per_seed="; ".join(f"{x:+.2f}" for x in g.d_asr_pp),
        d_clean_acc_mean=g.d_clean_acc_pp.mean(), d_clean_acc_sd=g.d_clean_acc_pp.std(ddof=1),
        d_attack_effect_mean=g.d_attack_effect_pp.mean(), d_attack_effect_sd=g.d_attack_effect_pp.std(ddof=1),
        d_attacker_weight_mean=g.d_attacker_weight_pp.mean(), d_attacker_weight_sd=g.d_attacker_weight_pp.std(ddof=1),
        n_seeds_with_positive_d_asr=int((g.d_asr_pp > 0).sum()),
        significance_test="NOT RUN (n=3 pairs; no p-value or CI computed)"))
pd.DataFrame(rows).round(4).to_csv(out / "R06b_paired_differences_summary_tab_paired_contributions.csv", index=False)

# ---------------------------------------------------------------- R07 per-round trajectories (seed 42, final_multidataset)
rows = []
for (suite, ds, seed, slug), h in hist_cache.items():
    if suite != "baseline_seed42":
        continue
    for _, r in h.iterrows():
        rows.append(dict(dataset=ds, method=disp[slug], round=int(r["round"]), clean_accuracy_pct=100 * r["test_accuracy"],
                         asr_pct=100 * r["attack_success_rate"], attack_effect_pp=100 * r["attack_effect"], validation_accuracy_pct=100 * r["validation_accuracy"],
                         attacker_weight_pct=(100 * r["etdfgl_weight_client_0"]) if "etdfgl_weight_client_0" in r and pd.notna(r.get("etdfgl_weight_client_0")) else np.nan))
pd.DataFrame(rows).round(5).to_csv(out / "R07_round_trajectories_seed42_baselines.csv", index=False)
rows = []
for (suite, ds, seed, slug), h in hist_cache.items():
    if suite != "controlled_ablation_v1" or slug == "fedavg_structural_backdoor" or seed != 42:
        continue
    for _, r in h.iterrows():
        rows.append(dict(dataset=ds, variant=cdisp[slug], round=int(r["round"]), attacker_weight_pct=100 * r["etdfgl_weight_client_0"],
                         attacker_trust=r["etdfgl_trust_client_0"], attacker_topology_risk=r["etdfgl_topology_risk_client_0"],
                         attacker_update_risk=r["etdfgl_update_risk_client_0"], asr_pct=100 * r["attack_success_rate"], clean_accuracy_pct=100 * r["test_accuracy"]))
pd.DataFrame(rows).round(5).to_csv(out / "R08_attacker_weight_trajectories_seed42_controlled.csv", index=False)

# multiseed ETD-FGL per-round trajectories (all seeds) for early-round check
rows = []
for (suite, ds, seed, slug), h in hist_cache.items():
    if suite != "multiseed":
        continue
    for _, r in h.iterrows():
        rows.append(dict(dataset=ds, seed=seed, method=disp[slug], round=int(r["round"]), clean_accuracy_pct=100 * r["test_accuracy"], asr_pct=100 * r["attack_success_rate"],
                         attacker_weight_pct=(100 * r["etdfgl_weight_client_0"]) if slug == "defended_etdfgl" else np.nan))
pd.DataFrame(rows).round(5).to_csv(out / "R09_round_trajectories_multiseed_all_seeds.csv", index=False)

# ---------------------------------------------------------------- R10 early-round check
rows = []
for (suite, ds, seed, slug), h in hist_cache.items():
    if suite not in ("multiseed", "baseline_seed42") or slug not in ("defended_etdfgl", "fedavg_structural_backdoor", "fedavg_clean"):
        continue
    if suite == "multiseed" and seed == 42:
        continue  # seed 42 covered by baseline_seed42 (also recorded in multiseed; same metrics)
    asr = 100 * h["attack_success_rate"].values
    rows.append(dict(suite=suite, dataset=ds, seed=seed, method=disp[slug], asr_round1=asr[0], asr_round2=asr[1], asr_round5=asr[4], asr_round10=asr[9], asr_round25=asr[24], asr_round50=asr[49],
                     asr_max_over_rounds=asr.max(), round_of_max=int(asr.argmax()) + 1, first_round_asr_below_5pct=int(np.argmax(asr < 5)) + 1 if (asr < 5).any() else -1,
                     rounds_with_asr_ge_5pct=int((asr >= 5).sum())))
pd.DataFrame(rows).round(3).to_csv(out / "R10_early_round_asr_check.csv", index=False)

# ---------------------------------------------------------------- R11 runtime variability
rt = raw[raw.slug.isin(["fedavg_structural_backdoor", "defended_etdfgl", "fedavg_clean"])][["suite", "dataset", "seed", "slug", "active_loop_seconds"]]
rt.round(4).to_csv(out / "R11_runtime_same_method_across_suites.csv", index=False)

# ---------------------------------------------------------------- R12 dataset / partition metadata
rows = []
for ds in ["cora", "pubmed", "reddit"]:
    for seed in (42, 43, 44):
        base = repo / "outputs" / "extended_experiments" / "multiseed" / ds / f"seed_{seed}"
        ps = list(base.glob("partitions/**/partition_summary.json")) or list(base.rglob("partition_summary.json"))
        s = json.loads((base / "defended_etdfgl" / "final_summary.json").read_text(encoding="utf-8"))
        am = s["attack_metadata"]
        row = dict(dataset=s["dataset"], seed=seed, dataset_nodes=s["dataset_metadata"].get("num_nodes", s["dataset_metadata"].get("sample_size")),
                   dataset_directed_edge_entries_pyg=s["dataset_metadata"].get("num_edges"), partition=s["partition_metadata"]["strategy"],
                   poison_count=am["poison_count"], added_trigger_nodes=am["added_trigger_nodes"], added_directed_edges=am["added_directed_edges"],
                   trigger_active_features=am["trigger_active_features"], trigger_feature_norm=am["trigger_feature_norm"])
        if ps:
            P = json.loads(ps[0].read_text(encoding="utf-8"))
            lst = P if isinstance(P, list) else P.get("clients", P)
            if isinstance(lst, list):
                for c_ in lst:
                    cid = c_.get("client_id")
                    for k in ("nodes", "edges", "train_nodes", "validation_nodes", "test_nodes"):
                        if k in c_:
                            row[f"client{cid}_{k}"] = c_[k]
        rows.append(row)
pd.DataFrame(rows).to_csv(out / "R12_dataset_partition_attack_metadata.csv", index=False)
print("ok", len(raw))
