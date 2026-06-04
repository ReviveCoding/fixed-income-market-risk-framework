from __future__ import annotations

import numpy as np
import pandas as pd


def pnl_attribution_proxy(losses: pd.DataFrame, residual_scale: float = 0.018, seed: int = 2026) -> tuple[pd.DataFrame, dict]:
    """Create actual/hypothetical P&L proxy and attribution diagnostics.

    This is an offline review artifact. It intentionally does not claim desk P&L.
    Hypothetical P&L proxy is the negative modeled portfolio loss. Actual P&L proxy
    adds deterministic unexplained noise to simulate fees, basis, and unmodeled risk.
    """
    required = ["date", "rates_loss", "corporate_credit_loss", "securitized_proxy_loss", "total_loss"]
    missing = [c for c in required if c not in losses.columns]
    if missing:
        raise ValueError(f"Missing columns for P&L attribution proxy: {missing}")
    df = losses[required + (["market_health_state"] if "market_health_state" in losses.columns else [])].copy()
    rng = np.random.default_rng(seed)
    scale = max(float(df["total_loss"].std(ddof=1)), 1.0) * residual_scale
    stress_multiplier = np.where(df.get("market_health_state", "normal") == "stressed", 1.65, 1.0)
    unexplained = rng.normal(0.0, scale, len(df)) * stress_multiplier
    df["hypothetical_pnl_proxy"] = -df["total_loss"]
    df["actual_pnl_proxy"] = df["hypothetical_pnl_proxy"] + unexplained
    df["unexplained_pnl_proxy"] = df["actual_pnl_proxy"] - df["hypothetical_pnl_proxy"]
    df["explained_loss_proxy"] = -df["hypothetical_pnl_proxy"]
    # Normalize residuals by modeled P&L magnitude plus a small tail floor so ratios are not
    # dominated by near-zero P&L days. This is a stable review proxy, not a formal PLA test.
    tail_floor = max(float(np.quantile(np.abs(df["hypothetical_pnl_proxy"]), 0.75)), 1.0) * 0.10
    denom = np.maximum(np.abs(df["hypothetical_pnl_proxy"]) + tail_floor, 1.0)
    df["absolute_unexplained_ratio"] = np.abs(df["unexplained_pnl_proxy"]) / denom
    df["dominant_loss_factor"] = df[["rates_loss", "corporate_credit_loss", "securitized_proxy_loss"]].abs().idxmax(axis=1).str.replace("_loss", "", regex=False)

    # A P&L attribution-style proxy: low unexplained ratio and strong correlation indicate better model explainability.
    corr = float(np.corrcoef(df["actual_pnl_proxy"], df["hypothetical_pnl_proxy"])[0, 1]) if len(df) > 2 else 1.0
    summary = {
        "observations": int(len(df)),
        "actual_hypothetical_corr": corr,
        "mean_absolute_unexplained_ratio": float(df["absolute_unexplained_ratio"].mean()),
        "p95_absolute_unexplained_ratio": float(df["absolute_unexplained_ratio"].quantile(0.95)),
        "unexplained_ratio_gate": 0.20,
        "correlation_gate": 0.90,
        "pla_proxy_status": "PASS" if corr >= 0.90 and float(df["absolute_unexplained_ratio"].quantile(0.95)) <= 0.20 else "REVIEW",
    }
    return df, summary
