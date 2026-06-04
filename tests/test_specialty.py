import pandas as pd
from fimrf.specialty.market_health_timestep import assign_market_health_timestep
from fimrf.specialty.conservative_risk_envelope import false_safe_metrics


def test_market_health_timestep_and_false_safe():
    df = pd.DataFrame({"date": pd.bdate_range("2024-01-01", periods=120), "total_loss": list(range(120))})
    out = assign_market_health_timestep(df, window=20)
    assert "market_health_state" in out.columns
    bt = pd.DataFrame({"total_loss": [1, 2, 10], "var_99": [3, 3, 3]})
    metrics = false_safe_metrics(bt, envelope=8)
    assert 0 <= metrics["false_safe_rate"] <= 1
