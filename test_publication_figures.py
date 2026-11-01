"""Data-to-figure fidelity tests for figures/publication (no training; CSV inputs only)."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent
TABLES = ROOT / "figures" / "publication" / "tables"
SCRIPT = ROOT / "tools" / "publication_figures" / "make_publication_figures.py"


@pytest.fixture(scope="module")
def rendered():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        subprocess.run([sys.executable, "-I", str(SCRIPT), str(TABLES), str(out)], check=True, cwd=ROOT)
        yield out, json.loads((out / "plotted_data.json").read_text(encoding="utf-8"))


@pytest.mark.unit
def test_all_figures_exported_as_pdf_and_png(rendered):
    out, _ = rendered
    for name in ["Fig1_etdfgl_architecture_workflow", "Fig2_overall_baselines", "Fig4_multiseed_robustness",
                 "Fig5_learning_dynamics_rounds", "Fig6_controlled_ablation", "Fig7_attacker_weight_dynamics"]:
        assert (out / f"{name}.pdf").stat().st_size > 5_000
        assert (out / "previews" / f"{name}.png").exists()
    assert (out / "supplementary" / "FigS1_runtime_exploratory.pdf").exists()
    assert (out / "supplementary" / "FigS2_accuracy_asr_scatter.pdf").exists()


@pytest.mark.unit
def test_plotted_values_equal_csv_values(rendered):
    _, P = rendered
    b = pd.read_csv(TABLES / "R02_seed42_baselines_tab_seed42_baselines.csv")
    ms = pd.read_csv(TABLES / "R03a_multiseed_per_seed.csv")
    pp = pd.read_csv(TABLES / "R06a_paired_differences_per_seed.csv")
    for d in ["Cora", "PubMed", "Reddit"]:
        for m in ["Clean FedAvg", "ETD-FGL", "FedTGE"]:
            r = b[(b.dataset == d) & (b.method == m)].iloc[0]
            assert P[f"fig3_seed42_{d}_{m}"]["x"] == [r.clean_accuracy_pct] and P[f"fig3_seed42_{d}_{m}"]["y"] == [r.asr_pct]
        for m in ["Attacked FedAvg", "ETD-FGL"]:
            g = ms[(ms.dataset == d) & (ms.method == m)].sort_values("seed")
            s = P[f"fig3_mean3_{d}_{m}"]
            assert np.isclose(s["y"][0], g.asr_pct.mean()) and np.isclose(s["sy"][0], g.asr_pct.std(ddof=1))  # ddof=1
            assert np.allclose(P[f"fig4_asr_pct_{d}_{m}"]["per_seed"], g.asr_pct.values)
    reddit43 = ms[(ms.dataset == "Reddit") & (ms.method == "ETD-FGL") & (ms.seed == 43)].asr_pct.iloc[0]
    assert round(reddit43, 2) == 34.82
    g = pp[(pp.dataset == "Reddit") & pp.comparison.str.startswith("Remove update")]
    assert round(P["fig6_delta_Reddit_0"]["mean"][0], 2) == 11.11 and np.isclose(P["fig6_delta_Reddit_0"]["sd"][0], g.d_asr_pp.std(ddof=1))


@pytest.mark.unit
def test_round_trajectories_are_complete_and_preserve_early_spikes(rendered):
    _, P = rendered
    for d in ["Cora", "PubMed", "Reddit"]:
        s = P[f"fig5_asr_pct_{d}_ETD-FGL"]
        assert s["round"] == list(map(float, range(1, 51)))
    assert round(P["fig5_asr_pct_Cora_ETD-FGL"]["y"][0], 1) == 75.4
    assert round(P["fig5_asr_pct_PubMed_ETD-FGL"]["y"][0], 1) == 99.9
    assert max(P["fig5_asr_pct_Cora_ETD-FGL"]["y"][1:]) > 35  # later spikes not smoothed away


@pytest.mark.unit
def test_attacker_weight_raw_trace_is_unsmoothed_and_not_capped(rendered):
    _, P = rendered
    full = P["fig7_Cora_Full"]["w0"]
    assert len(full) == 50 and max(full) > 4.7  # old "<=4.7 %" ceiling is false
    assert set(np.round(P["fig7_Cora_Fixed No Update"]["w0"], 3)) == {4.117}
    assert max(P["fig7_Cora_Fixed No Topology"]["w0"]) > 20


@pytest.mark.unit
def test_figure_source_contains_no_rejected_claims():
    text = SCRIPT.read_text(encoding="utf-8").lower()
    for bad in ["<= 4.7", "≤4.7", "from round 1", "within 0.5", "gnnexplainer", "upper-left", "pareto frontier is", "significant", "how stable", "how strongly", "desirable"]:
        assert bad not in text.replace("no cross-dataset pareto frontier is claimed", "")


@pytest.mark.unit
@pytest.mark.skipif(shutil.which("pdffonts") is None, reason="pdffonts not installed")
def test_fonts_embedded(rendered):
    out, _ = rendered
    res = subprocess.run(["pdffonts", str(out / "Fig6_controlled_ablation.pdf")], capture_output=True, text=True).stdout.splitlines()[2:]
    assert res and all(" yes " in line for line in res)
