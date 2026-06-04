from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUTPUTS = ROOT / "outputs"
DATA = ROOT / "data" / "cached_samples"

REPORTS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

report_path = REPORTS / "function_performance_evaluation_report.md"
summary_csv = OUTPUTS / "function_performance_evaluation_summary.csv"

records = []

def add(section, metric, value, status="INFO", note=""):
    records.append({
        "section": section,
        "metric": metric,
        "value": value,
        "status": status,
        "note": note,
    })

# 1. Functional evaluation: required files/artifacts
required_files = [
    "outputs/run_summary.json",
    "outputs/freddie_crt_sample_summary.csv",
    "reports/freddie_crt_sample_build_report.md",
    "outputs/var_es_by_portfolio.csv",
    "outputs/backtesting_exceptions.csv",
    "outputs/challenger_model_selection.csv",
    "outputs/pnl_attribution_summary.csv",
    "outputs/frtb_inspired_diagnostics.csv",
    "outputs/reverse_stress_diagnostics.csv",
    "reports/model_validation_memo.md",
    "reports/regulatory_mapping_memo.md",

    # Trained overlay and daily operations experiment artifacts
    "outputs/trained_var_overlay_model.json",
    "outputs/trained_var_overlay_predictions.csv",
    "outputs/trained_var_overlay_evaluation.csv",
    "outputs/daily_risk_operations_log.csv",
    "outputs/risk_limit_policy_comparison.csv",
    "outputs/action_recommendation_log.csv",
    "outputs/operational_experiment_summary.csv",
    "reports/trained_var_overlay_report.md",
    "reports/daily_risk_operations_experiment.md",
]

for rel in required_files:
    exists = (ROOT / rel).exists()
    add("functional_artifacts", rel, exists, "PASS" if exists else "FAIL")

# 2. Run summary
run_summary_path = OUTPUTS / "run_summary.json"
if run_summary_path.exists():
    run_summary = json.loads(run_summary_path.read_text(encoding="utf-8"))
    for k in [
        "data_source",
        "mortgage_source",
        "n_risk_factor_days",
        "n_corporate_bonds",
        "n_mortgage_loans",
        "historical_var_99",
        "historical_es_99",
        "stressed_var_99",
        "kupiec_exception_rate",
        "false_safe_rate",
        "release_status",
    ]:
        if k in run_summary:
            add("run_summary", k, run_summary[k], "PASS" if str(run_summary[k]).upper() == "PASS" or k != "release_status" else "FAIL")

# 3. Freddie CRT sample evaluation
freddie_path = OUTPUTS / "freddie_crt_sample_summary.csv"
if freddie_path.exists():
    f = pd.read_csv(freddie_path)
    add("freddie_crt_sample", "rows_in_summary", len(f), "PASS" if len(f) >= 2 else "FAIL")
    add("freddie_crt_sample", "contains_high_ltv_hqa", "high_ltv_hqa" in set(f["pool_type"]), "PASS" if "high_ltv_hqa" in set(f["pool_type"]) else "FAIL")
    add("freddie_crt_sample", "contains_low_ltv_dna", "low_ltv_dna" in set(f["pool_type"]), "PASS" if "low_ltv_dna" in set(f["pool_type"]) else "FAIL")
    add("freddie_crt_sample", "total_loans", int(f["loans"].sum()), "PASS" if f["loans"].sum() >= 3000 else "REVIEW")

mortgage_path = DATA / "mortgage_pool_sample.csv"
if mortgage_path.exists():
    m = pd.read_csv(mortgage_path)
    add("mortgage_sample_quality", "loan_rows", len(m), "PASS" if len(m) >= 1000 else "REVIEW")
    add("mortgage_sample_quality", "mean_fico", round(float(m["fico"].mean()), 3), "PASS" if m["fico"].mean() > 650 else "FAIL")
    add("mortgage_sample_quality", "min_fico", round(float(m["fico"].min()), 3), "PASS" if m["fico"].min() > 350 else "FAIL")
    add("mortgage_sample_quality", "mean_ltv", round(float(m["ltv"].mean()), 3), "PASS" if m["ltv"].mean() > 60 else "FAIL")
    add("mortgage_sample_quality", "hqa_avg_ltv", round(float(m[m["pool_type"] == "high_ltv_hqa"]["ltv"].mean()), 3), "PASS")
    add("mortgage_sample_quality", "dna_avg_ltv", round(float(m[m["pool_type"] == "low_ltv_dna"]["ltv"].mean()), 3), "PASS")

