from __future__ import annotations

import numpy as np
import pandas as pd

RATE_SERIES = ["DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]
SPREAD_SERIES = ["IG_OAS", "HY_OAS", "A_OAS", "BBB_OAS", "BB_OAS", "B_OAS", "CCC_OAS"]


def generate_market_data(n_days: int = 900, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate deterministic, realistic-enough fallback rate and spread panels.

    Values are in percentage points, similar to FRED convention.
    """
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n_days)

    base_curve = np.array([4.8, 4.75, 4.65, 4.45, 4.20, 4.05, 3.95, 4.00, 4.10, 4.35, 4.45])
    rate_level = np.zeros(n_days)
    slope = np.zeros(n_days)
    curvature = np.zeros(n_days)
    # Mild regime change and crisis-like window for testing stressed VaR.
    for t in range(1, n_days):
        shock_scale = 0.035 if 520 <= t <= 650 else 0.012
        rate_level[t] = 0.985 * rate_level[t-1] + rng.normal(0, shock_scale)
        slope[t] = 0.970 * slope[t-1] + rng.normal(0, shock_scale * 0.7)
        curvature[t] = 0.950 * curvature[t-1] + rng.normal(0, shock_scale * 0.4)
    maturity_loading = np.linspace(-0.5, 0.5, len(RATE_SERIES))
    curve = base_curve + rate_level[:, None] + slope[:, None] * maturity_loading + curvature[:, None] * (maturity_loading ** 2)
    rates = pd.DataFrame(curve, columns=RATE_SERIES)
    rates.insert(0, "date", dates)

    spread_base = np.array([1.20, 4.00, 0.90, 1.50, 3.00, 4.80, 8.50])
    credit_level = np.zeros(n_days)
    hy_extra = np.zeros(n_days)
    for t in range(1, n_days):
        shock_scale = 0.05 if 520 <= t <= 650 else 0.018
        credit_level[t] = 0.990 * credit_level[t-1] + abs(rng.normal(0, shock_scale)) * (1 if rng.random() < 0.52 else -0.35)
        hy_extra[t] = 0.985 * hy_extra[t-1] + rng.normal(0, shock_scale * 1.8)
    spread_load = np.array([0.55, 1.8, 0.4, 0.75, 1.25, 1.75, 2.4])
    spreads_arr = spread_base + credit_level[:, None] * spread_load + hy_extra[:, None] * np.array([0.0, 1.2, 0, 0.1, 0.7, 1.0, 1.4])
    spreads_arr = np.clip(spreads_arr, 0.2, None)
    spreads = pd.DataFrame(spreads_arr, columns=SPREAD_SERIES)
    spreads.insert(0, "date", dates)
    return rates, spreads


def generate_mortgage_pool(n_loans: int = 800, seed: int = 43) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    fico = np.clip(rng.normal(720, 55, n_loans), 560, 820)
    ltv = np.clip(rng.normal(76, 13, n_loans), 35, 115)
    coupon = np.clip(rng.normal(5.25, 0.9, n_loans), 2.0, 8.5)
    balance = np.clip(rng.lognormal(mean=12.35, sigma=0.45, size=n_loans), 50_000, 950_000)
    term_months = rng.choice([180, 240, 300, 360], size=n_loans, p=[0.12, 0.10, 0.08, 0.70])
    delinquency_proxy = np.clip((ltv - 70) / 75 + (680 - fico) / 260 + rng.normal(0, 0.08, n_loans), 0, 1)
    prepay_score = np.clip((coupon - 4.0) / 5.0 + (fico - 650) / 400 + rng.normal(0, 0.1, n_loans), 0, 1)
    return pd.DataFrame({
        "loan_id": [f"L{i:05d}" for i in range(n_loans)],
        "balance": balance.round(2),
        "coupon": coupon.round(4),
        "term_months": term_months,
        "fico": fico.round(0).astype(int),
        "ltv": ltv.round(2),
        "delinquency_proxy": delinquency_proxy.round(4),
        "prepay_score": prepay_score.round(4),
    })
