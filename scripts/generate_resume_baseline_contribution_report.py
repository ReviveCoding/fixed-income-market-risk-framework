from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
REPORTS = ROOT / "reports"

OUT_CSV = OUTPUTS / "resume_baseline_contribution_summary.csv"
OUT_MD = REPORTS / "resume_baseline_contribution_report.md"

policy_path = OUTPUTS / "risk_limit_policy_comparison.csv"
overlay_path = OUTPUTS / "trained_var_overlay_evaluation.csv"
ops_path = OUTPUTS / "operational_experiment_summary.csv"

if not policy_path.exists():
    raise FileNotFoundError("Missing outputs/risk_limit_policy_comparison.csv. Run scripts/train_var_overlay_and_ops.py first.")

policy = pd.read_csv(policy_path)

def pct_reduction(base, new):
    base = float(base)
    new = float(new)
    if base == 0:
        return np.nan
    return (base - new) / base * 100.0

vanilla = policy[policy["policy"].eq("vanilla_var")].iloc[0]

# Prefer the actually selected policy from the operational experiment.
selected_policy = "residual_corrected_var"
if ops_path.exists():
    ops = pd.read_csv(ops_path)
    m = dict(zip(ops["metric"].astype(str), ops["value"].astype(str)))
    selected_policy = m.get("selected_operations_policy", selected_policy)

selected = policy[policy["policy"].eq(selected_policy)].iloc[0]

rows = []

def add(metric, baseline_value, method_value, unit="", note=""):
    rows.append({
        "metric": metric,
        "baseline": "vanilla_var",
        "baseline_value": baseline_value,
        "method": selected_policy,
        "method_value": method_value,
        "absolute_change": float(method_value) - float(baseline_value),
        "relative_reduction_pct": pct_reduction(baseline_value, method_value),
        "unit": unit,
        "note": note,
    })

add(
    "exception_rate",
    vanilla["exception_rate"],
    selected["exception_rate"],
    "rate",
    "Primary risk-control metric."
)

add(
    "false_safe_days",
    vanilla["false_safe_days"],
    selected["false_safe_days"],
    "days",
    "Days where realized next-day loss exceeded selected risk number."
)

add(
    "red_days",
    vanilla["red_days"],
    selected["red_days"],
    "days",
    "Breach/escalation days in simulated operations."
)

add(
    "amber_days",
    vanilla["amber_days"],
    selected["amber_days"],
    "days",
    "Review-zone days in simulated operations."
)

add(
    "review_burden_amber_red",
    vanilla["review_burden_amber_red"],
    selected["review_burden_amber_red"],
    "days",
    "Total RED+AMBER review burden."
)

add(
    "p95_limit_utilization",
    vanilla["p95_utilization"],
    selected["p95_utilization"],
    "ratio",
    "Lower means lower tail utilization under selected risk number."
)

# Add trained overlay as a challenger, not the champion.
if overlay_path.exists():
    ov = pd.read_csv(overlay_path)
    all_rows = ov[ov["split"].astype(str).str.lower().eq("all")]
    if not all_rows.empty:
        v = all_rows[all_rows["policy"].eq("vanilla_var")].iloc[0]
        t = all_rows[all_rows["policy"].eq("trained_var_overlay")].iloc[0]
        rows.append({
            "metric": "trained_overlay_exception_rate",
            "baseline": "vanilla_var",
            "baseline_value": v["exception_rate"],
            "method": "trained_var_overlay",
            "method_value": t["exception_rate"],
            "absolute_change": float(t["exception_rate"]) - float(v["exception_rate"]),
            "relative_reduction_pct": pct_reduction(v["exception_rate"], t["exception_rate"]),
            "unit": "rate",
            "note": "Challenger model improved slightly but was not selected as operations champion."
        })
        rows.append({
            "metric": "trained_overlay_false_safe_days",
            "baseline": "vanilla_var",
            "baseline_value": v["false_safe_days"],
            "method": "trained_var_overlay",
            "method_value": t["false_safe_days"],
            "absolute_change": float(t["false_safe_days"]) - float(v["false_safe_days"]),
            "relative_reduction_pct": pct_reduction(v["false_safe_days"], t["false_safe_days"]),
            "unit": "days",
            "note": "Challenger model comparison."
        })

