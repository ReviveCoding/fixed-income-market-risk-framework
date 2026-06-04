
from pathlib import Path
import pandas as pd
from fimrf.pipeline import run_pipeline


def test_governance_and_source_readiness_artifacts(tmp_path):
    result = run_pipeline(tmp_path)
    assert result['release_status'] in {'PASS', 'REVIEW', 'BLOCK'}
    assert (tmp_path / 'outputs' / 'model_inventory.csv').exists()
    inventory = pd.read_csv(tmp_path / 'outputs' / 'model_inventory.csv')
    assert {'model_id', 'model_name', 'purpose', 'limitations', 'control'}.issubset(inventory.columns)
    assert len(inventory) >= 5
    assert (tmp_path / 'reports' / 'public_data_readiness_report.md').exists()
    assert (tmp_path / 'reports' / 'jpmc_market_risk_role_alignment.md').exists()
