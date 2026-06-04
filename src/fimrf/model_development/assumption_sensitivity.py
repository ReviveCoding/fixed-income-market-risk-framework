from __future__ import annotations

import numpy as np
import pandas as pd
from fimrf.risk_models.var import historical_var, expected_shortfall, monte_carlo_var


def assumption_sensitivity(losses: pd.Series, confidence: float = 0.99) -> pd.DataFrame:
    rows = []
    hist_var = historical_var(losses, confidence)
    hist_es = expected_shortfall(losses, confidence)
    rows.append({"assumption_family": "engine", "variant": "historical_simulation", "var_99": hist_var, "es_99": hist_es})
    mc_var, mc_es = monte_carlo_var(losses, confidence, student_t_df=None)
    rows.append({"assumption_family": "engine", "variant": "monte_carlo_gaussian", "var_99": mc_var, "es_99": mc_es})
    t_var, t_es = monte_carlo_var(losses, confidence, student_t_df=5)
    rows.append({"assumption_family": "tail_distribution", "variant": "student_t_df5", "var_99": t_var, "es_99": t_es})
    # EWMA-vol approximation rescale
    demeaned = losses - losses.mean()
    ewma_var = []
    lam = 0.94
    v = float(demeaned.var())
    for x in demeaned.fillna(0):
        v = lam * v + (1-lam) * float(x*x)
        ewma_var.append(v)
    ewma_scale = np.sqrt(ewma_var[-1] / max(float(losses.var()), 1e-12))
    rows.append({"assumption_family": "volatility", "variant": "ewma_0.94_rescaled", "var_99": hist_var * ewma_scale, "es_99": hist_es * ewma_scale})
    rows.append({"assumption_family": "horizon", "variant": "10_day_sqrt_time", "var_99": hist_var * np.sqrt(10), "es_99": hist_es * np.sqrt(10)})
    rows.append({"assumption_family": "valuation", "variant": "delta_gamma_proxy_uplift", "var_99": hist_var * 1.06, "es_99": hist_es * 1.06})
    rows.append({"assumption_family": "correlation", "variant": "stressed_correlation_uplift", "var_99": hist_var * 1.12, "es_99": hist_es * 1.12})
    rows.append({"assumption_family": "securitized_proxy", "variant": "high_default_high_severity", "var_99": hist_var * 1.08, "es_99": hist_es * 1.10})
    out = pd.DataFrame(rows)
    out["var_delta_vs_historical"] = out["var_99"] - hist_var
    out["es_delta_vs_historical"] = out["es_99"] - hist_es
    return out
