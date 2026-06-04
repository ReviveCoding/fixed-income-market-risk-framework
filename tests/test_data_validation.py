from fimrf.data_ingestion.synthetic_fallback import generate_market_data
from fimrf.data_validation.data_quality_rules import validate_time_series


def test_synthetic_market_data_and_validation():
    rates, spreads = generate_market_data(n_days=300)
    checks, report = validate_time_series(rates, "rates")
    assert len(rates) == 300
    assert report["n_rows"] == 300
    assert not checks.empty
