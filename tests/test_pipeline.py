from pathlib import Path
from fimrf.pipeline import run_pipeline


def test_pipeline_end_to_end(tmp_path):
    # Copy-less run into temp project-like root.
    result = run_pipeline(tmp_path)
    assert result["release_status"] in {"PASS", "REVIEW", "BLOCK"}
    assert (tmp_path / "outputs" / "run_summary.json").exists()
    assert (tmp_path / "reports" / "model_validation_memo.md").exists()
