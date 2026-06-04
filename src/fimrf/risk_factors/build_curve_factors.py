from __future__ import annotations

import pandas as pd


def build_curve_factors(rates: pd.DataFrame) -> pd.DataFrame:
    df = rates.sort_values("date").copy()
    # Percentage point changes converted to basis points.
    for col in [c for c in df.columns if c != "date"]:
        df[f"d_{col}_bp"] = df[col].diff() * 100.0
    df["rate_level_bp"] = df[["d_DGS2_bp", "d_DGS5_bp", "d_DGS10_bp"]].mean(axis=1)
    df["rate_slope_bp"] = df["d_DGS10_bp"] - df["d_DGS2_bp"]
    df["rate_curvature_bp"] = 2 * df["d_DGS5_bp"] - df["d_DGS2_bp"] - df["d_DGS10_bp"]
    return df[["date", "rate_level_bp", "rate_slope_bp", "rate_curvature_bp"]].dropna()
