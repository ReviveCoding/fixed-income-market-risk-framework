from __future__ import annotations

import pandas as pd

RATING_MAP = {"A": "A_OAS", "BBB": "BBB_OAS", "BB": "BB_OAS", "B": "B_OAS", "CCC": "CCC_OAS"}


def build_credit_spread_factors(spreads: pd.DataFrame) -> pd.DataFrame:
    df = spreads.sort_values("date").copy()
    for col in [c for c in df.columns if c != "date"]:
        df[f"d_{col}_bp"] = df[col].diff() * 100.0
    out = df[["date"]].copy()
    out["ig_spread_bp"] = df["d_IG_OAS_bp"]
    out["hy_spread_bp"] = df["d_HY_OAS_bp"]
    out["a_spread_bp"] = df["d_A_OAS_bp"]
    out["bbb_spread_bp"] = df["d_BBB_OAS_bp"]
    out["bb_spread_bp"] = df["d_BB_OAS_bp"]
    out["b_spread_bp"] = df["d_B_OAS_bp"]
    out["ccc_spread_bp"] = df["d_CCC_OAS_bp"]
    out["credit_level_bp"] = out[["ig_spread_bp", "hy_spread_bp"]].mean(axis=1)
    out["credit_quality_slope_bp"] = out["hy_spread_bp"] - out["ig_spread_bp"]
    return out.dropna()
