from __future__ import annotations

import numpy as np
import pandas as pd


def reverse_stress_diagnostics(stress_losses: pd.DataFrame, var_99: float, es_99: float) -> pd.DataFrame:
    """Estimate shock multipliers needed for stress losses to exceed VaR/ES thresholds."""
    if stress_losses.empty:
        return pd.DataFrame(columns=["scenario", "base_total_stress_loss", "multiplier_to_var_99", "multiplier_to_es_99", "reverse_stress_priority"])
    df = stress_losses.copy()
    denom = np.maximum(df["total_stress_loss"].abs(), 1.0)
    df["multiplier_to_var_99"] = float(var_99) / denom
    df["multiplier_to_es_99"] = float(es_99) / denom
    df["reverse_stress_priority"] = pd.cut(
        df["multiplier_to_es_99"],
        bins=[-np.inf, 0.75, 1.25, 2.0, np.inf],
        labels=["already_beyond_es", "near_es_threshold", "moderate_multiplier", "remote_under_current_proxy"],
    ).astype(str)
    return df[["scenario", "total_stress_loss", "multiplier_to_var_99", "multiplier_to_es_99", "reverse_stress_priority"]].rename(columns={"total_stress_loss": "base_total_stress_loss"}).sort_values("multiplier_to_es_99")
