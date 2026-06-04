# Validation Report

## Executed commands

```bash
python scripts/create_public_compatible_samples.py
python scripts/run_pipeline.py
pytest -q
```

## Result

- Release status: `PASS`
- Tests: `11 passed`
- Data source mode: `cached_public_compatible_sample`
- Mortgage source mode: `cached_public_compatible_sample`
- Risk-factor days: `899`
- Corporate bonds: `240`
- Mortgage loans: `800`
- Reports generated: `17`
- Model inventory rows: `5`
- Public source catalog rows: `22`

## Key synthetic/proxy outputs

- Historical 99% VaR: `3,390,744.45`
- Historical 99% ES: `4,461,286.46`
- Stressed 99% VaR: `5,011,375.22`
- Kupiec exception rate: `0.0154`
- False-safe rate: `0.0046`

## Claim boundary

These are validation-run outputs from cached public-compatible samples and synthetic/proxy portfolios. They should not be represented as real trading-desk P&L, JPMC data, production model results, or regulatory capital estimates.


## V4 Validation Addendum

Executed `python scripts/run_all_checks.py` after adding P&L attribution proxy, FRTB-inspired diagnostics, champion/challenger model selection, reverse stress diagnostics, and reproducibility manifest generation. The local/GitHub runnable check passed with 20 pytest tests.