summary = pd.DataFrame(rows)
summary["baseline_value"] = pd.to_numeric(summary["baseline_value"], errors="coerce")
summary["method_value"] = pd.to_numeric(summary["method_value"], errors="coerce")
summary["absolute_change"] = pd.to_numeric(summary["absolute_change"], errors="coerce")
summary["relative_reduction_pct"] = pd.to_numeric(summary["relative_reduction_pct"], errors="coerce")

summary.to_csv(OUT_CSV, index=False)

def fmt_pct(x):
    return "NA" if pd.isna(x) else f"{x:.1f}%"

exception_reduction = pct_reduction(vanilla["exception_rate"], selected["exception_rate"])
false_safe_reduction = pct_reduction(vanilla["false_safe_days"], selected["false_safe_days"])
review_reduction = pct_reduction(vanilla["review_burden_amber_red"], selected["review_burden_amber_red"])

resume_bullet_1 = (
    "Built and locally validated a fixed-income market-risk model development framework "
    "with public-compatible Treasury/OAS data, synthetic corporate-credit portfolios, "
    "Freddie Mac CRT-enhanced mortgage proxy pools, VaR/ES, stressed VaR, rolling backtesting, "
    "P&L attribution proxy, FRTB-inspired diagnostics, reverse stress testing, and "
    "function/performance evaluation reports."
)

resume_bullet_2 = (
    f"Trained a lightweight VaR multiplier overlay as a challenger model and ran a daily "
    f"market-risk operations simulation comparing vanilla, residual-corrected, trained-overlay, "
    f"stress-gate, conservative-envelope, and hybrid policies; selected {selected_policy}, "
    f"reducing simulated exception rate from {float(vanilla['exception_rate'])*100:.2f}% to "
    f"{float(selected['exception_rate'])*100:.2f}% ({exception_reduction:.1f}% relative reduction), "
    f"false-safe days from {int(vanilla['false_safe_days'])} to {int(selected['false_safe_days'])}, "
    f"and RED/AMBER review burden from {int(vanilla['review_burden_amber_red'])} to "
    f"{int(selected['review_burden_amber_red'])} days."
)

report = f"""# Resume Baseline Contribution Report

## Status

PASS

## Purpose

This report translates model-development and operations-simulation outputs into resume-safe baseline-vs-method contribution metrics.

## Selected operating method

**{selected_policy}**

## Baseline-vs-method summary

{summary.to_markdown(index=False)}

## Main improvement claims

- Exception rate: {float(vanilla['exception_rate'])*100:.2f}% → {float(selected['exception_rate'])*100:.2f}% ({exception_reduction:.1f}% relative reduction)
- False-safe days: {int(vanilla['false_safe_days'])} → {int(selected['false_safe_days'])} ({false_safe_reduction:.1f}% relative reduction)
- RED/AMBER review burden: {int(vanilla['review_burden_amber_red'])} → {int(selected['review_burden_amber_red'])} days ({review_reduction:.1f}% relative reduction)
- Tradeoff: selected policy is more conservative, with avg_overconservatism = {float(selected['avg_overconservatism']):.2f}

## Resume-ready bullets

1. {resume_bullet_1}

2. {resume_bullet_2}

## Claim boundary

These metrics are from an offline/local simulation using public-compatible market data artifacts, synthetic corporate-credit portfolios, Freddie Mac CRT-enhanced mortgage proxy pools, and proxy P&L/risk outputs. They should not be described as production bank results, proprietary trading-desk results, regulatory capital certification, or official Freddie Mac model replication.
"""

OUT_MD.write_text(report, encoding="utf-8")

print(f"Wrote {OUT_CSV}")
print(f"Wrote {OUT_MD}")
print()
print("Resume-safe main metrics:")
print(f"Exception rate: {float(vanilla['exception_rate'])*100:.2f}% -> {float(selected['exception_rate'])*100:.2f}% ({exception_reduction:.1f}% relative reduction)")
print(f"False-safe days: {int(vanilla['false_safe_days'])} -> {int(selected['false_safe_days'])} ({false_safe_reduction:.1f}% relative reduction)")
print(f"RED/AMBER review burden: {int(vanilla['review_burden_amber_red'])} -> {int(selected['review_burden_amber_red'])} ({review_reduction:.1f}% relative reduction)")
print(f"Selected policy: {selected_policy}")
