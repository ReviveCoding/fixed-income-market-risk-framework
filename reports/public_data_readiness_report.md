# Public Data Readiness Report

## Executed source mode

Market data source mode: `cached_public_compatible_sample`. Mortgage source mode: `cached_public_compatible_sample`.

## Source coverage

The source catalog maps 11 Treasury/rate fields, 7 corporate-credit spread fields, and 4 mortgage-proxy fields to framework columns.

## Live download boundary

The project includes live FRED adapters for internet-enabled environments, but the submitted validation run uses cached public-compatible samples or deterministic fallback to remain reproducible without proprietary data.

## Evidence files

`outputs/public_data_source_catalog.csv`, `outputs/risk_factor_panel.csv`, `outputs/data_quality_exceptions.csv`, and `reports/market_data_validation_report.md` document source readiness and schema compatibility.

## Claim boundary

A cached public-compatible sample is not represented as audited historical market data. It demonstrates schema compatibility, reproducibility, and model-development workflow readiness.
