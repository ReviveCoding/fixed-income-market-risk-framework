from __future__ import annotations

import pandas as pd


def assign_market_health_timestep(losses: pd.DataFrame, loss_col: str = "total_loss", window: int = 63) -> pd.DataFrame:
    df = losses.copy().sort_values("date")
    df["rolling_vol"] = df[loss_col].rolling(window, min_periods=10).std().bfill()
    q1, q2 = df["rolling_vol"].quantile([0.50, 0.85])
    def state(v):
        if v <= q1: return "normal"
        if v <= q2: return "elevated"
        return "stressed"
    df["market_health_state"] = df["rolling_vol"].map(state)
    df["market_health_timestep"] = df.groupby("market_health_state").cumcount() + 1
    return df
