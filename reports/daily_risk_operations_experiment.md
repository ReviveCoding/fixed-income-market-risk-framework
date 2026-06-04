# Daily Risk Operations Experiment

## Status

PASS

## Objective

Simulate a daily market-risk operating workflow using generated VaR, residual-corrected VaR, trained overlay VaR, stress-gate VaR, and conservative envelope policies.

## Selected policy

**residual_corrected_var**

## Policy comparison

| policy                   |   observations |   exception_rate |   exception_count |   mean_utilization |   p95_utilization |   false_safe_days |   avg_overconservatism |   review_burden_amber_red |   red_days |   amber_days |   review_efficiency_score |
|:-------------------------|---------------:|-----------------:|------------------:|-------------------:|------------------:|------------------:|-----------------------:|--------------------------:|-----------:|-------------:|--------------------------:|
| vanilla_var              |            647 |       0.0293663  |                19 |           0.320261 |          0.888894 |                19 |               0        |                        39 |         19 |           20 |                  0.353941 |
| residual_corrected_var   |            647 |       0.00927357 |                 6 |           0.228758 |          0.634924 |                 6 |               0.4      |                         9 |          6 |            3 |                  0.506646 |
| trained_overlay_var      |            647 |       0.0278207  |                18 |           0.312701 |          0.877057 |                18 |               0.028894 |                        36 |         18 |           18 |                  0.362743 |
| stress_gate_var          |            647 |       0.0200927  |                13 |           0.279889 |          0.797441 |                13 |               0.137074 |                        26 |         13 |           13 |                  0.378187 |
| conservative_envelope    |            647 |       0.00927357 |                 6 |           0.228758 |          0.634924 |                 6 |               0.4      |                         9 |          6 |            3 |                  0.506646 |
| hybrid_operations_policy |            647 |       0.0262751  |                17 |           0.310976 |          0.877057 |                17 |               0.033384 |                        35 |         17 |           18 |                  0.350231 |

## Action distribution

| risk_zone   |   days |
|:------------|-------:|
| GREEN       |    638 |
| RED         |      6 |
| AMBER       |      3 |

## Interpretation

The experiment translates model outputs into a desk-review style monitoring process: GREEN days require routine monitoring, AMBER days require review, and RED days require breach escalation and risk-reduction consideration. All actions are simulated and based on proxy P&L/risk outputs.

## Claim boundary

This is an offline operational simulation. It does not use proprietary JPMC data, real desk positions, official actual P&L, or official hypothetical P&L.
