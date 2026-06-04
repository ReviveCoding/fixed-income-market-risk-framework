
from __future__ import annotations

from pathlib import Path
import pandas as pd
from fimrf.utils import write_markdown


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def generate_model_inventory(root: Path) -> pd.DataFrame:
    rows = [
        {"model_id": "M-001", "model_name": "Treasury Curve Risk-Factor Builder", "purpose": "Construct level/slope/curvature and rate shocks", "input_data": "H.15/FRED-compatible Treasury rates or cached fallback", "validation_tests": "missing/stale/outlier checks; curve continuity; sign/sanity checks", "limitations": "No proprietary intraday or desk curve marks", "control": "source catalog, data-quality exceptions, lineage report"},
        {"model_id": "M-002", "model_name": "Corporate Credit Portfolio Valuation", "purpose": "Spread-adjusted valuation and DV01/CS01/OAS01 sensitivities", "input_data": "synthetic corporate bonds + ICE BofA OAS-compatible factors", "validation_tests": "duration/sensitivity sanity tests; maturity/rating bucket checks", "limitations": "Synthetic positions, index-level spreads, no issuer-level TRACE history", "control": "claim boundary, scenario stress, sensitivity report"},
        {"model_id": "M-003", "model_name": "Securitized-Products Proxy Waterfall", "purpose": "Mortgage-pool cash-flow and senior/mezz/equity tranche proxy", "input_data": "public-performance-compatible mortgage schema or deterministic fallback", "validation_tests": "cash-flow conservation; tranche priority; stress monotonicity", "limitations": "Proxy only; not production MBS/ABS pricing", "control": "explicit proxy memo, prepayment/default/severity scenarios"},
        {"model_id": "M-004", "model_name": "VaR/ES/Stressed VaR Engine", "purpose": "Historical, Monte Carlo, Student-t VaR, ES, 10-day scaling, stressed VaR", "input_data": "portfolio loss panel", "validation_tests": "rolling 250-day 99% VaR backtest; Kupiec; Christoffersen; exception severity", "limitations": "Offline portfolio benchmark, not regulatory capital certification", "control": "backtesting report, assumption matrix, release gate"},
        {"model_id": "M-005", "model_name": "Specialty Reliability Layer", "purpose": "Market Health Timestep, residual VaR correction, conservative envelope, false-safe diagnostics", "input_data": "loss panel + backtesting exceptions", "validation_tests": "specialty ablation; false-safe rate; coverage-overreach diagnostics", "limitations": "Research-inspired model-development enhancement; not approved regulatory overlay", "control": "specialty contribution report and ablation table"},
        {"model_id": "M-006", "model_name": "P&L Attribution Proxy", "purpose": "Compare actual-vs-hypothetical proxy P&L and unexplained residuals", "input_data": "portfolio loss components", "validation_tests": "correlation gate; unexplained residual ratio gate; dominant-factor attribution", "limitations": "Proxy only; no real desk P&L or official PLA test", "control": "P&L attribution proxy report and claim boundary"},
        {"model_id": "M-007", "model_name": "FRTB-Inspired Diagnostics", "purpose": "ES, liquidity-horizon, and modellability-proxy review diagnostics", "input_data": "loss components by risk-factor family", "validation_tests": "observation count; ES 97.5%; liquidity-horizon scaled ES proxy", "limitations": "Not an official FRTB implementation", "control": "FRTB-inspired diagnostics report"},
        {"model_id": "M-008", "model_name": "Champion/Challenger VaR Selection", "purpose": "Compare vanilla, residual-corrected, and conservative-envelope VaR variants", "input_data": "backtesting and specialty diagnostics", "validation_tests": "exception rate, false-safe rate, overreach proxy, complexity penalty", "limitations": "Review score is a transparent proxy, not model committee approval", "control": "challenger model selection report"},
        {"model_id": "M-009", "model_name": "Reverse Stress Diagnostics", "purpose": "Estimate stress multipliers needed to exceed VaR/ES thresholds", "input_data": "scenario stress losses and VaR/ES outputs", "validation_tests": "multiplier-to-VaR/ES and scenario priority classification", "limitations": "Scenario library is synthetic/proxy-based", "control": "reverse stress testing report"},
        {"model_id": "M-010", "model_name": "Reproducibility Manifest", "purpose": "Hash code, configs, reports, tests, and outputs for local/GitHub repeatability", "input_data": "repository files", "validation_tests": "SHA-256 file manifest and metadata generation", "limitations": "Engineering control, not formal audit certification", "control": "manifest report and run_all_checks.py"},
    ]
    out = pd.DataFrame(rows)
    out_path = root / 'outputs' / 'model_inventory.csv'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    return out


