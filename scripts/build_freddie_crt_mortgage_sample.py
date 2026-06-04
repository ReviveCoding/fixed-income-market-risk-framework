from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_public" / "freddie_crt"
OUT_DIR = ROOT / "data" / "cached_samples"
REPORT_DIR = ROOT / "reports"
OUTPUT_DIR = ROOT / "outputs"

OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT = OUT_DIR / "mortgage_pool_sample.csv"
SUMMARY_CSV = OUTPUT_DIR / "freddie_crt_sample_summary.csv"
REPORT_MD = REPORT_DIR / "freddie_crt_sample_build_report.md"


def col(df: pd.DataFrame, idx: int, default=None) -> pd.Series:
    if idx < df.shape[1]:
        return df.iloc[:, idx]
    return pd.Series([default] * len(df), index=df.index)


def num(s: pd.Series, default=np.nan) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    if default is not np.nan:
        x = x.fillna(default)
    return x


def clean_9999(x: pd.Series) -> pd.Series:
    return x.mask(x >= 9999, np.nan)


def read_lld_no_header(path: Path, nrows: int = 30000) -> pd.DataFrame:
    # Freddie CRT *_lld.txt files downloaded here are pipe-delimited and headerless.
    return pd.read_csv(
        path,
        sep="|",
        header=None,
        dtype=str,
        nrows=nrows,
        low_memory=False,
        encoding_errors="ignore",
    )


def normalize_one(path: Path, max_rows: int = 30000) -> pd.DataFrame:
    df = read_lld_no_header(path, nrows=max_rows)

    deal = path.name.split("_")[0].upper()
    is_hqa = "HQA" in deal
    is_dna = "DNA" in deal
    pool_type = "high_ltv_hqa" if is_hqa else ("low_ltv_dna" if is_dna else "unknown")

    # Positional mapping from observed Freddie CRT monthly LLD structure.
    # Core fields used by this project:
    # 0 reporting period, 1 deal, 2 loan id, 10 term, 11 note/coupon rate,
    # 12 original balance, 13 current/upb-like balance,
    # 22 credit score, 23/24 LTV-style fields observed in downloaded CRT LLD files.
    loan_id = col(df, 2).astype(str).str.strip()
    term_months = num(col(df, 10), 360).clip(lower=1, upper=480)
    coupon = num(col(df, 11), 6.5)
    original_balance = num(col(df, 12))
    current_balance = num(col(df, 13))
    balance = current_balance.where(current_balance.notna() & (current_balance > 0), original_balance)

    fico = clean_9999(num(col(df, 22))).fillna(720).clip(lower=300, upper=850)

    ltv_1 = clean_9999(num(col(df, 23)))
    ltv_2 = clean_9999(num(col(df, 24)))
    ltv = (
        pd.concat([ltv_1, ltv_2], axis=1)
        .max(axis=1)
        .fillna(90 if is_hqa else 75)
        .clip(lower=1, upper=150)
    )

    # Project proxy fields, not Freddie official delinquency/prepayment fields.
    # This keeps the claim boundary safe while using real CRT loan attributes.
    delinquency_proxy = np.clip(
        0.005
        + np.maximum(ltv - 80, 0) * 0.003
        + np.maximum(700 - fico, 0) * 0.0007
        + (0.010 if is_hqa else 0.000),
        0.0,
        0.35,
    )

    prepay_score = np.clip(
        0.025
        + np.maximum(fico - 700, 0) * 0.00004
        + np.maximum(80 - ltv, 0) * 0.00020
        - np.maximum(coupon - 6.75, 0) * 0.003,
        0.005,
        0.20,
    )

    out = pd.DataFrame(
        {
            "loan_id": loan_id,
            "balance": balance.fillna(balance.median()).clip(lower=1000),
            "coupon": coupon.fillna(coupon.median()).clip(lower=0.01, upper=20),
            "term_months": term_months.fillna(360),
            "fico": fico,
            "ltv": ltv,
            "delinquency_proxy": delinquency_proxy,
            "prepay_score": prepay_score,
            "deal": deal,
            "pool_type": pool_type,
            "source_file": path.name,
        }
    )

    out = out.dropna(subset=["loan_id", "balance"])
    out = out[out["loan_id"].astype(str).str.len() > 0]
    return out


def main() -> None:
    files = [
        RAW_DIR / "26DNA2_20260501_lld.txt",
        RAW_DIR / "26DNA1_20260501_lld.txt",
        RAW_DIR / "25HQA1_20260501_lld.txt",
    ]
    existing = [p for p in files if p.exists()]
    if not existing:
        raise FileNotFoundError(f"No Freddie CRT files found in {RAW_DIR}")

    frames = [normalize_one(p) for p in existing]
    full = pd.concat(frames, ignore_index=True)

    # Keep the sample manageable and balanced enough for local reruns.
    # Avoid groupby.apply here because recent pandas versions can drop grouping columns
    # from the returned DataFrame depending on apply/include_groups behavior.
    sample_parts = []
    for _, grp in full.groupby(["pool_type", "deal"], dropna=False, sort=True):
        n = min(len(grp), 1500)
        sample_parts.append(grp.sample(n=n, random_state=42))

    sample = pd.concat(sample_parts, ignore_index=True)

    core_cols = [
        "loan_id",
        "balance",
        "coupon",
        "term_months",
        "fico",
        "ltv",
        "delinquency_proxy",
        "prepay_score",
    ]
    trace_cols = ["deal", "pool_type", "source_file"]

    sample[core_cols + trace_cols].to_csv(OUTPUT, index=False)

    summary = (
        sample.groupby(["pool_type", "deal", "source_file"])
        .agg(
            loans=("loan_id", "count"),
            avg_balance=("balance", "mean"),
            avg_coupon=("coupon", "mean"),
            avg_fico=("fico", "mean"),
            avg_ltv=("ltv", "mean"),
            avg_delinquency_proxy=("delinquency_proxy", "mean"),
            avg_prepay_score=("prepay_score", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(SUMMARY_CSV, index=False)

    report = f"""# Freddie Mac CRT Mortgage Sample Build Report

## Source files

{chr(10).join(f"- {p.name}" for p in existing)}

## Output

- `{OUTPUT.relative_to(ROOT)}`
- `{SUMMARY_CSV.relative_to(ROOT)}`

## Claim boundary

This adapter uses real Freddie Mac CRT monthly loan-level disclosure rows from STACR DNA/HQA files, but it creates project-specific proxy fields for delinquency and prepayment. It does not claim to reproduce Freddie Mac official performance modeling, official delinquency reporting, official prepayment modeling, or production securitized-products valuation.

## Sample summary

{summary.to_markdown(index=False)}

## Numeric summary

{sample[core_cols].describe().to_markdown()}
"""
    REPORT_MD.write_text(report, encoding="utf-8")

    print(f"Wrote {OUTPUT}")
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {REPORT_MD}")
    print(summary.to_string(index=False))
    print(sample[core_cols].describe().to_string())


if __name__ == "__main__":
    main()
