# Upgrade Changelog

## v2 screening-readiness upgrade

Implemented improvements based on the JPMC Market Risk Model Development gap analysis.

### Added

- Cached public-compatible sample generator: `scripts/create_public_compatible_samples.py`.
- Public data source catalog: `data/cached_samples/public_data_source_catalog.csv` and `outputs/public_data_source_catalog.csv`.
- Public data readiness report: `reports/public_data_readiness_report.md`.
- Model inventory: `outputs/model_inventory.csv` and `reports/model_inventory.md`.
- JPMC role-alignment memo: `reports/jpmc_market_risk_role_alignment.md`.
- Official reference source report: `reports/official_reference_sources.md`.
- Reviewer notebook: `notebooks/model_development_walkthrough.ipynb`.
- Governance artifact tests: `tests/test_governance_artifacts.py`.

### Validation

- `python scripts/create_public_compatible_samples.py` completed.
- `python scripts/run_pipeline.py` completed.
- `pytest -q` passed with 11 tests.
- Validation source mode: cached public-compatible sample.
- Release status: PASS.

## v3 Enhancement Loop

Implemented a weakness-analysis and reinforcement loop after the JPMC role-fit review.

### Loop 1: backtesting interpretability
- Added `traffic_light_backtest.csv` for recent 250-day exception diagnostics.
- Added `exception_attribution.csv` to explain VaR breaches by dominant risk component and market-health state.
- Added `var_stability_diagnostics.csv` with multi-lookback and bootstrap VaR stability checks.

### Loop 2: specialty layer effectiveness
- Replaced aggregate-rate-only residual correction with bounded empirical breach-ratio correction.
- Main validation run improved residual correction exception rate from the vanilla 1.54% to 0.62%.
- Preserved claim boundary: the correction is an offline research diagnostic, not an approved regulatory overlay.

### Loop 3: securitized proxy depth
- Added `securitized_stress_grid.csv` with CPR/default/severity/liquidity stress combinations.
- Added monotonicity quality checks for default, severity, and liquidity multipliers.

### Loop 4: small-data validation and runnable audit
- Added `scripts/run_small_data_validation.py` to validate the framework on a smaller deterministic dataset.
- Added `scripts/run_all_checks.py`, Dockerfile, and GitHub Actions workflow.
- Added local/GitHub runnability audit report.


## V5 final runnable hardening

- Added explicit setuptools build metadata for the src-layout package.
- Updated GitHub Actions to install the package in editable mode and test Python 3.10/3.11.
- Added pip dependency caching in GitHub Actions.
- Added package import smoke test.
- Added required artifact verification script.
- Updated run_all_checks.py to verify package install, import, pipeline, small-data validation, pytest, and required artifacts.
- Updated README and local/GitHub runnability audit.
