# Trained VaR Overlay Report

## Status

PASS

## Model

A lightweight ridge-style closed-form regression model was trained to predict a conservative next-day VaR multiplier from lagged market-risk state features.

## Selected alpha

50.0

## Features

log_var_99, rolling_vol, abs_loss_lag1, loss_to_var_lag1, rolling_exception_20, rolling_exception_60, rolling_loss_p95_60, vol_to_var, credit_loss_share, securitized_loss_share, mht, state_elevated

## Evaluation

| split      | policy              |   observations |   exception_rate |   exception_count |   mean_utilization |   p95_utilization |   false_safe_days |   avg_overconservatism |   review_burden_amber_red |   red_days |   amber_days |
|:-----------|:--------------------|---------------:|-----------------:|------------------:|-------------------:|------------------:|------------------:|-----------------------:|--------------------------:|-----------:|-------------:|
| train      | vanilla_var         |            388 |        0.0489691 |                19 |           0.42071  |          0.989969 |                19 |              0         |                        39 |         19 |           20 |
| train      | trained_var_overlay |            388 |        0.0463918 |                18 |           0.413212 |          0.977735 |                18 |              0.0155746 |                        36 |         18 |           18 |
| validation | vanilla_var         |            129 |        0         |                 0 |           0.149373 |          0.386493 |                 0 |              0         |                         0 |          0 |            0 |
| validation | trained_var_overlay |            129 |        0         |                 0 |           0.143026 |          0.369537 |                 0 |              0.0460852 |                         0 |          0 |            0 |
| test       | vanilla_var         |            130 |        0         |                 0 |           0.190033 |          0.561115 |                 0 |              0         |                         0 |          0 |            0 |
| test       | trained_var_overlay |            130 |        0         |                 0 |           0.181084 |          0.541322 |                 0 |              0.0515886 |                         0 |          0 |            0 |
| all        | vanilla_var         |            647 |        0.0293663 |                19 |           0.320261 |          0.888894 |                19 |              0         |                        39 |         19 |           20 |
| all        | trained_var_overlay |            647 |        0.0278207 |                18 |           0.312701 |          0.877057 |                18 |              0.028894  |                        36 |         18 |           18 |

## Claim boundary

This is a local/offline challenger overlay trained on public-compatible and synthetic-portfolio risk outputs. It is not a production bank model, not a regulatory capital model, and not trained on proprietary trading-desk data.
