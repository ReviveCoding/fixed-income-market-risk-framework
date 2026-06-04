from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
REP = ROOT / "reports"


def test_v4_review_depth_outputs_exist():
    required = [
        "pnl_attribution_summary.csv",
        "pnl_attribution_proxy.csv",
        "frtb_inspired_diagnostics.csv",
        "challenger_model_selection.csv",
        "reverse_stress_diagnostics.csv",
        "reproducibility_manifest.csv",
        "reproducibility_metadata.json",
    ]
    for name in required:
        assert (OUT / name).exists(), name


def test_pnl_attribution_proxy_passes_review_gates():
    summary = pd.read_csv(OUT / "pnl_attribution_summary.csv").iloc[0]
    assert summary["pla_proxy_status"] == "PASS"
    assert float(summary["actual_hypothetical_corr"]) >= 0.90
    assert float(summary["p95_absolute_unexplained_ratio"]) <= 0.20


def test_frtb_inspired_diagnostics_are_complete_and_bounded():
    diag = pd.read_csv(OUT / "frtb_inspired_diagnostics.csv")
    assert set(diag["risk_factor_family"]) == {"rates", "corporate_credit", "securitized_proxy"}
    assert (diag["liquidity_horizon_days"] > 0).all()
    assert (diag["es_975"] >= diag["var_975"]).all()
    assert abs(float(diag["scaled_es_contribution_share"].sum()) - 1.0) < 1e-6


def test_challenger_selection_has_one_selected_model():
    challengers = pd.read_csv(OUT / "challenger_model_selection.csv")
    assert len(challengers) >= 3
    assert challengers["selected"].astype(str).str.lower().eq("true").sum() == 1
    selected = challengers.loc[challengers["selected"].astype(str).str.lower().eq("true"), "candidate"].iloc[0]
    assert selected in {"residual_corrected_var", "conservative_tail_envelope", "vanilla_historical_var"}


def test_reverse_stress_and_manifest_outputs_are_usable():
    reverse = pd.read_csv(OUT / "reverse_stress_diagnostics.csv")
    assert not reverse.empty
    assert (reverse["multiplier_to_var_99"] >= 0).all()
    manifest = pd.read_csv(OUT / "reproducibility_manifest.csv")
    assert len(manifest) >= 50
    assert {"relative_path", "bytes", "sha256"}.issubset(manifest.columns)
    meta = json.loads((OUT / "reproducibility_metadata.json").read_text())
    assert meta["file_count"] == len(manifest)


def test_v4_reports_exist():
    for name in [
        "pnl_attribution_proxy_report.md",
        "frtb_inspired_diagnostics_report.md",
        "challenger_model_selection_report.md",
        "reverse_stress_testing_report.md",
        "reproducibility_manifest_report.md",
    ]:
        text = (REP / name).read_text(encoding="utf-8")
        assert "#" in text and len(text) > 200
