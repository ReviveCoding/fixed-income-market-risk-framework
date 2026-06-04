from __future__ import annotations

import numpy as np
import pandas as pd


def residual_var_correction(backtest_df: pd.DataFrame, max_multiplier: float = 1.40) -> tuple[pd.DataFrame, float]:
    """Empirical residual VaR correction from observed backtesting residuals.

    The v2 correction only reacted to aggregate exception rate. This stronger but
    still conservative version estimates a bounded multiplier from the empirical
    loss/VaR ratio on breached days. It is an offline research diagnostic, not a
    model-approval overlay.
    """
    df = backtest_df.copy()
    if df.empty:
        return df, 1.0
    valid = df.loc[df["var_99"] > 0].copy()
    breached = valid.loc[valid["total_loss"] > valid["var_99"]].copy()
    target = 0.01
    realized = float(valid["exception"].mean()) if not valid.empty else 0.0
    rate_multiplier = 1.0 + max(realized - target, 0.0) * 10.0
    if breached.empty:
        multiplier = 1.0
    else:
        ratios = (breached["total_loss"] / breached["var_99"]).replace([np.inf, -np.inf], np.nan).dropna()
        severity_multiplier = float(np.quantile(ratios, 0.75) * 1.02) if len(ratios) else 1.0
        multiplier = max(rate_multiplier, severity_multiplier, 1.0)
    multiplier = min(max(multiplier, 1.0), max_multiplier)
    df["corrected_var_99"] = df["var_99"] * multiplier
    df["corrected_exception"] = df["total_loss"] > df["corrected_var_99"]
    df["correction_method"] = "bounded_empirical_breach_ratio_q75"
    return df, float(multiplier)
