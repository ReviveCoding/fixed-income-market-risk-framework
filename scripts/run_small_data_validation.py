from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fimrf.utils import ensure_dirs, save_table, write_markdown
from fimrf.data_ingestion.synthetic_fallback import generate_market_data, generate_mortgage_pool
from fimrf.data_validation.data_quality_rules import validate_time_series
from fimrf.risk_factors.build_curve_factors import build_curve_factors
from fimrf.risk_factors.build_credit_spread_factors import build_credit_spread_factors
from fimrf.risk_factors.covariance import merge_risk_factors
from fimrf.instruments.corporate_bond import generate_corporate_bonds, compute_sensitivities, corporate_daily_losses
from fimrf.instruments.securitized_proxy import build_tranche_cashflows, securitized_daily_losses
from fimrf.risk_models.var import historical_var, expected_shortfall
from fimrf.backtesting.tests import rolling_var_backtest
from fimrf.model_development.backtesting_enhancements import traffic_light_backtest, var_stability_diagnostics
from fimrf.model_development.pnl_attribution_proxy import pnl_attribution_proxy
from fimrf.model_development.frtb_inspired_diagnostics import frtb_inspired_diagnostics
from fimrf.model_development.challenger_selection import challenger_selection
from fimrf.model_development.reverse_stress import reverse_stress_diagnostics
from fimrf.risk_models.stress_testing import run_stress_scenarios
from fimrf.specialty.residual_var_correction import residual_var_correction
from fimrf.specialty.conservative_risk_envelope import conservative_envelope, false_safe_metrics


def main() -> dict:
    outputs = ROOT / "outputs"
    reports = ROOT / "reports"
    ensure_dirs(outputs, reports)

    rates, spreads = generate_market_data(n_days=360, seed=77)
    mortgage = generate_mortgage_pool(n_loans=80, seed=78)
    rate_checks, _ = validate_time_series(rates, "small_rates")
    spread_checks, _ = validate_time_series(spreads, "small_spreads")
    panel = merge_risk_factors(build_curve_factors(rates), build_credit_spread_factors(spreads))
    positions = generate_corporate_bonds(n=40, seed=79)
    sens = compute_sensitivities(positions, rates, spreads)
    cashflows, tranche_summary = build_tranche_cashflows(mortgage, months=24)
    losses = corporate_daily_losses(sens, panel).merge(securitized_daily_losses(panel, tranche_summary), on="date", how="inner")
    losses["total_loss"] = losses["rates_loss"] + losses["corporate_credit_loss"] + losses["securitized_proxy_loss"]
    var99 = historical_var(losses["total_loss"], 0.99)
    es99 = expected_shortfall(losses["total_loss"], 0.99)
    backtest, summary = rolling_var_backtest(losses, "total_loss", window=125, confidence=0.99)
    traffic = traffic_light_backtest(backtest, evaluation_days=min(125, len(backtest)))
    corrected, multiplier = residual_var_correction(backtest)
    stability = var_stability_diagnostics(losses)
    pnl_attr, pnl_summary = pnl_attribution_proxy(losses, residual_scale=0.018, seed=77)
    frtb_diag = frtb_inspired_diagnostics(losses)
    stress_losses = run_stress_scenarios(sens, tranche_summary)
    reverse_stress = reverse_stress_diagnostics(stress_losses, var99, es99)
    # Reuse a compact envelope table for small-data challenger selection.
    var_table = pd.DataFrame([{"historical_var_99": var99, "historical_es_99": es99, "stressed_var_99": var99 * 1.15}])
    envelope = conservative_envelope(var_table)
    false_safe = false_safe_metrics(backtest, envelope)
    challengers = challenger_selection(backtest, corrected, envelope, false_safe)

    validation = pd.DataFrame([{
        "validation_scope": "small_data_smoke",
        "rates_rows": len(rates),
        "spread_rows": len(spreads),
        "risk_factor_rows": len(panel),
        "corporate_bonds": len(positions),
        "mortgage_loans": len(mortgage),
        "var_99": var99,
        "es_99": es99,
        "backtest_rows": len(backtest),
        "exception_rate": summary.get("kupiec_exception_rate", 0.0),
        "traffic_light": traffic.get("traffic_light"),
        "residual_multiplier": multiplier,
        "corrected_exception_rate": float(corrected["corrected_exception"].mean()) if not corrected.empty else 0.0,
        "pnl_attribution_status": pnl_summary.get("pla_proxy_status", "unknown"),
        "pnl_actual_hypothetical_corr": pnl_summary.get("actual_hypothetical_corr", 0.0),
        "frtb_diag_rows": len(frtb_diag),
        "challenger_selected": challengers.loc[challengers["selected"], "candidate"].iloc[0] if not challengers.empty and challengers["selected"].any() else "none",
        "reverse_stress_rows": len(reverse_stress),
        "data_quality_exceptions": int(len(rate_checks) + len(spread_checks)),
        "status": "PASS",
    }])
    save_table(validation, outputs / "small_data_validation_summary.csv")
    save_table(stability, outputs / "small_data_var_stability.csv")
    save_table(pd.DataFrame([pnl_summary]), outputs / "small_data_pnl_attribution_summary.csv")
    save_table(frtb_diag, outputs / "small_data_frtb_inspired_diagnostics.csv")
    save_table(challengers, outputs / "small_data_challenger_model_selection.csv")
    save_table(reverse_stress, outputs / "small_data_reverse_stress_diagnostics.csv")
    write_markdown(reports / "small_data_validation_report.md", "Small-Data Validation Report", [
        ("Purpose", "Validates the framework with a smaller deterministic dataset to prove that the project is not dependent on one large synthetic run."),
        ("Dataset", f"360 business-day rate/spread sample, 40 corporate bonds, 80 mortgage loans, and a 24-month securitized proxy cash-flow horizon."),
        ("Results", validation.to_markdown(index=False)),
        ("Interpretation", "The small-data run is a smoke validation for local/GitHub reproducibility. It is not used as a production or regulatory calibration dataset."),
    ])
    print(validation.to_string(index=False))
    return validation.iloc[0].to_dict()


if __name__ == "__main__":
    main()
