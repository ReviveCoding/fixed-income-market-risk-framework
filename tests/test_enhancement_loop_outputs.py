from __future__ import annotations

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_backtesting_enhancement_outputs_exist():
    for name in [
        "traffic_light_backtest.csv",
        "exception_attribution.csv",
        "var_stability_diagnostics.csv",
        "securitized_stress_grid.csv",
        "securitized_grid_quality_checks.csv",
    ]:
        assert (ROOT / "outputs" / name).exists(), name


def test_residual_correction_does_not_increase_exception_rate():
    ablation = pd.read_csv(ROOT / "outputs" / "specialty_ablation_table.csv")
    base = float(ablation.loc[ablation["module"] == "vanilla_historical_var", "exception_rate"].iloc[0])
    corrected = float(ablation.loc[ablation["module"] == "residual_var_correction", "exception_rate"].iloc[0])
    assert corrected <= base


def test_securitized_grid_quality_checks_pass():
    checks = pd.read_csv(ROOT / "outputs" / "securitized_grid_quality_checks.csv")
    assert not checks.empty
    assert checks["passed"].all()
