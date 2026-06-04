from __future__ import annotations

import pandas as pd

RATE_SERIES = ["DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]


def fetch_fred_rates(series: list[str] | None = None) -> pd.DataFrame:
    """Fetch FRED Treasury-rate CSVs when internet access is available.

    This function is optional. The default project pipeline uses cached samples or
    deterministic synthetic fallback so the repository remains local-runnable.
    """
    series = series or RATE_SERIES
    frames = []
    for sid in series:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        df = pd.read_csv(url)
        df.columns = ["date", sid]
        df["date"] = pd.to_datetime(df["date"])
        df[sid] = pd.to_numeric(df[sid].replace(".", pd.NA), errors="coerce")
        frames.append(df)
    out = frames[0]
    for df in frames[1:]:
        out = out.merge(df, on="date", how="outer")
    return out.sort_values("date").dropna()
