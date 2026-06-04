from __future__ import annotations

import pandas as pd


def run_stress_scenarios(corp_sens: pd.DataFrame, tranche_summary: pd.DataFrame) -> pd.DataFrame:
    scenarios = {
        "parallel_rate_up_100bp": {"rate_bp": 100, "credit_bp": 0, "securitized_bp": 0},
        "curve_shock_proxy": {"rate_bp": 60, "credit_bp": 20, "securitized_bp": 25},
        "ig_spread_widen_75bp": {"rate_bp": 0, "credit_bp": 75, "securitized_bp": 25},
        "hy_spread_widen_250bp": {"rate_bp": 0, "credit_bp": 250, "securitized_bp": 50},
        "liquidity_spread_shock": {"rate_bp": 0, "credit_bp": 150, "securitized_bp": 175},
        "mortgage_default_severity_shock": {"rate_bp": 20, "credit_bp": 80, "securitized_bp": 250},
    }
    rows = []
    total_dv01 = float(corp_sens["dv01"].sum())
    total_cs01 = float(corp_sens["cs01"].sum())
    sec_exposure = float(tranche_summary["total_principal"].sum() + tranche_summary["ending_outstanding"].sum())
    for name, s in scenarios.items():
        rate_loss = total_dv01 * s["rate_bp"]
        credit_loss = total_cs01 * s["credit_bp"]
        sec_loss = sec_exposure * s["securitized_bp"] * 0.00002
        rows.append({"scenario": name, "rate_loss": rate_loss, "corporate_credit_loss": credit_loss, "securitized_proxy_loss": sec_loss, "total_stress_loss": rate_loss + credit_loss + sec_loss})
    return pd.DataFrame(rows).sort_values("total_stress_loss", ascending=False)
