from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None


def main(root: str = ".") -> None:
    if st is None:
        print("Streamlit is optional. Install streamlit to run the dashboard.")
        return
    root = Path(root)
    st.title("Fixed-Income Market Risk Framework")
    summary_path = root / "outputs" / "run_summary.json"
    if summary_path.exists():
        st.json(json.loads(summary_path.read_text()))
    for name in ["var_es_by_portfolio.csv", "stress_loss_by_scenario.csv", "kupiec_christoffersen_results.csv", "assumption_sensitivity_matrix.csv"]:
        path = root / "outputs" / name
        if path.exists():
            st.subheader(name)
            st.dataframe(pd.read_csv(path))

if __name__ == "__main__":
    main()
