# Securitized Proxy Stress Grid Report

## Purpose

Adds a transparent CPR/default/severity/liquidity sensitivity grid for the securitized-products proxy. It validates structural intuition without claiming production MBS/ABS valuation.

## Top stress cases

|   prepayment_multiplier |   default_multiplier |   severity_multiplier |   liquidity_spread_multiplier |   proxy_stress_loss |   stress_rank |
|------------------------:|---------------------:|----------------------:|------------------------------:|--------------------:|--------------:|
|                     0.5 |                    3 |                   1.5 |                           2   |         1.74914e+06 |             1 |
|                     1   |                    3 |                   1.5 |                           2   |         1.66584e+06 |             2 |
|                     0.5 |                    3 |                   1.5 |                           1.5 |         1.6343e+06  |             3 |
|                     1.5 |                    3 |                   1.5 |                           2   |         1.58255e+06 |             4 |
|                     1   |                    3 |                   1.5 |                           1.5 |         1.55647e+06 |             5 |
|                     0.5 |                    3 |                   1.5 |                           1   |         1.51945e+06 |             6 |
|                     1.5 |                    3 |                   1.5 |                           1.5 |         1.47865e+06 |             7 |
|                     1   |                    3 |                   1.5 |                           1   |         1.4471e+06  |             8 |
|                     1.5 |                    3 |                   1.5 |                           1   |         1.37474e+06 |             9 |
|                     0.5 |                    2 |                   1.5 |                           2   |         1.31921e+06 |            10 |

## Quality checks

| check                                              | passed   | detail                                                                   |
|:---------------------------------------------------|:---------|:-------------------------------------------------------------------------|
| monotonic_mean_loss_by_default_multiplier          | True     | Mean proxy stress loss should increase with worsening stress multiplier. |
| monotonic_mean_loss_by_severity_multiplier         | True     | Mean proxy stress loss should increase with worsening stress multiplier. |
| monotonic_mean_loss_by_liquidity_spread_multiplier | True     | Mean proxy stress loss should increase with worsening stress multiplier. |

## Boundary

The grid is synthetic/proxy-based and should be described as public-mortgage-performance-compatible, not as production securitized-products modeling.
