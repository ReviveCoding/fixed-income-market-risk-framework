from fimrf.data_ingestion.synthetic_fallback import generate_market_data
from fimrf.instruments.corporate_bond import generate_corporate_bonds, compute_sensitivities


def test_corporate_bond_sensitivities_positive():
    rates, spreads = generate_market_data(n_days=300)
    positions = generate_corporate_bonds(n=20)
    sens = compute_sensitivities(positions, rates, spreads)
    assert len(sens) == 20
    assert sens["market_value"].sum() > 0
    assert sens["dv01"].sum() > 0
    assert sens["cs01"].sum() > 0
