# Weakness Reinforcement Loop Report

## Loop 1: public/small-data readiness

Identified weakness: v2 already had cached public-compatible samples, but the evidence was still mostly framework-level. Reinforcement: added explicit source catalog, cached sample generation, and small-data validation script so the project can prove local execution without external credentials.

## Loop 2: backtesting interpretability

Identified weakness: VaR exceptions were counted but not fully attributed. Reinforcement: added 250-day traffic-light proxy, exception attribution by dominant loss factor and market-health state, and VaR stability diagnostics. Current traffic light: `green` with 0 recent exceptions.

## Loop 3: specialty layer effectiveness

Identified weakness: the v2 residual correction could leave the exception rate unchanged. Reinforcement: replaced it with a bounded empirical breach-ratio correction and preserved ablation/false-safe metrics. Current specialty ablation:

| module                     |   exception_rate |   relative_change_vs_vanilla |
|:---------------------------|-----------------:|-----------------------------:|
| vanilla_historical_var     |       0.0154083  |                   0          |
| residual_var_correction    |       0.00616333 |                  -0.00924499 |
| conservative_risk_envelope |       0.0046225  |                  -0.0107858  |

## Loop 4: securitized proxy depth

Identified weakness: securitized-products proxy stress was mostly scenario-multiplier based. Reinforcement: added CPR/default/severity/liquidity stress grid plus monotonicity checks while keeping the proxy claim boundary.

## Loop 5: model review depth

Identified weakness: v3 still lacked explicit challenger model selection, P&L attribution proxy, FRTB-inspired liquidity-horizon diagnostics, reverse stress tests, and reproducibility hashing. Reinforcement: added challenger selection table, PLA-style proxy summary, FRTB-inspired ES/liquidity-horizon diagnostics, reverse stress multipliers, and a file-hash reproducibility manifest. Challenger summary:

| candidate                  |   exception_rate |   false_safe_rate |   coverage_overreach_proxy |   complexity_penalty |   target_exception_rate |   exception_excess |   exception_shortfall |   review_score | selected   | selection_rationale                |
|:---------------------------|-----------------:|------------------:|---------------------------:|---------------------:|------------------------:|-------------------:|----------------------:|---------------:|:-----------|:-----------------------------------|
| residual_corrected_var     |       0.00616333 |        0.00616333 |                      0.004 |                0.004 |                    0.01 |         0          |            0.00383667 |     0.00819183 | True       | selected champion for review       |
| vanilla_historical_var     |       0.0154083  |        0.0154083  |                      0     |                0     |                    0.01 |         0.00540832 |            0          |     0.0154391  | False      | retained as challenger / benchmark |
| conservative_tail_envelope |       0.00616333 |        0.0046225  |                      0.025 |                0.02  |                    0.01 |         0          |            0.00383667 |     0.0289796  | False      | retained as challenger / benchmark |

## Stop condition

Additional possible improvements are now mostly minor for resume-screening purposes unless proprietary market data, real TRACE history, Bloomberg marks, official modellability testing data, or professional desk P&L are available. The remaining gap is professional Fixed Income quant experience, not project structure.
