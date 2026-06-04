from __future__ import annotations

import pandas as pd


def securitized_stress_grid(tranche_summary: pd.DataFrame) -> pd.DataFrame:
    """Create a transparent CPR/default/severity/liquidity sensitivity grid.

    The grid is intentionally proxy-based: it validates monotonicity and tranche
    sensitivity without claiming production MBS/ABS valuation.
    """
    base_loss = float(tranche_summary["total_loss"].sum())
    exposure = float(tranche_summary["ending_outstanding"].sum() + tranche_summary["total_principal"].sum())
    rows = []
    for prepay_mult in [0.5, 1.0, 1.5]:
        for default_mult in [0.75, 1.0, 2.0, 3.0]:
            for severity_mult in [0.75, 1.0, 1.5]:
                for liquidity_mult in [1.0, 1.5, 2.0]:
                    credit_loss = base_loss * default_mult * severity_mult
                    liquidity_loss = exposure * 0.000015 * 75.0 * liquidity_mult
                    # Faster prepay reduces outstanding risk exposure but can reduce excess-spread protection.
                    prepay_effect = 1.0 + (1.0 - prepay_mult) * 0.10
                    total_loss = (credit_loss + liquidity_loss) * prepay_effect
                    rows.append({
                        "prepayment_multiplier": prepay_mult,
                        "default_multiplier": default_mult,
                        "severity_multiplier": severity_mult,
                        "liquidity_spread_multiplier": liquidity_mult,
                        "proxy_stress_loss": total_loss,
                    })
    df = pd.DataFrame(rows)
    df["stress_rank"] = df["proxy_stress_loss"].rank(method="dense", ascending=False).astype(int)
    return df.sort_values("proxy_stress_loss", ascending=False)


def securitized_grid_quality_checks(grid: pd.DataFrame) -> pd.DataFrame:
    checks = []
    for axis in ["default_multiplier", "severity_multiplier", "liquidity_spread_multiplier"]:
        grouped = grid.groupby(axis)["proxy_stress_loss"].mean().sort_index()
        monotonic = bool(grouped.is_monotonic_increasing)
        checks.append({
            "check": f"monotonic_mean_loss_by_{axis}",
            "passed": monotonic,
            "detail": "Mean proxy stress loss should increase with worsening stress multiplier.",
        })
    return pd.DataFrame(checks)
