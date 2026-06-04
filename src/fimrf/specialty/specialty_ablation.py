from __future__ import annotations

import pandas as pd


def build_specialty_ablation(backtest_df: pd.DataFrame, corrected_df: pd.DataFrame, envelope: float) -> pd.DataFrame:
    baseline_exc = float(backtest_df["exception"].mean()) if not backtest_df.empty else 0.0
    corrected_exc = float(corrected_df["corrected_exception"].mean()) if not corrected_df.empty else baseline_exc
    envelope_exc = float((backtest_df["total_loss"] > envelope).mean()) if not backtest_df.empty else 0.0
    return pd.DataFrame([
        {"module": "vanilla_historical_var", "exception_rate": baseline_exc, "relative_change_vs_vanilla": 0.0},
        {"module": "residual_var_correction", "exception_rate": corrected_exc, "relative_change_vs_vanilla": corrected_exc - baseline_exc},
        {"module": "conservative_risk_envelope", "exception_rate": envelope_exc, "relative_change_vs_vanilla": envelope_exc - baseline_exc},
    ])
