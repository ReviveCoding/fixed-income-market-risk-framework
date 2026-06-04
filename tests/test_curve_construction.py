from fimrf.data_ingestion.synthetic_fallback import generate_market_data
from fimrf.risk_factors.build_curve_factors import build_curve_factors
from fimrf.risk_factors.build_credit_spread_factors import build_credit_spread_factors
from fimrf.risk_factors.covariance import merge_risk_factors


def test_risk_factor_panel():
    rates, spreads = generate_market_data(n_days=300)
    panel = merge_risk_factors(build_curve_factors(rates), build_credit_spread_factors(spreads))
    assert len(panel) > 250
    assert "rate_level_bp" in panel.columns
    assert "credit_level_bp" in panel.columns
