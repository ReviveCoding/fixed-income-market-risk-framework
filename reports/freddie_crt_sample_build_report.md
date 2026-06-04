# Freddie Mac CRT Mortgage Sample Build Report

## Source files

- 26DNA2_20260501_lld.txt
- 26DNA1_20260501_lld.txt
- 25HQA1_20260501_lld.txt

## Output

- `data\cached_samples\mortgage_pool_sample.csv`
- `outputs\freddie_crt_sample_summary.csv`

## Claim boundary

This adapter uses real Freddie Mac CRT monthly loan-level disclosure rows from STACR DNA/HQA files, but it creates project-specific proxy fields for delinquency and prepayment. It does not claim to reproduce Freddie Mac official performance modeling, official delinquency reporting, official prepayment modeling, or production securitized-products valuation.

## Sample summary

| pool_type    | deal   | source_file             |   loans |   avg_balance |   avg_coupon |   avg_fico |   avg_ltv |   avg_delinquency_proxy |   avg_prepay_score |
|:-------------|:-------|:------------------------|--------:|--------------:|-------------:|-----------:|----------:|------------------------:|-------------------:|
| high_ltv_hqa | 25HQA1 | 25HQA1_20260501_lld.txt |    1500 |        331533 |      6.91529 |    745.808 |   93.3687 |              0.0574258  |          0.0260645 |
| low_ltv_dna  | 26DNA1 | 26DNA1_20260501_lld.txt |    1500 |        346683 |      6.82512 |    757.666 |   75.3413 |              0.00773307 |          0.0276819 |
| low_ltv_dna  | 26DNA2 | 26DNA2_20260501_lld.txt |    1500 |        366742 |      6.74466 |    759.471 |   75.4547 |              0.0072728  |          0.0278866 |

## Numeric summary

|       |          balance |     coupon |   term_months |      fico |        ltv |   delinquency_proxy |   prepay_score |
|:------|-----------------:|-----------:|--------------:|----------:|-----------:|--------------------:|---------------:|
| count |   4500           | 4500       |    4500       | 4500      | 4500       |        4500         |  4500          |
| mean  | 348319           |    6.82836 |     359.796   |  754.315  |   81.3882  |           0.0241439 |     0.027211   |
| std   | 180111           |    0.51465 |       4.32976 |   42.3725 |    9.96871 |           0.0260471 |     0.00225752 |
| min   |   1000           |    4.375   |     300       |  603      |   61       |           0.005     |     0.019375   |
| 25%   | 210436           |    6.5     |     360       |  727      |   75       |           0.005     |     0.02556    |
| 50%   | 317612           |    6.875   |     360       |  762      |   80       |           0.005     |     0.027425   |
| 75%   | 450296           |    7.125   |     360       |  789      |   90       |           0.0463    |     0.0288     |
| max   |      1.49494e+06 |    8.625   |     480       |  830      |  105       |           0.1185    |     0.03328    |