def generate_public_data_readiness(root: Path, source: str, mortgage_source: str) -> None:
    reports = root / 'reports'
    outputs = root / 'outputs'
    catalog_path = root / 'data' / 'cached_samples' / 'public_data_source_catalog.csv'
    catalog = _safe_read_csv(catalog_path)
    if not catalog.empty:
        catalog.to_csv(outputs / 'public_data_source_catalog.csv', index=False)
        n_rate = int((catalog['domain'] == 'rates').sum())
        n_credit = int((catalog['domain'] == 'credit_spread').sum())
        n_mortgage = int((catalog['domain'] == 'mortgage_proxy').sum())
    else:
        n_rate = n_credit = n_mortgage = 0

    write_markdown(reports / 'public_data_readiness_report.md', 'Public Data Readiness Report', [
        ('Executed source mode', f'Market data source mode: `{source}`. Mortgage source mode: `{mortgage_source}`.'),
        ('Source coverage', f'The source catalog maps {n_rate} Treasury/rate fields, {n_credit} corporate-credit spread fields, and {n_mortgage} mortgage-proxy fields to framework columns.'),
        ('Live download boundary', 'The project includes live FRED adapters for internet-enabled environments, but the submitted validation run uses cached public-compatible samples or deterministic fallback to remain reproducible without proprietary data.'),
        ('Evidence files', '`outputs/public_data_source_catalog.csv`, `outputs/risk_factor_panel.csv`, `outputs/data_quality_exceptions.csv`, and `reports/market_data_validation_report.md` document source readiness and schema compatibility.'),
        ('Claim boundary', 'A cached public-compatible sample is not represented as audited historical market data. It demonstrates schema compatibility, reproducibility, and model-development workflow readiness.'),
    ])


def generate_jpmc_role_alignment(root: Path) -> None:
    write_markdown(root / 'reports' / 'jpmc_market_risk_role_alignment.md', 'JPMC Market Risk Model Development Role Alignment', [
        ('Positioning', 'This project is positioned as a role-specific offline framework for fixed-income market-risk model development, not as a generic ML or fraud-risk project.'),
        ('Strong evidence', 'The strongest evidence is fixed-income pricing and sensitivities, corporate-credit spread factors, securitized-products proxy cash flows, VaR/ES/stressed VaR, rolling 250-day backtesting, assumption-impact analysis, and model-risk documentation.'),
        ('Relevant qualifications shown', 'Probability, time-series analysis, stress testing, backtesting, alternative assumption evaluation, Python implementation, model validation, documentation, and stakeholder-ready reporting are represented by executable artifacts.'),
        ('Remaining gap', 'The project does not replace professional fixed-income trading quant experience. Resume language should frame it as an offline, public-data-compatible portfolio framework under explicit synthetic/proxy boundaries.'),
        ('Suggested interview narrative', 'Lead with the end-to-end model-development lifecycle: data validation, risk-factor construction, valuation and sensitivities, VaR/ES/stress, backtesting, assumption impact, specialty reliability layer, and governance packet.'),
    ])


