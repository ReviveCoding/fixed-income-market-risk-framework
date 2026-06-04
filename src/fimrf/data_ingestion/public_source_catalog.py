
from __future__ import annotations

import pandas as pd

RATE_SOURCE_CATALOG = [
    {"domain": "rates", "framework_column": "DGS1MO", "official_series_id": "DGS1MO", "source": "Federal Reserve H.15 via FRED", "role": "1-month Treasury constant maturity / bill-style short-rate factor"},
    {"domain": "rates", "framework_column": "DGS3MO", "official_series_id": "DGS3MO", "source": "Federal Reserve H.15 via FRED", "role": "3-month Treasury short-rate factor"},
    {"domain": "rates", "framework_column": "DGS6MO", "official_series_id": "DGS6MO", "source": "Federal Reserve H.15 via FRED", "role": "6-month Treasury short-rate factor"},
    {"domain": "rates", "framework_column": "DGS1", "official_series_id": "DGS1", "source": "Federal Reserve H.15 via FRED", "role": "1-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS2", "official_series_id": "DGS2", "source": "Federal Reserve H.15 via FRED", "role": "2-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS3", "official_series_id": "DGS3", "source": "Federal Reserve H.15 via FRED", "role": "3-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS5", "official_series_id": "DGS5", "source": "Federal Reserve H.15 via FRED", "role": "5-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS7", "official_series_id": "DGS7", "source": "Federal Reserve H.15 via FRED", "role": "7-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS10", "official_series_id": "DGS10", "source": "Federal Reserve H.15 via FRED", "role": "10-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS20", "official_series_id": "DGS20", "source": "Federal Reserve H.15 via FRED", "role": "20-year Treasury curve point"},
    {"domain": "rates", "framework_column": "DGS30", "official_series_id": "DGS30", "source": "Federal Reserve H.15 via FRED", "role": "30-year Treasury curve point"},
]

OAS_SOURCE_CATALOG = [
    {"domain": "credit_spread", "framework_column": "IG_OAS", "official_series_id": "BAMLC0A0CM", "source": "FRED ICE BofA US Corporate Index OAS", "role": "investment-grade corporate credit spread factor"},
    {"domain": "credit_spread", "framework_column": "HY_OAS", "official_series_id": "BAMLH0A0HYM2", "source": "FRED ICE BofA US High Yield Index OAS", "role": "high-yield corporate credit spread factor"},
    {"domain": "credit_spread", "framework_column": "A_OAS", "official_series_id": "BAMLC0A3CA", "source": "FRED ICE BofA Single-A US Corporate Index OAS", "role": "A-rated corporate credit spread factor"},
    {"domain": "credit_spread", "framework_column": "BBB_OAS", "official_series_id": "BAMLC0A4CBBB", "source": "FRED ICE BofA BBB US Corporate Index OAS", "role": "BBB-rated corporate credit spread factor"},
    {"domain": "credit_spread", "framework_column": "BB_OAS", "official_series_id": "BAMLH0A1HYBB", "source": "FRED ICE BofA BB US High Yield Index OAS", "role": "BB-rated high-yield spread factor"},
    {"domain": "credit_spread", "framework_column": "B_OAS", "official_series_id": "BAMLH0A2HYB", "source": "FRED ICE BofA Single-B US High Yield Index OAS", "role": "B-rated high-yield spread factor"},
    {"domain": "credit_spread", "framework_column": "CCC_OAS", "official_series_id": "BAMLH0A3HYC", "source": "FRED ICE BofA CCC & Lower US High Yield Index OAS", "role": "CCC-and-lower high-yield spread factor"},
]

MORTGAGE_SOURCE_CATALOG = [
    {"domain": "mortgage_proxy", "framework_column": "fico", "official_series_id": "Freddie/Fannie-style loan performance field", "source": "Freddie Mac/Fannie Mae loan performance schema", "role": "borrower credit-quality proxy for prepayment/default stress"},
    {"domain": "mortgage_proxy", "framework_column": "ltv", "official_series_id": "Freddie/Fannie-style loan performance field", "source": "Freddie Mac/Fannie Mae loan performance schema", "role": "collateral leverage proxy for default/severity stress"},
    {"domain": "mortgage_proxy", "framework_column": "balance", "official_series_id": "Freddie/Fannie-style loan performance field", "source": "Freddie Mac/Fannie Mae loan performance schema", "role": "loan balance supporting pool cash-flow and tranche waterfall"},
    {"domain": "mortgage_proxy", "framework_column": "delinquency_proxy", "official_series_id": "derived from loan performance status", "source": "public-performance-compatible proxy", "role": "default transition proxy; not actual loan-level disclosure"},
]


def build_source_catalog() -> pd.DataFrame:
    return pd.DataFrame(RATE_SOURCE_CATALOG + OAS_SOURCE_CATALOG + MORTGAGE_SOURCE_CATALOG)
