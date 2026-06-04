from __future__ import annotations

import numpy as np
import pandas as pd

_COMPONENT_MAP = {
    "rates": ("rates_loss", 10),
    "corporate_credit": ("corporate_credit_loss", 20),
    "securitized_proxy": ("securitized_proxy_loss", 60),
}


def frtb_inspired_diagnostics(losses: pd.DataFrame, confidence: float = 0.975) -> pd.DataFrame:
    """Create FRTB-inspired ES, liquidity-horizon and modellability diagnostics.

    This is not an official FRTB implementation. It is a transparent model-risk review
    artifact that demonstrates awareness of ES, liquidity horizon, and modellable/non-
    modellable risk-factor concepts.
    """
    rows: list[dict] = []
    for family, (col, liquidity_horizon) in _COMPONENT_MAP.items():
        if col not in losses.columns:
            continue
        sample = losses[col].dropna().to_numpy(dtype=float)
        obs = int(len(sample))
        if obs == 0:
            var = es = scaled_es = 0.0
        else:
            var = float(np.quantile(sample, confidence))
            tail = sample[sample >= var]
            es = float(tail.mean()) if len(tail) else var
            scaled_es = float(es * np.sqrt(liquidity_horizon / 10.0))
        # Proxy: at least 24 usable observations per year equivalent and enough history.
        modellable_proxy = obs >= 250
        rows.append({
            "risk_factor_family": family,
            "loss_column": col,
            "observations": obs,
            "modellable_proxy": bool(modellable_proxy),
            "liquidity_horizon_days": int(liquidity_horizon),
            "var_975": var,
            "es_975": es,
            "liquidity_horizon_scaled_es_proxy": scaled_es,
            "review_action": "standard_review" if modellable_proxy else "treat_as_non_modellable_proxy_for_review",
        })
    out = pd.DataFrame(rows)
    if not out.empty:
        total = max(float(out["liquidity_horizon_scaled_es_proxy"].sum()), 1.0)
        out["scaled_es_contribution_share"] = out["liquidity_horizon_scaled_es_proxy"] / total
    return out
