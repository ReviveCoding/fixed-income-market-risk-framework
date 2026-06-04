from __future__ import annotations

import numpy as np
import pandas as pd


def traffic_light_backtest(backtest_df: pd.DataFrame, evaluation_days: int = 250) -> dict:
    """Basel-style traffic-light proxy using the most recent 250 VaR observations.

    This is a review diagnostic, not a regulatory capital calculation.
    """
    if backtest_df.empty:
        return {
            "evaluation_days": 0,
            "exceptions": 0,
            "exception_rate": 0.0,
            "traffic_light": "green",
            "review_action": "No observations available; rerun after data is available.",
        }
    recent = backtest_df.sort_values("date").tail(evaluation_days).copy()
    exceptions = int(recent["exception"].sum())
    n = int(len(recent))
    if exceptions <= 4:
        light = "green"
        action = "Within common green-zone review tolerance for a 99% VaR exception-count diagnostic."
    elif exceptions <= 9:
        light = "yellow"
        action = "Review VaR calibration, stressed periods, and exception root causes before model-use expansion."
    else:
        light = "red"
        action = "Block release and investigate calibration, data, and assumptions before model-use expansion."
    return {
        "evaluation_days": n,
        "exceptions": exceptions,
        "exception_rate": float(exceptions / max(n, 1)),
        "traffic_light": light,
        "review_action": action,
    }


def exception_attribution(losses: pd.DataFrame, backtest_df: pd.DataFrame) -> pd.DataFrame:
    """Attribute VaR exceptions to the largest daily loss component and market state."""
    if backtest_df.empty:
        return pd.DataFrame(columns=["dominant_factor", "market_health_state", "exceptions", "avg_severity", "max_severity"])
    cols = [
        "date",
        "rates_loss",
        "corporate_credit_loss",
        "securitized_proxy_loss",
        "market_health_state",
    ]
    merged = backtest_df.merge(losses[cols], on="date", how="left")
    exc = merged.loc[merged["exception"]].copy()
    if exc.empty:
        return pd.DataFrame(columns=["dominant_factor", "market_health_state", "exceptions", "avg_severity", "max_severity"])
    component_cols = ["rates_loss", "corporate_credit_loss", "securitized_proxy_loss"]
    exc["dominant_factor"] = exc[component_cols].abs().idxmax(axis=1).str.replace("_loss", "", regex=False)
    grouped = exc.groupby(["dominant_factor", "market_health_state"], as_index=False).agg(
        exceptions=("exception", "sum"),
        avg_severity=("exception_severity", "mean"),
        max_severity=("exception_severity", "max"),
    )
    total_exc = max(float(grouped["exceptions"].sum()), 1.0)
    grouped["exception_share"] = grouped["exceptions"] / total_exc
    return grouped.sort_values(["exceptions", "avg_severity"], ascending=False)


def var_stability_diagnostics(losses: pd.DataFrame, loss_col: str = "total_loss", confidence: float = 0.99) -> pd.DataFrame:
    """Compare VaR/ES estimates across lookback windows and simple bootstrap samples."""
    clean = losses.sort_values("date").dropna(subset=[loss_col]).copy()
    rows = []
    for window in [125, 250, 500, min(len(clean), 750)]:
        if window < 60 or len(clean) < window:
            continue
        sample = clean.tail(window)[loss_col].to_numpy()
        var = float(np.quantile(sample, confidence))
        tail = sample[sample >= var]
        es = float(tail.mean()) if len(tail) else var
        rng = np.random.default_rng(2026 + window)
        boot_vars = []
        for _ in range(200):
            draw = rng.choice(sample, size=len(sample), replace=True)
            boot_vars.append(float(np.quantile(draw, confidence)))
        rows.append({
            "lookback_days": int(window),
            "var_99": var,
            "es_99": es,
            "bootstrap_var_p05": float(np.quantile(boot_vars, 0.05)),
            "bootstrap_var_p95": float(np.quantile(boot_vars, 0.95)),
            "bootstrap_ci_width": float(np.quantile(boot_vars, 0.95) - np.quantile(boot_vars, 0.05)),
        })
    out = pd.DataFrame(rows).drop_duplicates(subset=["lookback_days"])
    if not out.empty:
        base = float(out.loc[out["lookback_days"].idxmax(), "var_99"])
        out["relative_delta_vs_longest"] = out["var_99"] / max(base, 1.0) - 1.0
    return out
