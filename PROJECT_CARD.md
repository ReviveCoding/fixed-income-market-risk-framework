# Project Card

## Name
Fixed-Income Market Risk Model Development Framework

## Scope
Offline framework for fixed-income market-risk model development and validation, focused on corporate credit and securitized-products proxy portfolios.

## Public-data boundary
- Public-data-compatible risk factors: Treasury rates and corporate credit OAS series.
- Public mortgage-performance/disclosure-compatible schemas for securitized-products proxy logic.
- Synthetic portfolios only.
- Deterministic synthetic fallback enables full reproducibility without internet or proprietary data.

## Not claimed
- No JPMC data.
- No proprietary trading positions.
- No production bank deployment.
- No regulatory capital certification.
- No production MBS/ABS pricing model.

## Technical evidence
- Market data validation.
- Fixed-income pricing and sensitivities.
- VaR, ES, stressed VaR, stress testing.
- 250-day rolling VaR backtesting.
- Kupiec and Christoffersen statistical tests.
- Assumption-impact analysis.
- Market Health Timestep, residual VaR correction, conservative risk envelope.
- Model validation memo and regulatory-style mapping.

## Recommended resume use
Use as a flagship project for market-risk, quantitative risk, model-development, model-validation, and fixed-income analytics roles. Pair with one compact supporting project covering derivatives, rates, Monte Carlo, and numerical model validation.


## JPMC screening improvements

- Added source-readiness reporting for Federal Reserve H.15/FRED Treasury rates, FRED ICE BofA corporate OAS factors, and public mortgage-performance/disclosure-compatible schema fields.
- Added a model inventory linking each component to purpose, inputs, validation tests, limitations, and controls.
- Added a role-alignment memo focused on Market Risk Model Development rather than generic AI/ML or fraud analytics.
- Preserved public-data/synthetic-portfolio/proxy/offline boundaries to avoid overclaiming production bank experience.


## V4 Final Evidence Snapshot

- Release status: PASS.
- Tests: 20 passed.
- P&L attribution proxy: PASS.
- Challenger selected: residual_corrected_var in small-data validation.
- Model inventory rows: 10.
- Reproducibility manifest generated.
- Claim boundary: offline/public-data-compatible/synthetic-portfolio/securitized-products proxy.
