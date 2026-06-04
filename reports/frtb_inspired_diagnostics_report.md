# FRTB-Inspired Diagnostics Report

## Purpose

Adds Expected Shortfall, liquidity-horizon scaling, and modellability-proxy diagnostics for review discussion. This is not an official FRTB implementation.

## Diagnostics

| risk_factor_family   | loss_column            |   observations | modellable_proxy   |   liquidity_horizon_days |         var_975 |          es_975 |   liquidity_horizon_scaled_es_proxy | review_action   |   scaled_es_contribution_share |
|:---------------------|:-----------------------|---------------:|:-------------------|-------------------------:|----------------:|----------------:|------------------------------------:|:----------------|-------------------------------:|
| rates                | rates_loss             |            899 | True               |                       10 |     1.24321e+06 |     1.76407e+06 |                         1.76407e+06 | standard_review |                     0.259127   |
| corporate_credit     | corporate_credit_loss  |            899 | True               |                       20 |     2.2318e+06  |     3.52483e+06 |                         4.98486e+06 | standard_review |                     0.732237   |
| securitized_proxy    | securitized_proxy_loss |            899 | True               |                       60 | 16577.9         | 24001.1         |                     58790.6         | standard_review |                     0.00863587 |

## Boundary

The diagnostics are educational/model-risk review artifacts under public-data-compatible and synthetic/proxy constraints.
