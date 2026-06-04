from fimrf.data_ingestion.synthetic_fallback import generate_market_data
from fimrf.risk_factors.build_curve_factors import build_curve_factors
from fimrf.risk_factors.build_credit_spread_factors import build_credit_spread_factors
from fimrf.risk_factors.covariance import merge_risk_factors
from fimrf.instruments.corporate_bond import generate_corporate_bonds, compute_sensitivities, corporate_daily_losses
from fimrf.backtesting.tests import rolling_var_backtest


def test_rolling_backtest_runs():
    rates, spreads = generate_market_data(n_days=500)
    panel = merge_risk_factors(build_curve_factors(rates), build_credit_spread_factors(spreads))
    sens = compute_sensitivities(generate_corporate_bonds(n=30), rates, spreads)
    losses = corporate_daily_losses(sens, panel).rename(columns={"corporate_total_loss": "total_loss"})
    bt, summary = rolling_var_backtest(losses, "total_loss", window=250, confidence=0.99)
    assert len(bt) > 0
    assert "kupiec_exception_rate" in summary
