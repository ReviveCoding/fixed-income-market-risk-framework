"""Formatting and numerical utility contracts."""

import json

import pytest

from fimrf.utils import chi2_sf_df1, chi2_sf_df2, pct, write_json, write_markdown


def test_report_writers_preserve_bytes_and_create_parent(tmp_path):
    output = tmp_path / "nested"
    write_markdown(output / "report.md", "Risk Report", [("Results", " metrics ")])
    assert (output / "report.md").read_text(encoding="utf-8") == (
        "# Risk Report\n\n## Results\n\nmetrics\n"
    )
    write_json(output / "result.json", {"status": "PASS"})
    assert json.loads((output / "result.json").read_text(encoding="utf-8")) == {"status": "PASS"}


def test_chi_square_survival_boundaries_and_percentage():
    assert chi2_sf_df1(0) == 1.0
    assert chi2_sf_df2(0) == 1.0
    assert chi2_sf_df2(2) == pytest.approx(0.36787944117144233)
    assert pct(0.125) == "12.50%"
