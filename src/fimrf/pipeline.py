from __future__ import annotations

from pathlib import Path
import pandas as pd

from fimrf.utils import ensure_dirs, save_table, write_json
from fimrf.data_ingestion.source_registry import load_market_data, load_mortgage_pool
from fimrf.data_validation.data_quality_rules import validate_time_series
from fimrf.risk_factors.build_curve_factors import build_curve_factors
from fimrf.risk_factors.build_credit_spread_factors import build_credit_spread_factors
from fimrf.risk_factors.covariance import merge_risk_factors
from fimrf.instruments.corporate_bond import generate_corporate_bonds, compute_sensitivities, corporate_daily_losses
from fimrf.instruments.securitized_proxy import build_tranche_cashflows, securitized_daily_losses, securitized_scenario_stress
from fimrf.instruments.securitized_grid import securitized_stress_grid, securitized_grid_quality_checks
from fimrf.risk_models.var import historical_var, expected_shortfall, monte_carlo_var, stressed_var
from fimrf.risk_models.stress_testing import run_stress_scenarios
from fimrf.backtesting.tests import rolling_var_backtest
from fimrf.model_development.assumption_sensitivity import assumption_sensitivity
from fimrf.model_development.backtesting_enhancements import traffic_light_backtest, exception_attribution, var_stability_diagnostics
from fimrf.model_development.pnl_attribution_proxy import pnl_attribution_proxy
from fimrf.model_development.frtb_inspired_diagnostics import frtb_inspired_diagnostics
from fimrf.model_development.challenger_selection import challenger_selection
from fimrf.model_development.reverse_stress import reverse_stress_diagnostics
from fimrf.reproducibility.manifest import build_reproducibility_manifest
from fimrf.specialty.market_health_timestep import assign_market_health_timestep
from fimrf.specialty.residual_var_correction import residual_var_correction
from fimrf.specialty.conservative_risk_envelope import conservative_envelope, false_safe_metrics
from fimrf.specialty.specialty_ablation import build_specialty_ablation
from fimrf.model_development.release_gate import decide_release
from fimrf.governance.reports import generate_reports
from fimrf.governance.enhancement_reports import generate_enhancement_reports


