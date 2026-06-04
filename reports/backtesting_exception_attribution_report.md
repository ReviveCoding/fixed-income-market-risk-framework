# Backtesting Exception Attribution Report

## Traffic-light diagnostic

The most recent 250 VaR observations had 0 exceptions, exception rate 0.0, and review status `green`. This is a review proxy, not a formal regulatory capital calculation.

## Dominant-factor attribution

| dominant_factor   | market_health_state   |   exceptions |     avg_severity |     max_severity |   exception_share |
|:------------------|:----------------------|-------------:|-----------------:|-----------------:|------------------:|
| corporate_credit  | elevated              |            5 |      1.81665e+06 |      3.482e+06   |               0.5 |
| corporate_credit  | stressed              |            4 | 717462           |      1.14611e+06 |               0.4 |
| corporate_credit  | normal                |            1 | 528020           | 528020           |               0.1 |

## VaR stability diagnostics

|   lookback_days |      var_99 |       es_99 |   bootstrap_var_p05 |   bootstrap_var_p95 |   bootstrap_ci_width |   relative_delta_vs_longest |
|----------------:|------------:|------------:|--------------------:|--------------------:|---------------------:|----------------------------:|
|             125 | 2.12886e+06 | 2.39081e+06 |         1.62654e+06 |         2.6094e+06  |     982859           |                  -0.401266  |
|             250 | 2.08371e+06 | 2.35675e+06 |         1.87526e+06 |         2.45223e+06 |     576967           |                  -0.413965  |
|             500 | 3.83807e+06 | 5.092e+06   |         3.38949e+06 |         4.63284e+06 |          1.24335e+06 |                   0.0794417 |
|             750 | 3.5556e+06  | 4.57975e+06 |         3.25801e+06 |         3.96371e+06 |     705696           |                   0         |

## Use

This report helps explain whether VaR breaches are dominated by rates, corporate credit spreads, securitized proxy losses, or stressed market-health regimes.
