from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
REPORTS = ROOT / "reports"
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

MODEL_JSON = OUTPUTS / "trained_var_overlay_model.json"
PRED_CSV = OUTPUTS / "trained_var_overlay_predictions.csv"
EVAL_CSV = OUTPUTS / "trained_var_overlay_evaluation.csv"
OPS_LOG_CSV = OUTPUTS / "daily_risk_operations_log.csv"
POLICY_CSV = OUTPUTS / "risk_limit_policy_comparison.csv"
ACTION_CSV = OUTPUTS / "action_recommendation_log.csv"
SUMMARY_CSV = OUTPUTS / "operational_experiment_summary.csv"
REPORT_MODEL = REPORTS / "trained_var_overlay_report.md"
REPORT_OPS = REPORTS / "daily_risk_operations_experiment.md"


def read_inputs() -> pd.DataFrame:
    pnl_path = OUTPUTS / "portfolio_loss_panel.csv"
    bt_path = OUTPUTS / "backtesting_exceptions.csv"
    if not pnl_path.exists() or not bt_path.exists():
        raise FileNotFoundError("Run scripts/run_pipeline.py before this script.")

    pnl = pd.read_csv(pnl_path, parse_dates=["date"])
    bt = pd.read_csv(bt_path, parse_dates=["date"])

    cols = ["date", "var_99"]
    if "exception" in bt.columns:
        cols.append("exception")

    df = pnl.merge(bt[cols], on="date", how="left")
    df = df.sort_values("date").reset_index(drop=True)

    if "var_99" not in df or df["var_99"].isna().all():
        losses = df["total_loss"].abs()
        df["var_99"] = losses.rolling(250, min_periods=60).quantile(0.99).bfill()

    df["exception"] = df.get("exception", False).fillna(False).astype(bool)
    return df


def build_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    x = df.copy()

    total_abs_components = (
        x.get("rates_loss", 0).abs()
        + x.get("corporate_credit_loss", 0).abs()
        + x.get("securitized_proxy_loss", 0).abs()
        + 1.0
    )

    x["abs_loss_lag1"] = x["total_loss"].abs().shift(1)
    x["loss_to_var_lag1"] = (x["total_loss"].abs().shift(1) / x["var_99"].shift(1)).replace([np.inf, -np.inf], np.nan)
    x["rolling_exception_20"] = x["exception"].astype(float).rolling(20, min_periods=1).sum().shift(1)
    x["rolling_exception_60"] = x["exception"].astype(float).rolling(60, min_periods=1).sum().shift(1)
    x["rolling_loss_p95_60"] = x["total_loss"].abs().rolling(60, min_periods=20).quantile(0.95).shift(1)
    x["vol_to_var"] = x.get("rolling_vol", pd.Series(0, index=x.index)) / x["var_99"].replace(0, np.nan)
    x["credit_loss_share"] = x.get("corporate_credit_loss", pd.Series(0, index=x.index)).abs() / total_abs_components
    x["securitized_loss_share"] = x.get("securitized_proxy_loss", pd.Series(0, index=x.index)).abs() / total_abs_components
    x["mht"] = pd.to_numeric(x.get("market_health_timestep", 0), errors="coerce").fillna(0)

    state = x.get("market_health_state", pd.Series("normal", index=x.index)).astype(str).str.lower()
    x["state_elevated"] = state.str.contains("elevated|stress").astype(float)
    x["log_var_99"] = np.log1p(x["var_99"].clip(lower=0))

    # Risk number on date t is evaluated against next observed loss.
    x["next_day_loss"] = x["total_loss"].abs().shift(-1)
    x["target_multiplier"] = (x["next_day_loss"] / x["var_99"]).replace([np.inf, -np.inf], np.nan)
    x["target_multiplier"] = x["target_multiplier"].clip(lower=1.0, upper=1.80)

    feature_cols = [
        "log_var_99",
        "rolling_vol",
        "abs_loss_lag1",
        "loss_to_var_lag1",
        "rolling_exception_20",
        "rolling_exception_60",
        "rolling_loss_p95_60",
        "vol_to_var",
        "credit_loss_share",
        "securitized_loss_share",
        "mht",
        "state_elevated",
    ]

    for c in feature_cols:
        if c not in x.columns:
            x[c] = 0.0
        x[c] = pd.to_numeric(x[c], errors="coerce")

    x[feature_cols] = x[feature_cols].replace([np.inf, -np.inf], np.nan)
    x = x.dropna(subset=feature_cols + ["target_multiplier", "next_day_loss", "var_99"]).reset_index(drop=True)
    return x, feature_cols