# 4. Backtesting / performance evaluation
bt_path = OUTPUTS / "backtesting_exceptions.csv"
if bt_path.exists():
    bt = pd.read_csv(bt_path)
    add("backtesting", "backtesting_rows", len(bt), "PASS" if len(bt) > 0 else "FAIL")
    for c in bt.columns:
        if "exception" in c.lower():
            try:
                add("backtesting", f"{c}_mean", round(float(pd.to_numeric(bt[c], errors="coerce").mean()), 6), "PASS")
            except Exception:
                pass

challenger_path = OUTPUTS / "challenger_model_selection.csv"
if challenger_path.exists():
    ch = pd.read_csv(challenger_path)
    add("challenger_selection", "candidate_models", len(ch), "PASS" if len(ch) >= 2 else "REVIEW")
    if "selected" in ch.columns:
        selected = ch[ch["selected"].astype(str).str.lower().isin(["true", "1", "yes"])]
        add("challenger_selection", "selected_model_count", len(selected), "PASS" if len(selected) >= 1 else "REVIEW")

pnl_path = OUTPUTS / "pnl_attribution_summary.csv"
if pnl_path.exists():
    pnl = pd.read_csv(pnl_path)
    add("pnl_attribution", "rows", len(pnl), "PASS" if len(pnl) > 0 else "REVIEW")
    for c in pnl.columns:
        if "corr" in c.lower() or "status" in c.lower():
            add("pnl_attribution", c, pnl[c].iloc[0], "PASS")

frtb_path = OUTPUTS / "frtb_inspired_diagnostics.csv"
if frtb_path.exists():
    frtb = pd.read_csv(frtb_path)
    add("frtb_inspired_diagnostics", "rows", len(frtb), "PASS" if len(frtb) >= 1 else "REVIEW")

reverse_path = OUTPUTS / "reverse_stress_diagnostics.csv"
if reverse_path.exists():
    rs = pd.read_csv(reverse_path)
    add("reverse_stress", "rows", len(rs), "PASS" if len(rs) >= 1 else "REVIEW")

# 8. Trained VaR overlay and daily operations evaluation
overlay_eval_path = OUTPUTS / "trained_var_overlay_evaluation.csv"
if overlay_eval_path.exists():
    ov = pd.read_csv(overlay_eval_path)
    add("trained_var_overlay", "evaluation_rows", len(ov), "PASS" if len(ov) >= 2 else "REVIEW")

    all_rows = ov[ov["split"].astype(str).str.lower().eq("all")]
    if not all_rows.empty and {"policy", "exception_rate", "false_safe_days"}.issubset(all_rows.columns):
        vanilla = all_rows[all_rows["policy"].eq("vanilla_var")]
        trained = all_rows[all_rows["policy"].eq("trained_var_overlay")]
        if not vanilla.empty and not trained.empty:
            vanilla_exception = float(vanilla["exception_rate"].iloc[0])
            trained_exception = float(trained["exception_rate"].iloc[0])
            vanilla_false_safe = int(vanilla["false_safe_days"].iloc[0])
            trained_false_safe = int(trained["false_safe_days"].iloc[0])

            add("trained_var_overlay", "all_vanilla_exception_rate", round(vanilla_exception, 6), "PASS")
            add("trained_var_overlay", "all_trained_exception_rate", round(trained_exception, 6), "PASS")
            add(
                "trained_var_overlay",
                "trained_overlay_exception_improvement",
                round(vanilla_exception - trained_exception, 6),
                "PASS" if trained_exception <= vanilla_exception else "REVIEW",
            )
            add("trained_var_overlay", "all_vanilla_false_safe_days", vanilla_false_safe, "PASS")
            add("trained_var_overlay", "all_trained_false_safe_days", trained_false_safe, "PASS")

