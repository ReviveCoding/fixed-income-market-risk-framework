
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from fimrf.data_ingestion.synthetic_fallback import generate_market_data, generate_mortgage_pool
from fimrf.data_ingestion.public_source_catalog import build_source_catalog


def main() -> None:
    cached = ROOT / 'data' / 'cached_samples'
    cached.mkdir(parents=True, exist_ok=True)
    rates, spreads = generate_market_data(n_days=900, seed=202617)
    mortgage = generate_mortgage_pool(n_loans=800, seed=202618)
    rates.to_csv(cached / 'rates_sample.csv', index=False)
    spreads.to_csv(cached / 'oas_sample.csv', index=False)
    mortgage.to_csv(cached / 'mortgage_pool_sample.csv', index=False)
    build_source_catalog().to_csv(cached / 'public_data_source_catalog.csv', index=False)
    print(f'Wrote cached public-compatible samples to {cached}')


if __name__ == '__main__':
    main()
