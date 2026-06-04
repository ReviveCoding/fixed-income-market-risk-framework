# Challenger Model Selection Report

## Purpose

Compares vanilla historical VaR, residual-corrected VaR, and conservative tail-envelope variants using exception rate, false-safe rate, overreach proxy, and complexity penalty.

## Selection table

| candidate                  |   exception_rate |   false_safe_rate |   coverage_overreach_proxy |   complexity_penalty |   target_exception_rate |   exception_excess |   exception_shortfall |   review_score | selected   | selection_rationale                |
|:---------------------------|-----------------:|------------------:|---------------------------:|---------------------:|------------------------:|-------------------:|----------------------:|---------------:|:-----------|:-----------------------------------|
| residual_corrected_var     |       0.00616333 |        0.00616333 |                      0.004 |                0.004 |                    0.01 |         0          |            0.00383667 |     0.00819183 | True       | selected champion for review       |
| vanilla_historical_var     |       0.0154083  |        0.0154083  |                      0     |                0     |                    0.01 |         0.00540832 |            0          |     0.0154391  | False      | retained as challenger / benchmark |
| conservative_tail_envelope |       0.00616333 |        0.0046225  |                      0.025 |                0.02  |                    0.01 |         0          |            0.00383667 |     0.0289796  | False      | retained as challenger / benchmark |

## Use

This converts model development from a single chosen model into an explicit champion/challenger decision record.
