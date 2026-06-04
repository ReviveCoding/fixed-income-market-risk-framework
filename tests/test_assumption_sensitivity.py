import pandas as pd
from fimrf.model_development.assumption_sensitivity import assumption_sensitivity


def test_assumption_sensitivity_contains_variants():
    losses = pd.Series(range(-50, 450))
    out = assumption_sensitivity(losses)
    assert "historical_simulation" in set(out["variant"])
    assert "student_t_df5" in set(out["variant"])
