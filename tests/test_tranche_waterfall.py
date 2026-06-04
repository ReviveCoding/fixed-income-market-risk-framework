from fimrf.data_ingestion.synthetic_fallback import generate_mortgage_pool
from fimrf.instruments.securitized_proxy import build_tranche_cashflows, securitized_scenario_stress


def test_tranche_waterfall_outputs():
    pool = generate_mortgage_pool(n_loans=100)
    cf, summary = build_tranche_cashflows(pool, months=24)
    stress = securitized_scenario_stress(summary)
    assert set(summary["tranche"]) == {"Senior", "Mezzanine", "Equity"}
    assert len(cf) == 72
    assert not stress.empty