def generate_reports(root: Path, context: dict) -> None:
    reports = root / 'reports'
    reports.mkdir(parents=True, exist_ok=True)
    source = context.get('data_source', 'deterministic_synthetic_fallback')
    mortgage_source = context.get('mortgage_source', 'deterministic_synthetic_fallback')
    var99 = context.get('historical_var_99', 0.0)
    es99 = context.get('historical_es_99', 0.0)
    stressed = context.get('stressed_var_99', 0.0)
    release = context.get('release_status', 'REVIEW')

    inventory = generate_model_inventory(root)
    generate_public_data_readiness(root, source, mortgage_source)
    generate_jpmc_role_alignment(root)

    write_markdown(reports / 'market_data_validation_report.md', 'Market Data Validation Report', [
        ('Scope', f'Validated Treasury-rate and corporate-credit spread panels using source mode `{source}`.'),
        ('Checks', 'Business-day alignment, missing observations, stale quote runs, outlier spread/rate moves, and data-lineage summaries were generated.'),
        ('Public source mapping', 'The framework maps Federal Reserve H.15/FRED Treasury series and FRED ICE BofA corporate OAS series to internal risk-factor columns through `public_data_source_catalog.csv`.'),
        ('Claim boundary', 'Public-data-compatible schemas, cached samples, and deterministic synthetic fallback are used; no proprietary market data is claimed.'),
    ])
    write_markdown(reports / 'risk_factor_methodology.md', 'Risk Factor Methodology', [
        ('Rate factors', 'Treasury curve level, slope, and curvature shocks are constructed from constant-maturity style rates.'),
        ('Credit spread factors', 'IG, HY, and rating-bucket OAS shock proxies are constructed from corporate spread series.'),
        ('Covariance and correlation', 'The merged panel supports portfolio loss simulation, stressed correlation comparisons, and assumption-impact analysis.'),
    ])
    write_markdown(reports / 'corporate_credit_portfolio_report.md', 'Corporate Credit Portfolio Report', [
        ('Portfolio', 'Synthetic corporate bonds are generated across rating, sector, coupon, notional, and maturity buckets.'),
        ('Sensitivities', 'Spread-adjusted pricing, DV01, CS01/OAS01, duration proxy, and risk contribution tables are produced.'),
        ('Hiring-manager signal', 'This module separates fixed-income valuation and sensitivity basics from generic VaR calculation.'),
    ])
    write_markdown(reports / 'securitized_products_proxy_report.md', 'Securitized Products Proxy Report', [
        ('Proxy design', f'A public mortgage-performance/disclosure-compatible schema feeds a synthetic loan pool and tranche waterfall using source mode `{mortgage_source}`.'),
        ('Cashflow logic', 'Scheduled principal, prepayment proxy, default proxy, severity/recovery, WAL, tranche loss, and liquidity spread stress are modeled.'),
        ('Boundary', 'This is not a production MBS/ABS model and does not claim instrument-level desk pricing.'),
    ])
    write_markdown(reports / 'var_es_methodology.md', 'VaR and Expected Shortfall Methodology', [
        ('Methods', 'Historical simulation VaR, Monte Carlo VaR, Student-t VaR, Expected Shortfall, 10-day sqrt-time scaling, and stressed VaR are calculated.'),
        ('Headline validation-run results', f'Historical 99% VaR: {var99:,.2f}; Historical 99% ES: {es99:,.2f}; stressed VaR: {stressed:,.2f}.'),
        ('Boundary', 'These values are produced from an offline synthetic/proxy portfolio and are not represented as bank regulatory capital estimates.'),
    ])
    write_markdown(reports / 'stress_testing_report.md', 'Stress Testing Report', [
        ('Scenario library', 'Parallel rate shock, curve proxy shock, IG/HY spread widening, liquidity spread shock, and mortgage default/severity shock are evaluated.'),
        ('Use', 'Stress losses complement VaR and ES because VaR alone can miss stressed-but-plausible joint moves.'),
    ])
    write_markdown(reports / 'backtesting_report.md', 'Backtesting Report', [
        ('Method', 'Rolling 250-day, one-day 99% VaR backtesting is used with exception count, Kupiec POF, Christoffersen independence, and exception severity.'),
        ('Result', f'Release-gate status from backtesting and false-safe diagnostics: `{release}`.'),
    ])
    write_markdown(reports / 'assumption_impact_report.md', 'Assumption Impact Report', [
        ('Compared assumptions', 'Historical vs Monte Carlo VaR, Gaussian vs Student-t tails, rolling vs EWMA volatility, 1-day vs 10-day horizon, stressed correlation, delta-gamma uplift, and securitized proxy stresses.'),
        ('Purpose', 'This converts model development from a single point estimate into an explicit comparison of modeling choices and limitations.'),
    ])
    write_markdown(reports / 'specialty_contribution_report.md', 'Specialty Contribution Report', [
        ('Market Health Timestep', "Regime-aligned market-health states adapt the user's health-timestep research logic to market-risk time-series validation."),
        ('Residual VaR correction', 'Backtesting residuals inform conservative VaR correction without claiming regulatory approval.'),
        ('Conservative risk envelope', 'A tail-risk envelope is used to reduce false-safe diagnostics while tracking coverage-overreach tradeoffs.'),
    ])
    write_markdown(reports / 'model_inventory.md', 'Model Inventory', [
        ('Inventory scope', f'{len(inventory)} model components are registered in `outputs/model_inventory.csv` with purpose, inputs, validation tests, limitations, and controls.'),
        ('Use', 'This inventory is designed for model-risk review and interview discussion, not formal bank model registration.'),
    ])
    write_markdown(reports / 'model_validation_memo.md', 'Model Validation Memo', [
        ('Model purpose', 'Offline fixed-income market-risk model development and validation for synthetic corporate-credit and securitized-products proxy portfolios.'),
        ('Validation tests', 'Data-quality checks, benchmark comparison, VaR/ES calculations, stress testing, backtesting, assumption sensitivity, specialty ablation, and release gates.'),
        ('Model inventory', '`outputs/model_inventory.csv` links each component to purpose, inputs, tests, limitations, and controls.'),
        ('Limitations', 'No proprietary data, no production deployment, no official regulatory capital certification.'),
    ])
    write_markdown(reports / 'regulatory_mapping_memo.md', 'Regulatory-Style Mapping Memo', [
        ('VaR and stressed VaR', 'The framework mirrors regulatory-style concepts around daily VaR, stressed VaR, and backtesting but is not a regulatory capital model.'),
        ('Backtesting', 'The backtesting design follows a 250-business-day, one-day 99% VaR exception-analysis pattern.'),
        ('Securitized products', 'Securitized exposure is represented by a synthetic proxy with explicit model limitations and compensating controls.'),
        ('Boundary', 'Regulatory-style and FRTB-inspired wording is used only for educational model-development artifacts; no compliance certification is claimed.'),
    ])
    write_markdown(reports / 'known_limitations.md', 'Known Limitations', [
        ('Data', 'Synthetic fallback or cached public-compatible data is not a substitute for audited market data, TRACE history, Bloomberg marks, or desk P&L.'),
        ('Portfolio', 'Synthetic positions approximate risk exposures but are not real bank positions.'),
        ('Securitized proxy', 'The tranche waterfall is a structural proxy, not production instrument valuation.'),
        ('Experience boundary', 'The project demonstrates technical readiness but does not represent professional fixed-income trading-desk employment.'),
    ])
    write_markdown(reports / 'compensating_controls.md', 'Compensating Controls', [
        ('Controls', 'Claim boundary, reproducible seed, data-lineage report, source catalog, synthetic fallback, backtesting diagnostics, model-risk findings, and conservative release gate.'),
    ])
    write_markdown(reports / 'executive_risk_summary.md', 'Executive Risk Summary', [
        ('Summary', f'The framework generated fixed-income VaR/ES, stress, backtesting, specialty ablation, source-readiness, and governance outputs with final release status `{release}`.'),
        ('Decision', 'Use as an offline model-development artifact and interview evidence, not as a production risk engine.'),
        ('JPMC relevance', 'The artifact is strongest for market-risk model development, model-performance testing, assumption-impact analysis, and regulatory-style model documentation.'),
    ])
