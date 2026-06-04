from __future__ import annotations

import numpy as np
import pandas as pd


def validate_time_series(df: pd.DataFrame, name: str, z_threshold: float = 5.0, stale_days: int = 3) -> tuple[pd.DataFrame, dict]:
    checks = []
    data_cols = [c for c in df.columns if c != "date"]
    for col in data_cols:
        missing = df[col].isna().sum()
        diffs = df[col].diff()
        std = diffs.std(ddof=0)
        mean = diffs.mean()
        if std == 0 or np.isnan(std):
            outlier_mask = pd.Series(False, index=df.index)
        else:
            outlier_mask = ((diffs - mean).abs() / std) > z_threshold
        stale_mask = df[col].diff().abs().fillna(0).eq(0).rolling(stale_days).sum().fillna(0) >= stale_days
        checks.append({
            "dataset": name,
            "column": col,
            "missing_count": int(missing),
            "outlier_move_count": int(outlier_mask.sum()),
            "stale_run_count": int(stale_mask.sum()),
        })
    report = {
        "dataset": name,
        "n_rows": int(len(df)),
        "n_columns": int(len(data_cols)),
        "date_min": str(pd.to_datetime(df["date"]).min().date()),
        "date_max": str(pd.to_datetime(df["date"]).max().date()),
        "total_missing": int(df[data_cols].isna().sum().sum()),
    }
    return pd.DataFrame(checks), report
