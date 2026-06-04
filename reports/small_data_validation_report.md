# Small-Data Validation Report

## Purpose

Validates the framework with a smaller deterministic dataset to prove that the project is not dependent on one large synthetic run.

## Dataset

360 business-day rate/spread sample, 40 corporate bonds, 80 mortgage loans, and a 24-month securitized proxy cash-flow horizon.

## Results

| validation_scope   |   rates_rows |   spread_rows |   risk_factor_rows |   corporate_bonds |   mortgage_loans |   var_99 |   es_99 |   backtest_rows |   exception_rate | traffic_light   |   residual_multiplier |   corrected_exception_rate | pnl_attribution_status   |   pnl_actual_hypothetical_corr |   frtb_diag_rows | challenger_selected    |   reverse_stress_rows |   data_quality_exceptions | status   |
|:-------------------|-------------:|--------------:|-------------------:|------------------:|-----------------:|---------:|--------:|----------------:|-----------------:|:----------------|----------------------:|---------------------------:|:-------------------------|-------------------------------:|-----------------:|:-----------------------|----------------------:|--------------------------:|:---------|
| small_data_smoke   |          360 |           360 |                359 |                40 |               80 |   189840 |  206723 |             234 |        0.0128205 | green           |               1.23444 |                  0.0042735 | PASS                     |                       0.999841 |                3 | residual_corrected_var |                     6 |                        18 | PASS     |

## Interpretation

The small-data run is a smoke validation for local/GitHub reproducibility. It is not used as a production or regulatory calibration dataset.
