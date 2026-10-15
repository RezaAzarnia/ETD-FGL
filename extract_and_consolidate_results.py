#!/usr/bin/env python3
"""ETD-FGL Scientific Data Consolidation and Inventory Pipeline.

Extracts, validates, and consolidates all 132 experiments across:
1. Baseline Seed 42 Suite (outputs/final_multidataset/)
2. Multi-seed Suite (outputs/extended_experiments/multiseed/)
3. Standard Ablation Suite (outputs/extended_experiments/ablation/)
4. Controlled Ablation Suite (outputs/extended_experiments/controlled_ablation_v1/)

Performs strict cryptographic hash verification against experiment_manifest.json,
computes sample statistics (ddof=1) and paired differences, and produces
reproducible machine-readable research tables.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

DATASETS = ["cora", "pubmed", "reddit"]
DISPLAY_DATASETS = {"cora": "Cora", "pubmed": "PubMed", "reddit": "Reddit"}
SEEDS = [42, 43, 44]


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _format_mean_std(values: list[float], precision: int = 2) -> str:
    if not values:
        return "N/A"
    if len(values) == 1:
        return f"{values[0]:.{precision}f}"
    mean_val = float(np.mean(values))
    std_val = float(np.std(values, ddof=1))
    return f"{mean_val:.{precision}f} ± {std_val:.{precision}f}"


def inspect_all_experiments(project_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    # 1. Baseline Seed 42 Suite (outputs/final_multidataset/federated_{dataset}/{slug})
    for ds in DATASETS:
        ds_dir = project_dir / "outputs" / "final_multidataset" / f"federated_{ds}"
        if not ds_dir.is_dir():
            continue
        for exp_dir in ds_dir.iterdir():
            if not exp_dir.is_dir() or exp_dir.name in ("partitions", "comparison", "section4_extra_figures"):
                continue
            rec = parse_experiment_directory(
                exp_dir=exp_dir,
                project_dir=project_dir,
                suite="baseline_seed42",
                default_dataset=ds,
                default_seed=42,
            )
            if rec:
                records.append(rec)

    # 2. Multi-seed Suite (outputs/extended_experiments/multiseed/{dataset}/seed_{seed}/{slug})
    ms_root = project_dir / "outputs" / "extended_experiments" / "multiseed"
    if ms_root.is_dir():
        for ds in DATASETS:
            for s in SEEDS:
                seed_dir = ms_root / ds / f"seed_{s}"
                if not seed_dir.is_dir():
                    continue
                for exp_dir in seed_dir.iterdir():
                    if not exp_dir.is_dir() or exp_dir.name == "partitions":
                        continue
                    rec = parse_experiment_directory(
                        exp_dir=exp_dir,
                        project_dir=project_dir,
                        suite="multiseed",
                        default_dataset=ds,
                        default_seed=s,
                    )
                    if rec:
                        records.append(rec)

    # 3. Standard Ablation Suite (outputs/extended_experiments/ablation/{dataset}/seed_{seed}/{slug})
    abl_root = project_dir / "outputs" / "extended_experiments" / "ablation"
    if abl_root.is_dir():
        for ds in DATASETS:
            for s in SEEDS:
                seed_dir = abl_root / ds / f"seed_{s}"
                if not seed_dir.is_dir():
                    continue
                for exp_dir in seed_dir.iterdir():
                    if not exp_dir.is_dir() or exp_dir.name == "partitions":
                        continue
                    rec = parse_experiment_directory(
                        exp_dir=exp_dir,
                        project_dir=project_dir,
                        suite="standard_ablation",
                        default_dataset=ds,
                        default_seed=s,
                    )
                    if rec:
                        records.append(rec)

    # 4. Controlled Ablation Suite (outputs/extended_experiments/controlled_ablation_v1/{dataset}/seed_{seed}/{slug})
    ctrl_root = project_dir / "outputs" / "extended_experiments" / "controlled_ablation_v1"
    if ctrl_root.is_dir():
        for ds in DATASETS:
            for s in SEEDS:
                seed_dir = ctrl_root / ds / f"seed_{s}"
                if not seed_dir.is_dir():
                    continue
                for exp_dir in seed_dir.iterdir():
                    if not exp_dir.is_dir() or exp_dir.name == "partitions":
                        continue
                    rec = parse_experiment_directory(
                        exp_dir=exp_dir,
                        project_dir=project_dir,
                        suite="controlled_ablation",
                        default_dataset=ds,
                        default_seed=s,
                    )
                    if rec:
                        records.append(rec)

    return records


def parse_experiment_directory(
    exp_dir: Path,
    project_dir: Path,
    suite: str,
    default_dataset: str,
    default_seed: int,
) -> dict[str, Any] | None:
    sum_path = exp_dir / "final_summary.json"
    hist_path = exp_dir / "training_history.csv"
    ckpt_path = exp_dir / "best_model.pt"
    manifest_path = exp_dir / "experiment_manifest.json"

    if not sum_path.is_file():
        return None

    try:
        sum_data = json.loads(sum_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    final_m = sum_data.get("final_metrics", {})
    cfg = sum_data.get("config", {})

    dataset_key = str(cfg.get("key", default_dataset)).lower()
    dataset_display = DISPLAY_DATASETS.get(dataset_key, dataset_key.capitalize())
    seed = int(cfg.get("seed", default_seed))
    method_name = sum_data.get("method", exp_dir.name)
    slug = sum_data.get("output_slug", exp_dir.name)

    # Metrics (converted to percentages where appropriate)
    clean_acc = float(final_m.get("test_accuracy", 0.0)) * 100.0 if "test_accuracy" in final_m else None
    clean_target_rate = (
        float(final_m.get("clean_target_rate", 0.0)) * 100.0
        if "clean_target_rate" in final_m and final_m["clean_target_rate"] is not None
        else None
    )
    asr = (
        float(final_m.get("attack_success_rate", 0.0)) * 100.0
        if "attack_success_rate" in final_m and final_m["attack_success_rate"] is not None
        else None
    )
    attack_effect = (
        float(final_m.get("attack_effect", 0.0)) * 100.0
        if "attack_effect" in final_m and final_m["attack_effect"] is not None
        else None
    )

    elapsed_seconds = float(sum_data.get("elapsed_seconds", 0.0))
    best_round = int(sum_data.get("best_round", 0))
    rounds = int(cfg.get("rounds", 50))

    # Parse history CSV
    attacker_weights = []
    benign_risks = []
    has_history = hist_path.is_file()
    if has_history:
        try:
            with hist_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "etdfgl_weight_client_0" in row and row["etdfgl_weight_client_0"] != "":
                        attacker_weights.append(float(row["etdfgl_weight_client_0"]))

                    b_vals = []
                    for cid in range(1, 10):
                        k = f"etdfgl_fused_risk_client_{cid}"
                        if k in row and row[k] != "":
                            b_vals.append(float(row[k]))
                    if b_vals:
                        benign_risks.append(float(np.mean(b_vals)))
        except Exception:
            pass

    attacker_weight_mean = float(np.mean(attacker_weights)) * 100.0 if attacker_weights else None
    attacker_weight_final = float(attacker_weights[-1]) * 100.0 if attacker_weights else None
    benign_risk_mean = float(np.mean(benign_risks)) if benign_risks else None
    benign_risk_final = float(benign_risks[-1]) if benign_risks else None

    # Checkpoint and Manifest validation
    has_checkpoint = ckpt_path.is_file()
    has_manifest = manifest_path.is_file()
    manifest_valid = False
    manifest_sum_h = ""
    actual_sum_h = _file_sha256(sum_path)
    manifest_ckpt_h = ""
    actual_ckpt_h = _file_sha256(ckpt_path) if has_checkpoint else ""
    manifest_hist_h = ""
    actual_hist_h = _file_sha256(hist_path) if has_history else ""

    if has_manifest:
        try:
            m_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_sum_h = m_data.get("summary_sha256", "")
            manifest_ckpt_h = m_data.get("checkpoint_sha256", "")
            manifest_hist_h = m_data.get("history_sha256", "")

            sum_ok = actual_sum_h == manifest_sum_h
            ckpt_ok = actual_ckpt_h == manifest_ckpt_h
            hist_ok = actual_hist_h == manifest_hist_h
            manifest_valid = bool(sum_ok and ckpt_ok and hist_ok)
        except Exception:
            manifest_valid = False

    return {
        "dataset": dataset_display,
        "dataset_key": dataset_key,
        "suite": suite,
        "experiment_dir": str(exp_dir.relative_to(project_dir)),
        "output_slug": slug,
        "method_name": method_name,
        "seed": seed,
        "rounds": rounds,
        "best_round": best_round,
        "clean_test_accuracy": clean_acc,
        "clean_target_rate": clean_target_rate,
        "attack_success_rate": asr,
        "attack_effect": attack_effect,
        "elapsed_seconds": elapsed_seconds,
        "attacker_weight_mean": attacker_weight_mean,
        "attacker_weight_final": attacker_weight_final,
        "benign_risk_mean": benign_risk_mean,
        "benign_risk_final": benign_risk_final,
        "has_checkpoint": has_checkpoint,
        "has_history": has_history,
        "has_manifest": has_manifest,
        "manifest_valid": manifest_valid,
        "manifest_summary_sha256": manifest_sum_h,
        "actual_summary_sha256": actual_sum_h,
        "manifest_checkpoint_sha256": manifest_ckpt_h,
        "actual_checkpoint_sha256": actual_ckpt_h,
        "manifest_history_sha256": manifest_hist_h,
        "actual_history_sha256": actual_hist_h,
    }


def write_csv(records: list[dict[str, Any]], out_path: Path) -> None:
    if not records:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys())
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    out_base = project_dir / "paper_artifacts" / "ETDFGL_Publication_Results_v1"
    data_dir = out_base / "consolidated_data"
    out_base.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    records = inspect_all_experiments(project_dir)
    print(f"Total experiments parsed: {len(records)}")

    # 1. Master Consolidated CSV & JSON
    consolidated_csv = data_dir / "consolidated_experiments.csv"
    write_csv(records, consolidated_csv)
    print(f"Wrote master consolidated CSV: {consolidated_csv}")

    consolidated_json = data_dir / "consolidated_experiments.json"
    consolidated_json.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Wrote master consolidated JSON: {consolidated_json}")

    # 2. Source Inventory CSV (with validation status)
    inv_records = []
    for r in records:
        inv_records.append({
            "suite": r["suite"],
            "dataset": r["dataset"],
            "method": r["method_name"],
            "seed": r["seed"],
            "experiment_dir": r["experiment_dir"],
            "has_checkpoint": r["has_checkpoint"],
            "has_history": r["has_history"],
            "manifest_valid": r["manifest_valid"],
            "actual_summary_sha256": r["actual_summary_sha256"],
            "actual_checkpoint_sha256": r["actual_checkpoint_sha256"],
            "actual_history_sha256": r["actual_history_sha256"],
            "clean_test_accuracy": r["clean_test_accuracy"],
            "attack_success_rate": r["attack_success_rate"],
            "attack_effect": r["attack_effect"],
        })
    inv_csv = out_base / "source_inventory.csv"
    write_csv(inv_records, inv_csv)
    print(f"Wrote source inventory CSV: {inv_csv}")

    # 3. Baseline Seed 42 CSV
    b42_records = [r for r in records if r["suite"] == "baseline_seed42"]
    b42_csv = data_dir / "baseline_seed42.csv"
    write_csv(b42_records, b42_csv)

    # 4. Multi-seed Summary CSV (mean ± std across seeds 42, 43, 44)
    ms_records = [r for r in records if r["suite"] == "multiseed"]
    ms_summary = []
    for ds in ["Cora", "PubMed", "Reddit"]:
        for m_name in ["Attacked FedAvg", "ETD-FGL"]:
            runs = [r for r in ms_records if r["dataset"] == ds and r["method_name"] == m_name]
            if not runs:
                continue
            accs = [r["clean_test_accuracy"] for r in runs if r["clean_test_accuracy"] is not None]
            asrs = [r["attack_success_rate"] for r in runs if r["attack_success_rate"] is not None]
            effs = [r["attack_effect"] for r in runs if r["attack_effect"] is not None]
            runtimes = [r["elapsed_seconds"] for r in runs]
            ms_summary.append({
                "dataset": ds,
                "method": m_name,
                "seeds": len(runs),
                "clean_accuracy_mean": float(np.mean(accs)),
                "clean_accuracy_std": float(np.std(accs, ddof=1)) if len(accs) > 1 else 0.0,
                "clean_accuracy_display": _format_mean_std(accs),
                "asr_mean": float(np.mean(asrs)) if asrs else None,
                "asr_std": float(np.std(asrs, ddof=1)) if len(asrs) > 1 else 0.0,
                "asr_display": _format_mean_std(asrs) if asrs else "N/A",
                "attack_effect_mean": float(np.mean(effs)) if effs else None,
                "attack_effect_std": float(np.std(effs, ddof=1)) if len(effs) > 1 else 0.0,
                "attack_effect_display": _format_mean_std(effs) if effs else "N/A",
                "training_runtime_mean": float(np.mean(runtimes)),
                "training_runtime_std": float(np.std(runtimes, ddof=1)) if len(runtimes) > 1 else 0.0,
            })
    ms_summary_csv = data_dir / "multiseed_summary.csv"
    write_csv(ms_summary, ms_summary_csv)

    # 5. Standard Ablation Summary CSV
    std_abl_records = [r for r in records if r["suite"] == "standard_ablation"]
    std_abl_summary = []
    std_variants = [
        "Attacked FedAvg",
        "ETD-FGL (Full final)",
        "ETD-FGL Topology-only",
        "ETD-FGL Update-only",
        "ETD-FGL w/o Trust Weighting",
        "Historical Three-Channel Variant (0.45/0.35/0.20)",
    ]
    for ds in ["Cora", "PubMed", "Reddit"]:
        for m_name in std_variants:
            runs = [r for r in std_abl_records if r["dataset"] == ds and r["method_name"] == m_name]
            if not runs:
                continue
            accs = [r["clean_test_accuracy"] for r in runs if r["clean_test_accuracy"] is not None]
            asrs = [r["attack_success_rate"] for r in runs if r["attack_success_rate"] is not None]
            effs = [r["attack_effect"] for r in runs if r["attack_effect"] is not None]
            std_abl_summary.append({
                "dataset": ds,
                "variant": m_name,
                "seeds": len(runs),
                "clean_accuracy_display": _format_mean_std(accs),
                "asr_display": _format_mean_std(asrs) if asrs else "N/A",
                "attack_effect_display": _format_mean_std(effs) if effs else "N/A",
            })
    std_abl_csv = data_dir / "standard_ablation_summary.csv"
    write_csv(std_abl_summary, std_abl_csv)

    # 6. Controlled Ablation Summary & Paired Differences CSV
    ctrl_abl_records = [r for r in records if r["suite"] == "controlled_ablation"]
    ctrl_summary = []
    ctrl_paired = []
    ctrl_variants = [
        ("etdfgl_full", "ETD-FGL (Full final)"),
        ("etdfgl_fixed_no_update", "ETD-FGL Fixed No Update (9/13 Topo)"),
        ("etdfgl_fixed_no_topology", "ETD-FGL Fixed No Topology (4/13 Update)"),
    ]
    for ds in ["Cora", "PubMed", "Reddit"]:
        full_runs = {r["seed"]: r for r in ctrl_abl_records if r["dataset"] == ds and r["output_slug"] == "etdfgl_full"}
        for slug, display_title in ctrl_variants:
            runs = [r for r in ctrl_abl_records if r["dataset"] == ds and r["output_slug"] == slug]
            if not runs:
                continue
            accs = [r["clean_test_accuracy"] for r in runs]
            asrs = [r["attack_success_rate"] for r in runs]
            effs = [r["attack_effect"] for r in runs]
            atkwts = [r["attacker_weight_mean"] for r in runs if r["attacker_weight_mean"] is not None]
            brisks = [r["benign_risk_mean"] for r in runs if r["benign_risk_mean"] is not None]

            ctrl_summary.append({
                "dataset": ds,
                "variant_slug": slug,
                "variant_name": display_title,
                "seeds": len(runs),
                "clean_accuracy_display": _format_mean_std(accs),
                "asr_display": _format_mean_std(asrs),
                "attack_effect_display": _format_mean_std(effs),
                "attacker_weight_display": _format_mean_std(atkwts) if atkwts else "N/A",
                "benign_risk_display": _format_mean_std(brisks, precision=4) if brisks else "N/A",
            })

            # Compute paired difference against Full
            if slug != "etdfgl_full":
                d_acc, d_asr, d_eff, d_wt, d_br = [], [], [], [], []
                for s in SEEDS:
                    if s in full_runs:
                        match_r = next((r for r in runs if r["seed"] == s), None)
                        if match_r:
                            f_r = full_runs[s]
                            d_acc.append(match_r["clean_test_accuracy"] - f_r["clean_test_accuracy"])
                            d_asr.append(match_r["attack_success_rate"] - f_r["attack_success_rate"])
                            d_eff.append(match_r["attack_effect"] - f_r["attack_effect"])
                            if match_r["attacker_weight_mean"] is not None and f_r["attacker_weight_mean"] is not None:
                                d_wt.append(match_r["attacker_weight_mean"] - f_r["attacker_weight_mean"])
                            if match_r["benign_risk_mean"] is not None and f_r["benign_risk_mean"] is not None:
                                d_br.append(match_r["benign_risk_mean"] - f_r["benign_risk_mean"])
                ctrl_paired.append({
                    "dataset": ds,
                    "variant_slug": slug,
                    "variant_name": display_title,
                    "paired_seeds": len(d_acc),
                    "delta_clean_accuracy": _format_mean_std(d_acc),
                    "delta_asr": _format_mean_std(d_asr),
                    "delta_attack_effect": _format_mean_std(d_eff),
                    "delta_attacker_weight": _format_mean_std(d_wt) if d_wt else "N/A",
                    "delta_benign_risk": _format_mean_std(d_br, precision=4) if d_br else "N/A",
                })

    write_csv(ctrl_summary, data_dir / "controlled_ablation_summary.csv")
    write_csv(ctrl_paired, data_dir / "paired_differences.csv")

    print("Consolidation and verification complete!")


if __name__ == "__main__":
    main()
