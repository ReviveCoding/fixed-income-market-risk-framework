from __future__ import annotations

import pandas as pd


def decide_release(backtest_summary: dict, false_safe_rate: float, required_reports_found: int) -> tuple[str, list[str]]:
    reasons = []
    exc_rate = float(backtest_summary.get("kupiec_exception_rate", 0.0))
    kup_p = float(backtest_summary.get("kupiec_p_value", 1.0))
    if exc_rate > 0.025:
        reasons.append(f"99% VaR exception rate {exc_rate:.3f} exceeds review threshold 0.025")
    if kup_p < 0.05:
        reasons.append(f"Kupiec POF p-value {kup_p:.3f} indicates possible VaR calibration issue")
    if false_safe_rate > 0.10:
        reasons.append(f"False-safe rate {false_safe_rate:.3f} exceeds threshold 0.10")
    if required_reports_found < 8:
        reasons.append("Required governance reports are incomplete")
    if any("exceeds" in r or "incomplete" in r for r in reasons):
        return "BLOCK", reasons
    if reasons:
        return "REVIEW", reasons
    return "PASS", ["All release-gate checks passed under offline synthetic/public-compatible boundary"]
