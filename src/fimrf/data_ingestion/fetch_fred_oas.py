from __future__ import annotations

import pandas as pd

# Public FRED series IDs mapped to framework columns.
OAS_SERIES = {
    "IG_OAS": "BAMLC0A0CM",
    "HY_OAS": "BAMLH0A0HYM2",
    "A_OAS": "BAMLC0A3CA",
    "BBB_OAS": "BAMLC0A4CBBB",
    "BB_OAS": "BAMLH0A1HYBB",
    "B_OAS": "BAMLH0A2HYB",
    "CCC_OAS": "BAMLH0A3HYC",
}


def fetch_fred_oas(series_map: dict[str, str] | None = None) -> pd.DataFrame:
    """Fetch FRED ICE BofA OAS CSVs when internet access is available.

    Default pipeline does not depend on live downloads. This adapter makes the
    project public-data-compatible when a user wants to refresh market factors.
    """
    series_map = series_map or OAS_SERIES
    frames = []
    for name, sid in series_map.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        df = pd.read_csv(url)
        df.columns = ["date", name]
        df["date"] = pd.to_datetime(df["date"])
        df[name] = pd.to_numeric(df[name].replace(".", pd.NA), errors="coerce")
        frames.append(df)
    out = frames[0]
    for df in frames[1:]:
        out = out.merge(df, on="date", how="outer")
    return out.sort_values("date").dropna()
