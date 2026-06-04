# Reverse Stress Testing Report

## Purpose

Estimates shock multipliers required for scenario stress losses to exceed VaR/ES thresholds, helping identify scenarios that are already near the tail-loss boundary.

## Reverse stress table

| scenario                        |   base_total_stress_loss |   multiplier_to_var_99 |   multiplier_to_es_99 | reverse_stress_priority   |
|:--------------------------------|-------------------------:|-----------------------:|----------------------:|:--------------------------|
| hy_spread_widen_250bp           |              8.76281e+07 |              0.0386947 |             0.0509116 | already_beyond_es         |
| liquidity_spread_shock          |              5.31407e+07 |              0.0638069 |             0.0839523 | already_beyond_es         |
| mortgage_default_severity_shock |              3.59456e+07 |              0.0943298 |             0.124112  | already_beyond_es         |
| parallel_rate_up_100bp          |              3.49734e+07 |              0.096952  |             0.127562  | already_beyond_es         |
| curve_shock_proxy               |              2.8076e+07  |              0.12077   |             0.1589    | already_beyond_es         |
| ig_spread_widen_75bp            |              2.63273e+07 |              0.128792  |             0.169455  | already_beyond_es         |

## Use

This supports risk-manager discussion about which scenario families require closer monitoring.
