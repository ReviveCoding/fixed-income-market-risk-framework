from __future__ import annotations

import numpy as np
import pandas as pd

RATING_SPREAD_COL = {"A": "a_spread_bp", "BBB": "bbb_spread_bp", "BB": "bb_spread_bp", "B": "b_spread_bp", "CCC": "ccc_spread_bp"}


def generate_corporate_bonds(n: int = 240, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ratings = rng.choice(["A", "BBB", "BB", "B", "CCC"], n, p=[0.20, 0.35, 0.20, 0.18, 0.07])
    sectors = rng.choice(["Financials", "Industrials", "Utilities", "Energy", "Consumer"], n)
    maturity = rng.choice([2, 4, 6, 8, 12], n, p=[0.18, 0.25, 0.25, 0.20, 0.12])
    coupon = np.clip(rng.normal(5.0, 1.0, n) + np.array([0 if r in ["A", "BBB"] else 1.2 for r in ratings]), 2.0, 11.0)
    notional = rng.choice([1_000_000, 2_000_000, 5_000_000, 10_000_000], n, p=[0.35, 0.30, 0.25, 0.10])
    return pd.DataFrame({
        "bond_id": [f"CB{i:04d}" for i in range(n)],
        "rating": ratings,
        "sector": sectors,
        "maturity_years": maturity,
        "coupon_pct": coupon.round(4),
        "notional": notional,
    })


def price_fixed_rate_bond(face: float, coupon_pct: float, maturity_years: int, discount_rate_pct: float, spread_pct: float) -> float:
    y = (discount_rate_pct + spread_pct) / 100.0
    c = coupon_pct / 100.0 * face
    times = np.arange(1, maturity_years + 1)
    cashflows = np.repeat(c, maturity_years)
    cashflows[-1] += face
    return float(np.sum(cashflows / (1 + y) ** times))


def compute_sensitivities(positions: pd.DataFrame, rates: pd.DataFrame, spreads: pd.DataFrame) -> pd.DataFrame:
    latest_rate = float(rates.sort_values("date")["DGS5"].iloc[-1])
    latest_spreads = spreads.sort_values("date").iloc[-1].to_dict()
    rows = []
    for _, row in positions.iterrows():
        rating = row["rating"]
        spread_col = {"A": "A_OAS", "BBB": "BBB_OAS", "BB": "BB_OAS", "B": "B_OAS", "CCC": "CCC_OAS"}[rating]
        spread = float(latest_spreads[spread_col])
        base = price_fixed_rate_bond(100, row["coupon_pct"], int(row["maturity_years"]), latest_rate, spread)
        up_rate = price_fixed_rate_bond(100, row["coupon_pct"], int(row["maturity_years"]), latest_rate + 0.01, spread)
        up_spread = price_fixed_rate_bond(100, row["coupon_pct"], int(row["maturity_years"]), latest_rate, spread + 0.01)
        market_value = base / 100.0 * row["notional"]
        dv01 = max((base - up_rate) / 100.0 * row["notional"], 0.0)
        cs01 = max((base - up_spread) / 100.0 * row["notional"], 0.0)
        duration_proxy = dv01 / max(market_value, 1.0) * 10000
        rows.append({**row.to_dict(), "price": base, "market_value": market_value, "dv01": dv01, "cs01": cs01, "oas01": cs01, "duration_proxy": duration_proxy})
    return pd.DataFrame(rows)


def corporate_daily_losses(sens: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, f in panel.iterrows():
        rate_loss = float(sens["dv01"].sum() * f["rate_level_bp"])
        spread_loss = 0.0
        for rating, factor_col in RATING_SPREAD_COL.items():
            spread_loss += float(sens.loc[sens["rating"] == rating, "cs01"].sum() * f[factor_col])
        rows.append({"date": f["date"], "rates_loss": rate_loss, "corporate_credit_loss": spread_loss, "corporate_total_loss": rate_loss + spread_loss})
    return pd.DataFrame(rows)
