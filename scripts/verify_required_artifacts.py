from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "PROJECT_CARD.md",
    "VALIDATION_REPORT.md",
    "Makefile",
    "pyproject.toml",
    "requirements.txt",
    ".github/workflows/ci.yml",
    "Dockerfile",
    "outputs/run_summary.json",
    "outputs/release_decision.json",
    "outputs/model_inventory.csv",
    "outputs/reproducibility_manifest.csv",
    "reports/local_github_runnability_audit.md",
    "reports/model_validation_memo.md",
    "reports/regulatory_mapping_memo.md",
    "reports/reproducibility_manifest_report.md",
]

missing = [path for path in REQUIRED if not (ROOT / path).exists()]
if missing:
    raise SystemExit("Missing required artifacts: " + ", ".join(missing))

summary = json.loads((ROOT / "outputs/run_summary.json").read_text())
release = json.loads((ROOT / "outputs/release_decision.json").read_text())
if summary.get("release_status") != "PASS":
    raise SystemExit(f"Run summary is not PASS: {summary.get('release_status')}")
if release.get("release_status") != "PASS":
    raise SystemExit(f"Release decision is not PASS: {release.get('release_status')}")
print("Required artifact verification passed.")
