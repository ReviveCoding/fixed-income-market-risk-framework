from __future__ import annotations

from pathlib import Path
import pandas as pd
from .synthetic_fallback import generate_mortgage_pool

REQUIRED_COLUMNS = {"loan_id", "balance", "coupon", "term_months", "fico", "ltv", "delinquency_proxy", "prepay_score"}


def load_mortgage_performance_sample(path: str | Path | None = None) -> pd.DataFrame:
    """Load a Freddie/Fannie/Ginnie-style mortgage sample if supplied.

    The function expects a privacy-safe, redistributable sample already normalized
    to this framework schema. If no file is supplied, a deterministic fallback
    pool is returned.
    """
    if path is None:
        return generate_mortgage_pool()
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Mortgage sample missing required columns: {sorted(missing)}")
    return df
