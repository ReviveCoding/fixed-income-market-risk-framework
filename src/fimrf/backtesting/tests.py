from __future__ import annotations

import math
import numpy as np
import pandas as pd
from fimrf.utils import chi2_sf_df1


def kupiec_pof(exceptions: pd.Series, alpha: float) -> dict:
    x = int(exceptions.sum())
    n = int(exceptions.count())
    if n == 0:
        return {"n": 0, "exceptions": 0, "exception_rate": 0.0, "lr_pof": 0.0, "p_value": 1.0}
    phat = min(max(x / n, 1e-12), 1 - 1e-12)
    p = alpha
    log_l_null = (n - x) * math.log(1 - p) + x * math.log(p) if x not in [0, n] else (n - x) * math.log(1 - p) + x * math.log(max(p, 1e-12))
    log_l_alt = (n - x) * math.log(1 - phat) + x * math.log(phat)
    lr = max(-2 * (log_l_null - log_l_alt), 0.0)
    return {"n": n, "exceptions": x, "exception_rate": x / n, "lr_pof": lr, "p_value": chi2_sf_df1(lr)}


def christoffersen_independence(exceptions: pd.Series) -> dict:
    e = exceptions.astype(int).to_numpy()
    if len(e) < 2:
        return {"lr_independence": 0.0, "p_value": 1.0, "n00": 0, "n01": 0, "n10": 0, "n11": 0}
    n00 = n01 = n10 = n11 = 0
    for a, b in zip(e[:-1], e[1:]):
        if a == 0 and b == 0: n00 += 1
        elif a == 0 and b == 1: n01 += 1
        elif a == 1 and b == 0: n10 += 1
        elif a == 1 and b == 1: n11 += 1
    def safe_log(x): return math.log(max(x, 1e-12))
    pi = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    pi01 = n01 / max(n00 + n01, 1)
    pi11 = n11 / max(n10 + n11, 1)
    ll_null = (n00 + n10) * safe_log(1 - pi) + (n01 + n11) * safe_log(pi)
    ll_alt = n00 * safe_log(1 - pi01) + n01 * safe_log(pi01) + n10 * safe_log(1 - pi11) + n11 * safe_log(pi11)
    lr = max(-2 * (ll_null - ll_alt), 0.0)
    return {"lr_independence": lr, "p_value": chi2_sf_df1(lr), "n00": n00, "n01": n01, "n10": n10, "n11": n11}


def rolling_var_backtest(losses: pd.DataFrame, loss_col: str = "total_loss", window: int = 250, confidence: float = 0.99) -> tuple[pd.DataFrame, dict]:
    df = losses[["date", loss_col]].dropna().copy().reset_index(drop=True)
    vars_ = []
    for i in range(len(df)):
        if i < window:
            vars_.append(np.nan)
        else:
            vars_.append(float(np.quantile(df.loc[i-window:i-1, loss_col], confidence)))
    df["var_99"] = vars_
    df["exception"] = (df[loss_col] > df["var_99"]).fillna(False)
    df["exception_severity"] = (df[loss_col] - df["var_99"]).where(df["exception"], 0.0)
    test_df = df.dropna(subset=["var_99"]).copy()
    kup = kupiec_pof(test_df["exception"], 1 - confidence)
    chr_ = christoffersen_independence(test_df["exception"])
    summary = {**{f"kupiec_{k}": v for k, v in kup.items()}, **{f"christoffersen_{k}": v for k, v in chr_.items()}}
    return test_df, summary
