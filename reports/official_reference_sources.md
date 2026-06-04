# Official Reference Sources

This project uses public-data-compatible schemas and optional live-data adapters. The submitted validation run uses cached public-compatible samples, not audited market data.

## Treasury / Rates

- Federal Reserve H.15 Selected Interest Rates: official daily selected interest rates release.
- FRED H.15 release/series endpoints: optional CSV download route for Treasury constant maturity series such as DGS1, DGS2, DGS5, DGS10, and DGS30.

## Corporate Credit Spreads

- FRED ICE BofA corporate option-adjusted spread series, including investment-grade and high-yield OAS factors.
- Framework examples include BAMLC0A0CM, BAMLH0A0HYM2, BAMLC0A3CA, BAMLC0A4CBBB, BAMLH0A1HYBB, BAMLH0A2HYB, and BAMLH0A3HYC.

## Mortgage / Securitized-Products Proxy

- Freddie Mac Single-Family Loan-Level Dataset and Fannie Mae Single-Family Loan Performance Data are used only as schema references for mortgage-performance-compatible proxy design.
- This project does not redistribute restricted loan-level data and does not claim production securitized-products valuation.

## Market Risk Backtesting

- 12 CFR 217.204 is used as a regulatory-style reference for 250-business-day, one-day, one-tail 99% VaR backtesting design.
- The project does not claim regulatory capital compliance or certification.
