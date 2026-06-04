from __future__ import annotations

import pandas as pd


def conservative_envelope(var_table: pd.DataFrame, uplift: float = 0.05) -> float:
    candidates = []
    for col in ["historical_var_99", "mc_gaussian_var_99", "mc_student_t_var_99", "stressed_var_99"]:
        if col in var_table.columns:
            candidates.extend(var_table[col].dropna().tolist())
    return max(candidates) * (1 + uplift) if candidates else 0.0


def false_safe_metrics(backtest_df: pd.DataFrame, envelope: float) -> dict:
    if backtest_df.empty:
        return {"false_safe_rate": 0.0, "tail_coverage_rate": 1.0, "coverage_overreach_ratio": 1.0}
    # False-safe proxy: realized loss exceeds original VaR but is not covered by conservative envelope.
    false_safe = ((backtest_df["total_loss"] > backtest_df["var_99"]) & (backtest_df["total_loss"] > envelope)).mean()
    tail_coverage = (backtest_df["total_loss"] <= envelope).mean()
    overreach = envelope / max(backtest_df["var_99"].median(), 1.0)
    return {"false_safe_rate": float(false_safe), "tail_coverage_rate": float(tail_coverage), "coverage_overreach_ratio": float(overreach)}