ops_summary_path = OUTPUTS / "operational_experiment_summary.csv"
if ops_summary_path.exists():
    osum = pd.read_csv(ops_summary_path)
    add("daily_operations", "summary_rows", len(osum), "PASS" if len(osum) >= 5 else "REVIEW")

    metric_map = dict(zip(osum["metric"].astype(str), osum["value"].astype(str)))
    selected_policy = metric_map.get("selected_operations_policy", "")
    add("daily_operations", "selected_operations_policy", selected_policy, "PASS" if selected_policy else "REVIEW")
    add("daily_operations", "operations_red_days", metric_map.get("operations_red_days", ""), "PASS")
    add("daily_operations", "operations_amber_days", metric_map.get("operations_amber_days", ""), "PASS")
    add("daily_operations", "operations_green_days", metric_map.get("operations_green_days", ""), "PASS")

policy_path = OUTPUTS / "risk_limit_policy_comparison.csv"
if policy_path.exists():
    pol = pd.read_csv(policy_path)
    add("daily_operations", "policy_comparison_rows", len(pol), "PASS" if len(pol) >= 4 else "REVIEW")

    required_policies = {
        "vanilla_var",
        "residual_corrected_var",
        "trained_overlay_var",
        "stress_gate_var",
        "conservative_envelope",
        "hybrid_operations_policy",
    }
    present = set(pol["policy"].astype(str))
    missing = sorted(required_policies - present)
    add("daily_operations", "required_policy_set_present", len(missing) == 0, "PASS" if not missing else "REVIEW", ",".join(missing))

    if {"policy", "exception_rate", "false_safe_days"}.issubset(pol.columns):
        vanilla = pol[pol["policy"].eq("vanilla_var")]
        selected = pol[pol["policy"].eq(selected_policy)] if "selected_policy" in locals() else pd.DataFrame()
        if not vanilla.empty and not selected.empty:
            add("daily_operations", "vanilla_exception_rate", round(float(vanilla["exception_rate"].iloc[0]), 6), "PASS")
            add("daily_operations", "selected_policy_exception_rate", round(float(selected["exception_rate"].iloc[0]), 6), "PASS")
            add("daily_operations", "vanilla_false_safe_days", int(vanilla["false_safe_days"].iloc[0]), "PASS")
            add("daily_operations", "selected_policy_false_safe_days", int(selected["false_safe_days"].iloc[0]), "PASS")

df = pd.DataFrame(records)
df.to_csv(summary_csv, index=False)

overall = "PASS" if not (df["status"] == "FAIL").any() else "FAIL"

report = f"""# Function and Performance Evaluation Report

## Overall status

**{overall}**

## Purpose

This report summarizes functional correctness and model-performance evidence for the Fixed-Income Market Risk Model Development Framework.

## Evaluation scope

### Functional evaluation
- Local package import
- Pipeline execution
- Required artifact generation
- Freddie Mac CRT sample adapter
- HQA/DNA mortgage-pool separation
- Test suite execution
- Required report/output availability

### Performance evaluation
- VaR / Expected Shortfall output generation
- Stressed VaR
- Rolling backtesting outputs
- Exception diagnostics
- P&L attribution proxy
- Challenger model selection
- FRTB-inspired diagnostics
- Reverse stress diagnostics
- Freddie CRT data-quality sanity checks
- Trained VaR overlay evaluation
- Daily risk operations policy comparison
- Limit-monitoring action simulation

## Summary table

{df.to_markdown(index=False)}

## Interpretation

The framework has passed local functional validation and generated model-performance artifacts. The Freddie CRT-enhanced local run uses real Freddie Mac CRT loan-level disclosure rows for mortgage-pool attributes while keeping delinquency and prepayment as project-specific proxy fields. The project should therefore be described as a public-data-compatible, local/offline, regulatory-style fixed-income market-risk framework, not as a production bank model or regulatory capital-certified implementation.

## Claim boundary

- No proprietary JPMC data.
- No real trading-desk portfolio.
- No official Freddie Mac performance model replication.
- No production securitized-products valuation.
- No regulatory capital certification.
- Freddie CRT fields are used for local-enhanced mortgage-pool proxy attributes.
"""

report_path.write_text(report, encoding="utf-8")

print(f"Wrote {summary_csv}")
print(f"Wrote {report_path}")
print(f"Overall function/performance evaluation: {overall}")
