# Resume Baseline Contribution Report

## Status

PASS

## Purpose

This report translates model-development and operations-simulation outputs into resume-safe baseline-vs-method contribution metrics.

## Selected operating method

**residual_corrected_var**

## Baseline-vs-method summary

| metric                          | baseline    |   baseline_value | method                 |   method_value |   absolute_change |   relative_reduction_pct | unit   | note                                                                            |
|:--------------------------------|:------------|-----------------:|:-----------------------|---------------:|------------------:|-------------------------:|:-------|:--------------------------------------------------------------------------------|
| exception_rate                  | vanilla_var |        0.0293663 | residual_corrected_var |     0.00927357 |        -0.0200927 |                 68.4211  | rate   | Primary risk-control metric.                                                    |
| false_safe_days                 | vanilla_var |       19         | residual_corrected_var |     6          |       -13         |                 68.4211  | days   | Days where realized next-day loss exceeded selected risk number.                |
| red_days                        | vanilla_var |       19         | residual_corrected_var |     6          |       -13         |                 68.4211  | days   | Breach/escalation days in simulated operations.                                 |
| amber_days                      | vanilla_var |       20         | residual_corrected_var |     3          |       -17         |                 85       | days   | Review-zone days in simulated operations.                                       |
| review_burden_amber_red         | vanilla_var |       39         | residual_corrected_var |     9          |       -30         |                 76.9231  | days   | Total RED+AMBER review burden.                                                  |
| p95_limit_utilization           | vanilla_var |        0.888894  | residual_corrected_var |     0.634924   |        -0.25397   |                 28.5714  | ratio  | Lower means lower tail utilization under selected risk number.                  |
| trained_overlay_exception_rate  | vanilla_var |        0.0293663 | trained_var_overlay    |     0.0278207  |        -0.0015456 |                  5.26316 | rate   | Challenger model improved slightly but was not selected as operations champion. |
| trained_overlay_false_safe_days | vanilla_var |       19         | trained_var_overlay    |    18          |        -1         |                  5.26316 | days   | Challenger model comparison.                                                    |

## Main improvement claims

- Exception rate: 2.94% → 0.93% (68.4% relative reduction)
- False-safe days: 19 → 6 (68.4% relative reduction)
- RED/AMBER review burden: 39 → 9 days (76.9% relative reduction)
- Tradeoff: selected policy is more conservative, with avg_overconservatism = 0.40

## Resume-ready bullets

1. Built and locally validated a fixed-income market-risk model development framework with public-compatible Treasury/OAS data, synthetic corporate-credit portfolios, Freddie Mac CRT-enhanced mortgage proxy pools, VaR/ES, stressed VaR, rolling backtesting, P&L attribution proxy, FRTB-inspired diagnostics, reverse stress testing, and function/performance evaluation reports.

2. Trained a lightweight VaR multiplier overlay as a challenger model and ran a daily market-risk operations simulation comparing vanilla, residual-corrected, trained-overlay, stress-gate, conservative-envelope, and hybrid policies; selected residual_corrected_var, reducing simulated exception rate from 2.94% to 0.93% (68.4% relative reduction), false-safe days from 19 to 6, and RED/AMBER review burden from 39 to 9 days.

## Claim boundary

These metrics are from an offline/local simulation using public-compatible market data artifacts, synthetic corporate-credit portfolios, Freddie Mac CRT-enhanced mortgage proxy pools, and proxy P&L/risk outputs. They should not be described as production bank results, proprietary trading-desk results, regulatory capital certification, or official Freddie Mac model replication.
