from __future__ import annotations

import pandas as pd


def challenger_selection(backtest_df: pd.DataFrame, corrected_df: pd.DataFrame, envelope: float, false_safe: dict) -> pd.DataFrame:
    """Rank candidate VaR model variants using transparent review metrics."""
    if backtest_df.empty:
        return pd.DataFrame(columns=["candidate", "exception_rate", "false_safe_rate", "coverage_overreach_proxy", "review_score", "selected"])
    base_rate = float(backtest_df["exception"].mean())
    corr_rate = float(corrected_df["corrected_exception"].mean()) if not corrected_df.empty and "corrected_exception" in corrected_df else base_rate
    env_rate = float(false_safe.get("envelope_exception_rate", corr_rate))
    # Overreach proxy rewards lower exceptions but penalizes unnecessary conservatism.
    rows = [
        {"candidate": "vanilla_historical_var", "exception_rate": base_rate, "false_safe_rate": base_rate, "coverage_overreach_proxy": 0.000, "complexity_penalty": 0.00},
        {"candidate": "residual_corrected_var", "exception_rate": corr_rate, "false_safe_rate": corr_rate, "coverage_overreach_proxy": max(0.0, corr_rate - base_rate) + 0.004, "complexity_penalty": 0.004},
        {"candidate": "conservative_tail_envelope", "exception_rate": env_rate, "false_safe_rate": float(false_safe.get("false_safe_rate", env_rate)), "coverage_overreach_proxy": float(false_safe.get("overreach_proxy", 0.025)), "complexity_penalty": 0.02},
    ]
    out = pd.DataFrame(rows)
    out["target_exception_rate"] = 0.01
    out["exception_excess"] = (out["exception_rate"] - out["target_exception_rate"]).clip(lower=0.0)
    out["exception_shortfall"] = (out["target_exception_rate"] - out["exception_rate"]).clip(lower=0.0)
    # Penalize undercoverage more heavily than modest conservatism; this is closer to
    # market-risk review priorities where false-safe risk is worse than mild overreach.
    out["review_score"] = out["exception_excess"] * 2.0 + out["exception_shortfall"] * 0.35 + out["false_safe_rate"] * 0.30 + out["coverage_overreach_proxy"] * 0.25 + out["complexity_penalty"]
    best_idx = out["review_score"].idxmin()
    out["selected"] = False
    out.loc[best_idx, "selected"] = True
    out["selection_rationale"] = out.apply(
        lambda r: "selected champion for review" if r["selected"] else "retained as challenger / benchmark", axis=1
    )
    return out.sort_values("review_score")
