from __future__ import annotations

import math

import numpy as np
import pandas as pd

from fimrf.utils import chi2_sf_df1


def kupiec_pof(exceptions: pd.Series, alpha: float) -> dict:
    """Test whether the observed VaR exception rate matches the expected rate."""
    exception_count = int(exceptions.sum())
    observation_count = int(exceptions.count())
    if observation_count == 0:
        return {
            "n": 0,
            "exceptions": 0,
            "exception_rate": 0.0,
            "lr_pof": 0.0,
            "p_value": 1.0,
        }
    observed_exception_rate = min(
        max(exception_count / observation_count, 1e-12), 1 - 1e-12
    )
    expected_exception_rate = alpha
    null_log_likelihood = (
        (observation_count - exception_count) * math.log(1 - expected_exception_rate)
        + exception_count * math.log(expected_exception_rate)
        if exception_count not in [0, observation_count]
        else (observation_count - exception_count)
        * math.log(1 - expected_exception_rate)
        + exception_count * math.log(max(expected_exception_rate, 1e-12))
    )
    alternative_log_likelihood = (observation_count - exception_count) * math.log(
        1 - observed_exception_rate
    ) + exception_count * math.log(observed_exception_rate)
    lr = max(-2 * (null_log_likelihood - alternative_log_likelihood), 0.0)
    return {
        "n": observation_count,
        "exceptions": exception_count,
        "exception_rate": exception_count / observation_count,
        "lr_pof": lr,
        "p_value": chi2_sf_df1(lr),
    }


def christoffersen_independence(exceptions: pd.Series) -> dict:
    """Test whether consecutive VaR exception flags are independent."""
    exception_flags = exceptions.astype(int).to_numpy()
    if len(exception_flags) < 2:
        return {
            "lr_independence": 0.0,
            "p_value": 1.0,
            "n00": 0,
            "n01": 0,
            "n10": 0,
            "n11": 0,
        }
    n00 = n01 = n10 = n11 = 0
    for previous_flag, current_flag in zip(exception_flags[:-1], exception_flags[1:]):
        if previous_flag == 0 and current_flag == 0:
            n00 += 1
        elif previous_flag == 0 and current_flag == 1:
            n01 += 1
        elif previous_flag == 1 and current_flag == 0:
            n10 += 1
        elif previous_flag == 1 and current_flag == 1:
            n11 += 1

    def safe_log(x):
        return math.log(max(x, 1e-12))

    exception_probability = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    exception_after_no_exception = n01 / max(n00 + n01, 1)
    exception_after_exception = n11 / max(n10 + n11, 1)
    ll_null = (n00 + n10) * safe_log(1 - exception_probability) + (
        n01 + n11
    ) * safe_log(exception_probability)
    ll_alt = (
        n00 * safe_log(1 - exception_after_no_exception)
        + n01 * safe_log(exception_after_no_exception)
        + n10 * safe_log(1 - exception_after_exception)
        + n11 * safe_log(exception_after_exception)
    )
    lr = max(-2 * (ll_null - ll_alt), 0.0)
    return {
        "lr_independence": lr,
        "p_value": chi2_sf_df1(lr),
        "n00": n00,
        "n01": n01,
        "n10": n10,
        "n11": n11,
    }


def rolling_var_backtest(
    losses: pd.DataFrame,
    loss_col: str = "total_loss",
    window: int = 250,
    confidence: float = 0.99,
) -> tuple[pd.DataFrame, dict]:
    df = losses[["date", loss_col]].dropna().copy().reset_index(drop=True)
    vars_ = []
    for i in range(len(df)):
        if i < window:
            vars_.append(np.nan)
        else:
            vars_.append(
                float(np.quantile(df.loc[i - window : i - 1, loss_col], confidence))
            )
    df["var_99"] = vars_
    df["exception"] = (df[loss_col] > df["var_99"]).fillna(False)
    df["exception_severity"] = (df[loss_col] - df["var_99"]).where(df["exception"], 0.0)
    test_df = df.dropna(subset=["var_99"]).copy()
    kup = kupiec_pof(test_df["exception"], 1 - confidence)
    chr_ = christoffersen_independence(test_df["exception"])
    summary = {
        **{f"kupiec_{k}": v for k, v in kup.items()},
        **{f"christoffersen_{k}": v for k, v in chr_.items()},
    }
    return test_df, summary
