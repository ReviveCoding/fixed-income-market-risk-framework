from __future__ import annotations

import numpy as np
import pandas as pd


def build_tranche_cashflows(pool: pd.DataFrame, months: int = 60) -> tuple[pd.DataFrame, pd.DataFrame]:
    total_balance = float(pool["balance"].sum())
    avg_coupon = float(np.average(pool["coupon"], weights=pool["balance"])) / 100.0
    base_default = float(np.average(pool["delinquency_proxy"], weights=pool["balance"])) * 0.012
    base_prepay = float(np.average(pool["prepay_score"], weights=pool["balance"])) * 0.10
    smm = 1 - (1 - base_prepay) ** (1 / 12)
    monthly_default = base_default / 12
    severity = 0.35

    tranche_balances = {"Senior": total_balance * 0.80, "Mezzanine": total_balance * 0.15, "Equity": total_balance * 0.05}
    records = []
    outstanding_pool = total_balance
    tranche_outstanding = tranche_balances.copy()

    for m in range(1, months + 1):
        sched_prin = outstanding_pool / max(1, (360 - m + 1))
        prepay = max(outstanding_pool - sched_prin, 0) * smm
        default = outstanding_pool * monthly_default
        loss = default * severity
        interest = outstanding_pool * avg_coupon / 12
        principal = sched_prin + prepay + max(default - loss, 0)
        outstanding_pool = max(outstanding_pool - principal - loss, 0)

        # Allocate principal senior-first and losses reverse sequential.
        remaining_principal = principal
        principal_alloc = {}
        for tr in ["Senior", "Mezzanine", "Equity"]:
            paid = min(tranche_outstanding[tr], remaining_principal)
            tranche_outstanding[tr] -= paid
            remaining_principal -= paid
            principal_alloc[tr] = paid
        remaining_loss = loss
        loss_alloc = {}
        for tr in ["Equity", "Mezzanine", "Senior"]:
            absorbed = min(tranche_outstanding[tr], remaining_loss)
            tranche_outstanding[tr] -= absorbed
            remaining_loss -= absorbed
            loss_alloc[tr] = absorbed
        for tr in ["Senior", "Mezzanine", "Equity"]:
            records.append({
                "month": m,
                "tranche": tr,
                "interest_cashflow": interest * (tranche_balances[tr] / total_balance),
                "principal_cashflow": principal_alloc[tr],
                "loss_allocated": loss_alloc.get(tr, 0.0),
                "tranche_outstanding": tranche_outstanding[tr],
            })
    cashflows = pd.DataFrame(records)
    summary = cashflows.groupby("tranche", as_index=False).agg(
        total_interest=("interest_cashflow", "sum"),
        total_principal=("principal_cashflow", "sum"),
        total_loss=("loss_allocated", "sum"),
        ending_outstanding=("tranche_outstanding", "last"),
    )
    tmp = cashflows.assign(weighted_month=lambda d: d["month"] * d["principal_cashflow"])
    wal_num = tmp.groupby("tranche", as_index=False)["weighted_month"].sum()
    wal_den = tmp.groupby("tranche", as_index=False)["principal_cashflow"].sum()
    wal = wal_num.merge(wal_den, on="tranche")
    wal["wal_years"] = wal["weighted_month"] / wal["principal_cashflow"].clip(lower=1.0) / 12
    wal = wal[["tranche", "wal_years"]]
    summary = summary.merge(wal, on="tranche", how="left")
    return cashflows, summary


def securitized_daily_losses(panel: pd.DataFrame, tranche_summary: pd.DataFrame) -> pd.DataFrame:
    # Proxy spread exposure: mezz/equity more sensitive to credit and liquidity shocks.
    exposure = float(tranche_summary["ending_outstanding"].sum() + tranche_summary["total_principal"].sum())
    rows = []
    for _, f in panel.iterrows():
        shock = 0.35 * f["rate_level_bp"] + 0.55 * f["credit_level_bp"] + 0.10 * f["credit_quality_slope_bp"]
        rows.append({"date": f["date"], "securitized_proxy_loss": exposure * shock * 0.000015})
    return pd.DataFrame(rows)


def securitized_scenario_stress(tranche_summary: pd.DataFrame) -> pd.DataFrame:
    base_loss = float(tranche_summary["total_loss"].sum())
    rows = []
    for name, mult in {"base": 1.0, "high_prepay": 0.8, "high_default": 2.2, "high_severity": 1.7, "liquidity_spread": 1.35}.items():
        rows.append({"scenario": name, "proxy_tranche_loss": base_loss * mult, "loss_multiplier": mult})
    return pd.DataFrame(rows)
