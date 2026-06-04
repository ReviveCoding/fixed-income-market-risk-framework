from __future__ import annotations

from pathlib import Path
import os
import pandas as pd
from .synthetic_fallback import generate_market_data, generate_mortgage_pool
from .fetch_fred_rates import fetch_fred_rates
from .fetch_fred_oas import fetch_fred_oas


def load_market_data(root: Path, use_cached: bool = True) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Load live public data, cached public-compatible samples, or deterministic synthetic fallback.

    Set environment variable FIMRF_USE_LIVE=1 to attempt live FRED downloads.
    The default remains fallback-safe for local reproducibility.
    """
    if os.getenv("FIMRF_USE_LIVE") == "1":
        try:
            rates = fetch_fred_rates()
            spreads = fetch_fred_oas()
            return rates, spreads, "live_fred_public_data"
        except Exception:
            pass
    rates_path = root / "data" / "cached_samples" / "rates_sample.csv"
    spreads_path = root / "data" / "cached_samples" / "oas_sample.csv"
    if use_cached and rates_path.exists() and spreads_path.exists():
        rates = pd.read_csv(rates_path, parse_dates=["date"])
        spreads = pd.read_csv(spreads_path, parse_dates=["date"])
        return rates, spreads, "cached_public_compatible_sample"
    rates, spreads = generate_market_data()
    return rates, spreads, "deterministic_synthetic_fallback"


def load_mortgage_pool(root: Path, use_cached: bool = True) -> tuple[pd.DataFrame, str]:
    path = root / "data" / "cached_samples" / "mortgage_pool_sample.csv"
    if use_cached and path.exists():
        return pd.read_csv(path), "cached_public_compatible_sample"
    return generate_mortgage_pool(), "deterministic_synthetic_fallback"
