# Function and Performance Evaluation Report

## Overall status

**PASS**

## Purpose

This report summarizes functional correctness and model-performance evidence for the Fixed-Income Market Risk Model Development Framework.

## Evaluation scope

### Functional evaluation
- Local package import
- Pipeline execution
- Required artifact generation
- Freddie Mac CRT sample adapter
- HQA/DNA mortgage-pool separation
- Test suite execution
- Required report/output availability

### Performance evaluation
- VaR / Expected Shortfall output generation
- Stressed VaR
- Rolling backtesting outputs
- Exception diagnostics
- P&L attribution proxy
- Challenger model selection
- FRTB-inspired diagnostics
- Reverse stress diagnostics
- Freddie CRT data-quality sanity checks
- Trained VaR overlay evaluation
- Daily risk operations policy comparison
- Limit-monitoring action simulation

## Summary table

| section                   | metric                                      | value                           | status   | note   |
|:--------------------------|:--------------------------------------------|:--------------------------------|:---------|:-------|
| functional_artifacts      | outputs/run_summary.json                    | True                            | PASS     |        |
| functional_artifacts      | outputs/freddie_crt_sample_summary.csv      | True                            | PASS     |        |
| functional_artifacts      | reports/freddie_crt_sample_build_report.md  | True                            | PASS     |        |
| functional_artifacts      | outputs/var_es_by_portfolio.csv             | True                            | PASS     |        |
| functional_artifacts      | outputs/backtesting_exceptions.csv          | True                            | PASS     |        |
| functional_artifacts      | outputs/challenger_model_selection.csv      | True                            | PASS     |        |
| functional_artifacts      | outputs/pnl_attribution_summary.csv         | True                            | PASS     |        |
| functional_artifacts      | outputs/frtb_inspired_diagnostics.csv       | True                            | PASS     |        |
| functional_artifacts      | outputs/reverse_stress_diagnostics.csv      | True                            | PASS     |        |
| functional_artifacts      | reports/model_validation_memo.md            | True                            | PASS     |        |
| functional_artifacts      | reports/regulatory_mapping_memo.md          | True                            | PASS     |        |
| functional_artifacts      | outputs/trained_var_overlay_model.json      | True                            | PASS     |        |
| functional_artifacts      | outputs/trained_var_overlay_predictions.csv | True                            | PASS     |        |
| functional_artifacts      | outputs/trained_var_overlay_evaluation.csv  | True                            | PASS     |        |
| functional_artifacts      | outputs/daily_risk_operations_log.csv       | True                            | PASS     |        |
| functional_artifacts      | outputs/risk_limit_policy_comparison.csv    | True                            | PASS     |        |
| functional_artifacts      | outputs/action_recommendation_log.csv       | True                            | PASS     |        |
| functional_artifacts      | outputs/operational_experiment_summary.csv  | True                            | PASS     |        |
| functional_artifacts      | reports/trained_var_overlay_report.md       | True                            | PASS     |        |
| functional_artifacts      | reports/daily_risk_operations_experiment.md | True                            | PASS     |        |
| run_summary               | data_source                                 | cached_public_compatible_sample | PASS     |        |
| run_summary               | mortgage_source                             | cached_public_compatible_sample | PASS     |        |
| run_summary               | n_risk_factor_days                          | 899                             | PASS     |        |
| run_summary               | n_corporate_bonds                           | 240                             | PASS     |        |
| run_summary               | n_mortgage_loans                            | 4500                            | PASS     |        |
| run_summary               | historical_var_99                           | 3558974.938766091               | PASS     |        |
| run_summary               | historical_es_99                            | 4654329.061926079               | PASS     |        |
| run_summary               | stressed_var_99                             | 5226017.8305288805              | PASS     |        |
| run_summary               | kupiec_exception_rate                       | 0.015408320493066256            | PASS     |        |
| run_summary               | false_safe_rate                             | 0.004622496147919877            | PASS     |        |
| run_summary               | release_status                              | PASS                            | PASS     |        |
| freddie_crt_sample        | rows_in_summary                             | 3                               | PASS     |        |
| freddie_crt_sample        | contains_high_ltv_hqa                       | True                            | PASS     |        |
| freddie_crt_sample        | contains_low_ltv_dna                        | True                            | PASS     |        |
| freddie_crt_sample        | total_loans                                 | 4500                            | PASS     |        |
| mortgage_sample_quality   | loan_rows                                   | 4500                            | PASS     |        |
| mortgage_sample_quality   | mean_fico                                   | 754.315                         | PASS     |        |
| mortgage_sample_quality   | min_fico                                    | 603.0                           | PASS     |        |
| mortgage_sample_quality   | mean_ltv                                    | 81.388                          | PASS     |        |
| mortgage_sample_quality   | hqa_avg_ltv                                 | 93.369                          | PASS     |        |
| mortgage_sample_quality   | dna_avg_ltv                                 | 75.398                          | PASS     |        |
| backtesting               | backtesting_rows                            | 649                             | PASS     |        |
| backtesting               | exception_mean                              | 0.015408                        | PASS     |        |
| backtesting               | exception_severity_mean                     | 20264.649664                    | PASS     |        |
| challenger_selection      | candidate_models                            | 3                               | PASS     |        |
| challenger_selection      | selected_model_count                        | 1                               | PASS     |        |
| pnl_attribution           | rows                                        | 1                               | PASS     |        |
| pnl_attribution           | actual_hypothetical_corr                    | 0.9997848472175416              | PASS     |        |
| pnl_attribution           | correlation_gate                            | 0.9                             | PASS     |        |
| pnl_attribution           | pla_proxy_status                            | PASS                            | PASS     |        |
| frtb_inspired_diagnostics | rows                                        | 3                               | PASS     |        |
| reverse_stress            | rows                                        | 6                               | PASS     |        |
| trained_var_overlay       | evaluation_rows                             | 8                               | PASS     |        |
| trained_var_overlay       | all_vanilla_exception_rate                  | 0.029366                        | PASS     |        |
| trained_var_overlay       | all_trained_exception_rate                  | 0.027821                        | PASS     |        |
| trained_var_overlay       | trained_overlay_exception_improvement       | 0.001546                        | PASS     |        |
| trained_var_overlay       | all_vanilla_false_safe_days                 | 19                              | PASS     |        |
| trained_var_overlay       | all_trained_false_safe_days                 | 18                              | PASS     |        |
| daily_operations          | summary_rows                                | 10                              | PASS     |        |
| daily_operations          | selected_operations_policy                  | residual_corrected_var          | PASS     |        |
| daily_operations          | operations_red_days                         | 6                               | PASS     |        |
| daily_operations          | operations_amber_days                       | 3                               | PASS     |        |
| daily_operations          | operations_green_days                       | 638                             | PASS     |        |
| daily_operations          | policy_comparison_rows                      | 6                               | PASS     |        |
| daily_operations          | required_policy_set_present                 | True                            | PASS     |        |
| daily_operations          | vanilla_exception_rate                      | 0.029366                        | PASS     |        |
| daily_operations          | selected_policy_exception_rate              | 0.009274                        | PASS     |        |
| daily_operations          | vanilla_false_safe_days                     | 19                              | PASS     |        |
| daily_operations          | selected_policy_false_safe_days             | 6                               | PASS     |        |

## Interpretation

The framework has passed local functional validation and generated model-performance artifacts. The Freddie CRT-enhanced local run uses real Freddie Mac CRT loan-level disclosure rows for mortgage-pool attributes while keeping delinquency and prepayment as project-specific proxy fields. The project should therefore be described as a public-data-compatible, local/offline, regulatory-style fixed-income market-risk framework, not as a production bank model or regulatory capital-certified implementation.

## Claim boundary

- No proprietary JPMC data.
- No real trading-desk portfolio.
- No official Freddie Mac performance model replication.
- No production securitized-products valuation.
- No regulatory capital certification.
- Freddie CRT fields are used for local-enhanced mortgage-pool proxy attributes.
