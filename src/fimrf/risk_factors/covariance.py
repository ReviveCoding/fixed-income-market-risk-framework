from __future__ import annotations

import pandas as pd


def merge_risk_factors(curve: pd.DataFrame, credit: pd.DataFrame) -> pd.DataFrame:
    panel = pd.merge(curve, credit, on="date", how="inner").dropna().reset_index(drop=True)
    return panel


def covariance_matrix(panel: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in panel.columns if c != "date"]
    return panel[cols].cov()
