# Market Data Validation Report

## Scope

Validated Treasury-rate and corporate-credit spread panels using source mode `cached_public_compatible_sample`.

## Checks

Business-day alignment, missing observations, stale quote runs, outlier spread/rate moves, and data-lineage summaries were generated.

## Public source mapping

The framework maps Federal Reserve H.15/FRED Treasury series and FRED ICE BofA corporate OAS series to internal risk-factor columns through `public_data_source_catalog.csv`.

## Claim boundary

Public-data-compatible schemas, cached samples, and deterministic synthetic fallback are used; no proprietary market data is claimed.
