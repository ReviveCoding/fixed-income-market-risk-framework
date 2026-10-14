# Fixed-Income Market Risk Model Development Framework

Corporate Credit, Securitized-Products Proxy, VaR/ES, Stress Testing, Backtesting, Model Governance

This repository is an offline, local-runnable framework for fixed-income market-risk model development. It uses public-data-compatible loaders, cached/sample-compatible interfaces, and deterministic synthetic fallbacks so the full pipeline can run without proprietary data or internet access.

## Claim boundary

This is a non-production portfolio framework. It does **not** use J.P. Morgan data, proprietary bank portfolios, trading-desk positions, Bloomberg/TRACE subscription data, or production securitized-products models. Outputs are regulatory-style and FRTB-inspired review artifacts, not regulatory capital certification.

## What the pipeline does

1. Builds a Treasury-rate and credit-spread risk-factor panel from public-data-compatible schemas or deterministic fallback data.
2. Validates market data for missing observations, stale quotes, date alignment, and outlier shocks.
3. Generates synthetic corporate-credit and securitized-products proxy portfolios.
4. Prices fixed-rate corporate bonds using spread-adjusted discounting and computes DV01/CS01/OAS01 sensitivities.
5. Builds a synthetic mortgage-pool and tranche waterfall proxy with prepayment, default, severity, WAL, and tranche-loss diagnostics.
6. Computes historical VaR, Monte Carlo VaR, Student-t VaR, Expected Shortfall, stressed VaR, and scenario stress losses.
7. Runs rolling 250-day 99% VaR backtesting with Kupiec and Christoffersen tests.
8. Quantifies modeling-assumption impact across VaR engine, distribution, volatility, horizon, correlation, valuation, and securitized-product assumptions.
9. Adds reliability-focused specialty modules: Market Health Timestep, residual VaR correction, conservative risk envelope, false-safe diagnostics, and specialty ablation.
10. Generates model-risk documentation: methodology notes, validation memo, regulatory mapping, limitations, compensating controls, and executive summary.

## Public-data and governance updates

The repository includes the following additions for public-data compatibility and model validation:

1. `scripts/create_public_compatible_samples.py` creates cached public-compatible samples and a source catalog so the pipeline can demonstrate public-data schema readiness without requiring live internet access.
2. `outputs/model_inventory.csv` and `reports/model_inventory.md` register model components, inputs, validation tests, limitations, and controls.
3. `reports/public_data_readiness_report.md` documents whether the run used live FRED data, cached public-compatible samples, or deterministic fallback.
4. The governance packet separates regulatory-style evidence from prohibited overclaims such as production regulatory capital, real JPMC data, or desk-approved securitized-products pricing.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
make run
make test
```

Or directly:

```bash
python scripts/run_pipeline.py
pytest -q
```

## Main outputs

- `outputs/risk_factor_panel.csv` or `outputs/risk_factor_panel.parquet`
- `outputs/corporate_credit_sensitivities.csv`
- `outputs/securitized_tranche_cashflows.csv`
- `outputs/var_es_by_portfolio.csv`
- `outputs/stressed_var_results.csv`
- `outputs/stress_loss_by_scenario.csv`
- `outputs/backtesting_exceptions.csv`
- `outputs/kupiec_christoffersen_results.csv`
- `outputs/assumption_sensitivity_matrix.csv`
- `outputs/specialty_ablation_table.csv`
- `outputs/model_risk_findings.csv`
- `outputs/release_decision.json`

## Reports

- `reports/market_data_validation_report.md`
- `reports/corporate_credit_portfolio_report.md`
- `reports/securitized_products_proxy_report.md`
- `reports/var_es_methodology.md`
- `reports/stress_testing_report.md`
- `reports/backtesting_report.md`
- `reports/assumption_impact_report.md`
- `reports/specialty_contribution_report.md`
- `reports/model_validation_memo.md`
- `reports/regulatory_mapping_memo.md`
- `reports/known_limitations.md`
- `reports/compensating_controls.md`
- `reports/executive_risk_summary.md`

## Data-source design

The framework is built around the following public-data-compatible layers:

- Federal Reserve H.15 / FRED Treasury constant maturity rates for rate-risk factors.
- FRED ICE BofA option-adjusted spread series for corporate-credit spread factors.
- Freddie Mac / Fannie Mae / Ginnie Mae style mortgage-performance or disclosure schemas for securitized-products proxy modeling.
- Synthetic positions and deterministic fallback samples for reproducible local execution.

## Backtesting and stress extensions

The validation suite also includes:

- 250-day traffic-light backtesting proxy
- VaR exception attribution by dominant risk component and market-health state
- VaR stability diagnostics across multiple lookback windows and bootstrap intervals
- bounded empirical residual VaR correction
- securitized proxy CPR/default/severity/liquidity stress grid
- small-data validation smoke run
- Dockerfile and GitHub Actions CI workflow

Canonical validation commands:

```bash
python scripts/create_public_compatible_samples.py
python scripts/run_pipeline.py
python scripts/run_small_data_validation.py
pytest -q
```

Or run everything:

```bash
python scripts/run_all_checks.py
```

Claim boundary: offline framework, public-data-compatible loaders, cached public-style samples, deterministic synthetic fallback, synthetic portfolio, securitized-products proxy, and regulatory-style documentation. No proprietary bank data, production trading-desk portfolio, production MBS/ABS model, or regulatory capital certification is claimed.

## Expanded model-risk diagnostics

Additional diagnostics extend the original VaR, stress-testing, and backtesting workflow:

- Actual-vs-hypothetical P&L attribution proxy.
- FRTB-inspired ES, liquidity-horizon, and modellability-proxy diagnostics.
- Champion/challenger VaR model selection.
- Reverse stress testing against VaR/ES thresholds.
- SHA-256 reproducibility manifest.
- Expanded small-data smoke validation and 20 pytest checks.

Canonical full validation command:

```bash
python scripts/run_all_checks.py
```

Latest validation status: PASS. The framework remains offline/public-data-compatible/synthetic-portfolio/proxy only and does not claim production or regulatory certification.

## Final local / GitHub runnable verification

Recommended local setup:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
python scripts/run_all_checks.py
```

The project uses a `src/` package layout and now includes explicit `setuptools` build metadata in `pyproject.toml`. The GitHub Actions workflow installs the package in editable mode, runs an import smoke test, regenerates cached public-compatible samples, executes the full pipeline, runs small-data validation, executes pytest, and verifies required artifacts.

Docker smoke test:

```bash
docker build -t fimrf .
docker run --rm fimrf
```

Boundary: this is an offline/public-data-compatible framework with deterministic cached samples and synthetic fallback data. It does not use JPMC data, desk P&L, Bloomberg/TRACE/WRDS marks, or production securitized-products assumptions.

## Latest validated results

This project includes a local/offline fixed-income market-risk model development workflow with public-compatible Treasury/OAS samples, synthetic corporate-credit portfolios, Freddie Mac CRT-enhanced local mortgage proxy validation, VaR/ES, stressed VaR, rolling backtesting, P&L attribution proxy, FRTB-inspired diagnostics, reverse stress testing, trained VaR overlay, daily risk operations simulation, and function/performance evaluation reports.

In the simulated local operations experiment, selected residual-corrected VaR reduced simulated exception rate from 2.94% to 0.93%, false-safe days from 19 to 6, and RED/AMBER review burden from 39 to 9 days under explicit public-data/synthetic-portfolio boundaries.