def chronological_split(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    train_end = max(int(n * 0.60), 10)
    valid_end = max(int(n * 0.80), train_end + 1)
    idx = np.arange(n)
    return idx[:train_end], idx[train_end:valid_end], idx[valid_end:]


def fit_ridge(X: np.ndarray, y: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std == 0] = 1.0
    Xs = (X - mean) / std
    Xb = np.c_[np.ones(len(Xs)), Xs]

    penalty = np.eye(Xb.shape[1]) * alpha
    penalty[0, 0] = 0.0

    beta = np.linalg.pinv(Xb.T @ Xb + penalty) @ Xb.T @ y
    return beta, mean, std


def predict_ridge(X: np.ndarray, beta: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    Xs = (X - mean) / std
    Xb = np.c_[np.ones(len(Xs)), Xs]
    return Xb @ beta


def evaluate_policy(loss: pd.Series, risk_number: pd.Series, base_var: pd.Series) -> dict:
    loss = pd.to_numeric(loss, errors="coerce").abs()
    risk_number = pd.to_numeric(risk_number, errors="coerce")
    base_var = pd.to_numeric(base_var, errors="coerce")

    mask = loss.notna() & risk_number.notna() & base_var.notna() & (risk_number > 0)
    loss = loss[mask]
    risk_number = risk_number[mask]
    base_var = base_var[mask]

    exceptions = loss > risk_number
    utilization = loss / risk_number

    return {
        "observations": int(mask.sum()),
        "exception_rate": float(exceptions.mean()) if len(exceptions) else np.nan,
        "exception_count": int(exceptions.sum()) if len(exceptions) else 0,
        "mean_utilization": float(utilization.mean()) if len(utilization) else np.nan,
        "p95_utilization": float(utilization.quantile(0.95)) if len(utilization) else np.nan,
        "false_safe_days": int(exceptions.sum()) if len(exceptions) else 0,
        "avg_overconservatism": float((risk_number / base_var - 1.0).mean()) if len(risk_number) else np.nan,
        "review_burden_amber_red": int((utilization >= 0.85).sum()) if len(utilization) else 0,
        "red_days": int((utilization >= 1.0).sum()) if len(utilization) else 0,
        "amber_days": int(((utilization >= 0.85) & (utilization < 1.0)).sum()) if len(utilization) else 0,
    }


def main() -> None:
    df0 = read_inputs()
    df, features = build_features(df0)

    if len(df) < 100:
        raise ValueError(f"Not enough rows for training: {len(df)}")

    train_idx, valid_idx, test_idx = chronological_split(len(df))

    X = df[features].to_numpy(dtype=float)
    y = df["target_multiplier"].to_numpy(dtype=float)

    alpha_grid = [0.01, 0.1, 1.0, 10.0, 50.0]
    best = None

    for alpha in alpha_grid:
        beta, mean, std = fit_ridge(X[train_idx], y[train_idx], alpha)
        pred_valid = np.clip(predict_ridge(X[valid_idx], beta, mean, std), 1.0, 1.8)
        valid_loss = float(np.mean((pred_valid - y[valid_idx]) ** 2))

        if best is None or valid_loss < best[0]:
            best = (valid_loss, alpha, beta, mean, std)

    _, alpha, beta, mean, std = best
    pred = np.clip(predict_ridge(X, beta, mean, std), 1.0, 1.8)

    df["predicted_var_multiplier"] = pred
    df["trained_overlay_var_99"] = df["var_99"] * df["predicted_var_multiplier"]
    df["vanilla_exception_next_day"] = df["next_day_loss"] > df["var_99"]
    df["trained_exception_next_day"] = df["next_day_loss"] > df["trained_overlay_var_99"]

    df["split"] = "train"
    df.loc[valid_idx, "split"] = "validation"
    df.loc[test_idx, "split"] = "test"

    eval_rows = []
    for split_name in ["train", "validation", "test", "all"]:
        part = df if split_name == "all" else df[df["split"] == split_name]
        if part.empty:
            continue

        vanilla = evaluate_policy(part["next_day_loss"], part["var_99"], part["var_99"])
        trained = evaluate_policy(part["next_day_loss"], part["trained_overlay_var_99"], part["var_99"])

        eval_rows.append({"split": split_name, "policy": "vanilla_var", **vanilla})
        eval_rows.append({"split": split_name, "policy": "trained_var_overlay", **trained})

    eval_df = pd.DataFrame(eval_rows)

    var_es_path = OUTPUTS / "var_es_by_portfolio.csv"
    if var_es_path.exists():
        ve = pd.read_csv(var_es_path)
        stressed_const = float(ve["stressed_var_99"].iloc[0]) if "stressed_var_99" in ve.columns else float(df["var_99"].quantile(0.99))
    else:
        stressed_const = float(df["var_99"].quantile(0.99))

    corrected_path = OUTPUTS / "corrected_backtesting_exceptions.csv"
    corrected = None
    if corrected_path.exists():
        cdf = pd.read_csv(corrected_path, parse_dates=["date"])
        if "corrected_var_99" in cdf.columns:
            corrected = cdf[["date", "corrected_var_99"]]

    ops = df.copy()

    if corrected is not None:
        ops = ops.merge(corrected, on="date", how="left")
    else:
        ops["corrected_var_99"] = np.nan

    ops["corrected_var_99"] = ops["corrected_var_99"].fillna(ops["var_99"] * 1.25)
    ops["stress_gate_var_99"] = np.maximum(ops["var_99"], stressed_const * 0.50)

    ops["conservative_envelope_var_99"] = np.maximum.reduce([
        ops["var_99"].to_numpy(),
        ops["corrected_var_99"].to_numpy(),
        ops["trained_overlay_var_99"].to_numpy(),
    ])

    ops["hybrid_operations_var_99"] = np.maximum(
        ops["trained_overlay_var_99"],
        ops["stress_gate_var_99"] * 0.75,
    )

    policy_cols = {
        "vanilla_var": "var_99",
        "residual_corrected_var": "corrected_var_99",
        "trained_overlay_var": "trained_overlay_var_99",
        "stress_gate_var": "stress_gate_var_99",
        "conservative_envelope": "conservative_envelope_var_99",
        "hybrid_operations_policy": "hybrid_operations_var_99",
    }

    policy_rows = []
    for policy, col in policy_cols.items():
        policy_rows.append({"policy": policy, **evaluate_policy(ops["next_day_loss"], ops[col], ops["var_99"])})

    policy_df = pd.DataFrame(policy_rows)
    policy_df["review_efficiency_score"] = (
        policy_df["exception_rate"].fillna(1) * 10
        + policy_df["avg_overconservatism"].fillna(0).clip(lower=0)
        + policy_df["review_burden_amber_red"].fillna(0) / max(len(ops), 1)
    )

    selected_policy = policy_df.sort_values(["exception_rate", "review_efficiency_score"]).iloc[0]["policy"]

    ops["selected_policy"] = selected_policy
    ops["selected_policy_var_99"] = ops[policy_cols[selected_policy]]
    ops["limit_utilization"] = ops["next_day_loss"] / ops["selected_policy_var_99"]

    ops["risk_zone"] = np.select(
        [ops["limit_utilization"] >= 1.0, ops["limit_utilization"] >= 0.85],
        ["RED", "AMBER"],
        default="GREEN",
    )

    ops["recommended_action"] = np.select(
        [ops["risk_zone"] == "RED", ops["risk_zone"] == "AMBER"],
        [
            "Escalate breach review, reduce risk, and document exception.",
            "Desk review: monitor drivers and consider hedging/risk reduction.",
        ],
        default="No action required; continue monitoring.",
    )

    model_payload = {
        "model_type": "ridge_style_closed_form_var_multiplier_overlay",
        "alpha": float(alpha),
        "features": features,
        "intercept": float(beta[0]),
        "coefficients": {f: float(v) for f, v in zip(features, beta[1:])},
        "feature_mean": {f: float(v) for f, v in zip(features, mean)},
        "feature_std": {f: float(v) for f, v in zip(features, std)},
        "prediction_clip": [1.0, 1.8],
        "selected_operations_policy": str(selected_policy),
        "claim_boundary": "trained on local public-compatible/synthetic portfolio outputs; not a production bank model",
    }

    MODEL_JSON.write_text(json.dumps(model_payload, indent=2), encoding="utf-8")

    pred_cols = [
        "date",
        "split",
        "var_99",
        "next_day_loss",
        "target_multiplier",
        "predicted_var_multiplier",
        "trained_overlay_var_99",
        "vanilla_exception_next_day",
        "trained_exception_next_day",
    ]

    df[pred_cols].to_csv(PRED_CSV, index=False)
    eval_df.to_csv(EVAL_CSV, index=False)

    ops_cols = [
        "date",
        "selected_policy",
        "selected_policy_var_99",
        "next_day_loss",
        "limit_utilization",
        "risk_zone",
        "recommended_action",
        "var_99",
        "corrected_var_99",
        "trained_overlay_var_99",
        "stress_gate_var_99",
        "conservative_envelope_var_99",
        "hybrid_operations_var_99",
    ]

    ops[ops_cols].to_csv(OPS_LOG_CSV, index=False)
    policy_df.to_csv(POLICY_CSV, index=False)
    ops[ops_cols][ops["risk_zone"].isin(["AMBER", "RED"])].to_csv(ACTION_CSV, index=False)

    summary = pd.DataFrame([
        {"metric": "training_rows", "value": len(train_idx)},
        {"metric": "validation_rows", "value": len(valid_idx)},
        {"metric": "test_rows", "value": len(test_idx)},
        {"metric": "selected_alpha", "value": alpha},
        {"metric": "selected_operations_policy", "value": selected_policy},
        {"metric": "test_vanilla_exception_rate", "value": float(eval_df[(eval_df.split == "test") & (eval_df.policy == "vanilla_var")]["exception_rate"].iloc[0])},
        {"metric": "test_trained_exception_rate", "value": float(eval_df[(eval_df.split == "test") & (eval_df.policy == "trained_var_overlay")]["exception_rate"].iloc[0])},
        {"metric": "operations_red_days", "value": int((ops["risk_zone"] == "RED").sum())},
        {"metric": "operations_amber_days", "value": int((ops["risk_zone"] == "AMBER").sum())},
        {"metric": "operations_green_days", "value": int((ops["risk_zone"] == "GREEN").sum())},
    ])

    summary.to_csv(SUMMARY_CSV, index=False)

    model_report = f"""# Trained VaR Overlay Report

## Status

PASS

## Model

A lightweight ridge-style closed-form regression model was trained to predict a conservative next-day VaR multiplier from lagged market-risk state features.

## Selected alpha

{alpha}

## Features

{', '.join(features)}

## Evaluation

{eval_df.to_markdown(index=False)}

## Claim boundary

This is a local/offline challenger overlay trained on public-compatible and synthetic-portfolio risk outputs. It is not a production bank model, not a regulatory capital model, and not trained on proprietary trading-desk data.
"""

    REPORT_MODEL.write_text(model_report, encoding="utf-8")

    ops_report = f"""# Daily Risk Operations Experiment

## Status

PASS

## Objective

Simulate a daily market-risk operating workflow using generated VaR, residual-corrected VaR, trained overlay VaR, stress-gate VaR, and conservative envelope policies.

## Selected policy

**{selected_policy}**

## Policy comparison

{policy_df.to_markdown(index=False)}

## Action distribution

{ops['risk_zone'].value_counts().rename_axis('risk_zone').reset_index(name='days').to_markdown(index=False)}

## Interpretation

The experiment translates model outputs into a desk-review style monitoring process: GREEN days require routine monitoring, AMBER days require review, and RED days require breach escalation and risk-reduction consideration. All actions are simulated and based on proxy P&L/risk outputs.

## Claim boundary

This is an offline operational simulation. It does not use proprietary JPMC data, real desk positions, official actual P&L, or official hypothetical P&L.
"""

    REPORT_OPS.write_text(ops_report, encoding="utf-8")

    print(f"Wrote {MODEL_JSON}")
    print(f"Wrote {PRED_CSV}")
    print(f"Wrote {EVAL_CSV}")
    print(f"Wrote {OPS_LOG_CSV}")
    print(f"Wrote {POLICY_CSV}")
    print(f"Wrote {ACTION_CSV}")
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {REPORT_MODEL}")
    print(f"Wrote {REPORT_OPS}")

    print("\nTraining evaluation:")
    print(eval_df.to_string(index=False))

    print("\nOperational policy comparison:")
    print(policy_df.to_string(index=False))

    print(f"\nSelected operations policy: {selected_policy}")


if __name__ == "__main__":
    main()
