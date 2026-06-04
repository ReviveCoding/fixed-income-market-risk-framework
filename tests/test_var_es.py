import pandas as pd
from fimrf.risk_models.var import historical_var, expected_shortfall, monte_carlo_var


def test_var_es_positive_tail():
    losses = pd.Series([-1, 0, 1, 2, 3, 10, 20, 30, 40, 100])
    v = historical_var(losses, 0.90)
    e = expected_shortfall(losses, 0.90)
    mv, me = monte_carlo_var(losses, 0.95, scenarios=1000, seed=1)
    assert v > 0
    assert e >= v
    assert me >= mv