def run_pipeline(root: str | Path | None = None) -> dict:
    root = Path(root or Path(__file__).resolve().parents[2])
    outputs = root / "outputs"
    reports = root / "reports"
    processed = root / "data" / "processed"
    ensure_dirs(outputs, reports, processed)

    rates, spreads, source_mode = load_market_data(root)
    mortgage_pool, mortgage_source_mode = load_mortgage_pool(root)

    rate_checks, rate_report = validate_time_series(rates, "rates")
    spread_checks, spread_report = validate_time_series(spreads, "spreads")
    data_quality = pd.concat([rate_checks, spread_checks], ignore_index=True)
    save_table(data_quality, outputs / "data_quality_exceptions.csv")

    curve = build_curve_factors(rates)
    credit = build_credit_spread_factors(spreads)
    panel = merge_risk_factors(curve, credit)
    save_table(panel, outputs / "risk_factor_panel.parquet")

    positions = generate_corporate_bonds()
    sens = compute_sensitivities(positions, rates, spreads)
    save_table(positions, outputs / "corporate_bond_positions.csv")
    save_table(sens, outputs / "corporate_credit_sensitivities.csv")

    cashflows, tranche_summary = build_tranche_cashflows(mortgage_pool)
    sec_stress = securitized_scenario_stress(tranche_summary)
    save_table(mortgage_pool, outputs / "mortgage_pool_features.csv")
    save_table(cashflows, outputs / "securitized_tranche_cashflows.csv")
    save_table(sec_stress, outputs / "securitized_stress_results.csv")
    sec_grid = securitized_stress_grid(tranche_summary)
    sec_grid_checks = securitized_grid_quality_checks(sec_grid)
    save_table(sec_grid, outputs / "securitized_stress_grid.csv")
    save_table(sec_grid_checks, outputs / "securitized_grid_quality_checks.csv")

    corp_losses = corporate_daily_losses(sens, panel)
    sec_losses = securitized_daily_losses(panel, tranche_summary)
    losses = corp_losses.merge(sec_losses, on="date", how="inner")
    losses["total_loss"] = losses["rates_loss"] + losses["corporate_credit_loss"] + losses["securitized_proxy_loss"]
    losses = assign_market_health_timestep(losses)
    save_table(losses, outputs / "portfolio_loss_panel.csv")

    hist95 = historical_var(losses["total_loss"], 0.95)
    hist99 = historical_var(losses["total_loss"], 0.99)
    es99 = expected_shortfall(losses["total_loss"], 0.99)
    mc_g_var, mc_g_es = monte_carlo_var(losses["total_loss"], 0.99, student_t_df=None)
    mc_t_var, mc_t_es = monte_carlo_var(losses["total_loss"], 0.99, student_t_df=5)
    stressed = stressed_var(losses, "total_loss", 250, 0.99)
    var_table = pd.DataFrame([{
        "portfolio": "total_fixed_income_proxy",
        "historical_var_95": hist95,
        "historical_var_99": hist99,
        "historical_es_99": es99,
        "mc_gaussian_var_99": mc_g_var,
        "mc_gaussian_es_99": mc_g_es,
        "mc_student_t_var_99": mc_t_var,
        "mc_student_t_es_99": mc_t_es,
        "ten_day_scaled_var_99": hist99 * (10 ** 0.5),
        "stressed_var_99": stressed["stressed_var"],
    }])
    save_table(var_table, outputs / "var_es_by_portfolio.csv")
    save_table(pd.DataFrame([stressed]), outputs / "stressed_var_results.csv")

    stress_losses = run_stress_scenarios(sens, tranche_summary)
    save_table(stress_losses, outputs / "stress_loss_by_scenario.csv")
    reverse_stress = reverse_stress_diagnostics(stress_losses, hist99, es99)
    save_table(reverse_stress, outputs / "reverse_stress_diagnostics.csv")

    pnl_attr, pnl_summary = pnl_attribution_proxy(losses)
    save_table(pnl_attr, outputs / "pnl_attribution_proxy.csv")
    save_table(pd.DataFrame([pnl_summary]), outputs / "pnl_attribution_summary.csv")

    frtb_diag = frtb_inspired_diagnostics(losses)
    save_table(frtb_diag, outputs / "frtb_inspired_diagnostics.csv")

    backtest_df, backtest_summary = rolling_var_backtest(losses, "total_loss", 250, 0.99)
    save_table(backtest_df, outputs / "backtesting_exceptions.csv")
    save_table(pd.DataFrame([backtest_summary]), outputs / "kupiec_christoffersen_results.csv")
    traffic_light = traffic_light_backtest(backtest_df, evaluation_days=250)
    exception_attr = exception_attribution(losses, backtest_df)
    stability = var_stability_diagnostics(losses)
    save_table(pd.DataFrame([traffic_light]), outputs / "traffic_light_backtest.csv")
    save_table(exception_attr, outputs / "exception_attribution.csv")
    save_table(stability, outputs / "var_stability_diagnostics.csv")

    assumption = assumption_sensitivity(losses["total_loss"], 0.99)
    save_table(assumption, outputs / "assumption_sensitivity_matrix.csv")

    corrected_df, correction_multiplier = residual_var_correction(backtest_df)
    envelope = conservative_envelope(var_table)
    false_safe = false_safe_metrics(backtest_df, envelope)
    ablation = build_specialty_ablation(backtest_df, corrected_df, envelope)
    challengers = challenger_selection(backtest_df, corrected_df, envelope, false_safe)
    save_table(corrected_df, outputs / "corrected_backtesting_exceptions.csv")
    save_table(ablation, outputs / "specialty_ablation_table.csv")
    save_table(pd.DataFrame([{**false_safe, "correction_multiplier": correction_multiplier, "conservative_envelope": envelope}]), outputs / "false_safe_metrics.csv")
    save_table(challengers, outputs / "challenger_model_selection.csv")

    release_status, reasons = decide_release(backtest_summary, false_safe["false_safe_rate"], required_reports_found=15)
    findings = pd.DataFrame([
        {"finding_id": "F-001", "severity": "Medium" if release_status != "PASS" else "Low", "finding": r, "recommended_action": "Review threshold, assumptions, and compensating controls"}
        for r in reasons
    ])
    save_table(findings, outputs / "model_risk_findings.csv")
    write_json(outputs / "release_decision.json", {"release_status": release_status, "reasons": reasons})

    context = {
        "data_source": source_mode,
        "mortgage_source": mortgage_source_mode,
        "historical_var_99": hist99,
        "historical_es_99": es99,
        "stressed_var_99": stressed["stressed_var"],
        "release_status": release_status,
    }
    generate_reports(root, context)
    generate_enhancement_reports(root)
    manifest, manifest_meta = build_reproducibility_manifest(root)
    save_table(manifest, outputs / "reproducibility_manifest.csv")
    write_json(outputs / "reproducibility_metadata.json", manifest_meta)
    # Regenerate reports after manifest creation so the reproducibility report can include current hashes.
    generate_enhancement_reports(root)
    write_json(outputs / "run_summary.json", {
        **context,
        "n_risk_factor_days": int(len(panel)),
        "n_corporate_bonds": int(len(positions)),
        "n_mortgage_loans": int(len(mortgage_pool)),
        "kupiec_exception_rate": float(backtest_summary.get("kupiec_exception_rate", 0.0)),
        "false_safe_rate": false_safe["false_safe_rate"],
        "traffic_light": traffic_light.get("traffic_light", "unknown"),
        "traffic_light_exceptions": int(traffic_light.get("exceptions", 0)),
        "pnl_attribution_status": pnl_summary.get("pla_proxy_status", "unknown"),
        "pnl_actual_hypothetical_corr": float(pnl_summary.get("actual_hypothetical_corr", 0.0)),
        "frtb_diag_rows": int(len(frtb_diag)),
        "challenger_rows": int(len(challengers)),
        "reverse_stress_rows": int(len(reverse_stress)),
        "securitized_grid_rows": int(len(sec_grid)),
        "stability_windows": int(len(stability)),
        "reports_generated": len(list(reports.glob("*.md"))),
        "model_inventory_rows": int(len(pd.read_csv(outputs / "model_inventory.csv"))) if (outputs / "model_inventory.csv").exists() else 0,
        "public_source_catalog_rows": int(len(pd.read_csv(outputs / "public_data_source_catalog.csv"))) if (outputs / "public_data_source_catalog.csv").exists() else 0,
    })
    return {"root": str(root), "release_status": release_status, "run_summary": str(outputs / "run_summary.json")}


if __name__ == "__main__":
    print(run_pipeline())
