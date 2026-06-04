from __future__ import annotations

import numpy as np
import pandas as pd


def historical_var(losses: pd.Series, confidence: float = 0.99) -> float:
    return float(np.nanquantile(losses.dropna(), confidence))


def expected_shortfall(losses: pd.Series, confidence: float = 0.99) -> float:
    var = historical_var(losses, confidence)
    tail = losses.dropna()[losses.dropna() >= var]
    return float(tail.mean() if len(tail) else var)


def monte_carlo_var(losses: pd.Series, confidence: float = 0.99, scenarios: int = 20000, seed: int = 123, student_t_df: int | None = None) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    mu = float(losses.mean())
    sigma = float(losses.std(ddof=1))
    if student_t_df is None:
        sims = rng.normal(mu, sigma, scenarios)
    else:
        raw = rng.standard_t(student_t_df, scenarios)
        raw = raw / np.sqrt(student_t_df / (student_t_df - 2))
        sims = mu + sigma * raw
    var = float(np.quantile(sims, confidence))
    es = float(sims[sims >= var].mean())
    return var, es


def stressed_var(losses: pd.DataFrame, loss_col: str = "total_loss", window: int = 250, confidence: float = 0.99) -> dict:
    df = losses.dropna(subset=[loss_col]).copy().reset_index(drop=True)
    if len(df) < window:
        var = historical_var(df[loss_col], confidence)
        return {"window_start": str(df["date"].min().date()), "window_end": str(df["date"].max().date()), "stressed_var": var}
    rolling_vol = df[loss_col].rolling(window).std()
    end_idx = int(rolling_vol.idxmax())
    start_idx = max(0, end_idx - window + 1)
    window_df = df.iloc[start_idx:end_idx + 1]
    return {
        "window_start": str(window_df["date"].min().date()),
        "window_end": str(window_df["date"].max().date()),
        "stressed_var": historical_var(window_df[loss_col], confidence),
        "window_volatility": float(window_df[loss_col].std(ddof=1)),
    }
