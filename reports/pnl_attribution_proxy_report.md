# P&L Attribution Proxy Report

## Purpose

Adds an actual-vs-hypothetical P&L proxy to support model-performance discussion. This is not desk P&L and is used only as an offline review artifact.

## Summary

Actual/hypothetical correlation: 0.9997848482410968; p95 unexplained ratio: 0.1168761569705302; status: `PASS`.

## Sample rows

| date       |   actual_pnl_proxy |   hypothetical_pnl_proxy |   unexplained_pnl_proxy |   absolute_unexplained_ratio | dominant_loss_factor   |
|:-----------|-------------------:|-------------------------:|------------------------:|-----------------------------:|:-----------------------|
| 2022-12-26 |   807917           |         824806           |               -16889.5  |                    0.0180333 | rates                  |
| 2022-12-27 |    32141.6         |          27018.6         |                 5122.95 |                    0.0369129 | rates                  |
| 2022-12-28 |        2.52714e+06 |              2.56752e+06 |               -40382.1  |                    0.015072  | corporate_credit       |
| 2022-12-29 |       -1.21161e+06 |             -1.24134e+06 |                29722.9  |                    0.0219664 | corporate_credit       |
| 2022-12-30 |   132232           |         118639           |                13592.4  |                    0.0589936 | rates                  |
| 2023-01-02 |   472735           |         478954           |                -6219.13 |                    0.0105281 | corporate_credit       |
| 2023-01-03 |   525732           |         532375           |                -6642.94 |                    0.0103129 | corporate_credit       |
| 2023-01-04 |   194541           |         188071           |                 6470.15 |                    0.0215789 | corporate_credit       |

## Use

This helps explain whether modeled risk-factor losses explain proxy P&L and where unmodeled residuals may require compensating controls.
