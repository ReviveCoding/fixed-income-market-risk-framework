from __future__ import annotations

from pathlib import Path
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def ensure_dirs(*paths: str | Path) -> None:
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)


def write_json(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def write_markdown(path: str | Path, title: str, sections: list[tuple[str, str]]) -> None:
    """Write a report with stable section spacing and UTF-8 encoding."""
    lines = [f"# {title}\n"]
    for heading, body in sections:
        lines.append(f"## {heading}\n\n{body.strip()}\n")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def save_table(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        try:
            df.to_parquet(path, index=False)
        except Exception:
            df.to_csv(path.with_suffix(".csv"), index=False)
    else:
        df.to_csv(path, index=False)


def chi2_sf_df1(x: float) -> float:
    if x <= 0:
        return 1.0
    return math.erfc(math.sqrt(x / 2.0))


def chi2_sf_df2(x: float) -> float:
    if x <= 0:
        return 1.0
    return math.exp(-x / 2.0)


def pct(x: float) -> str:
    return f"{100 * x:.2f}%"
