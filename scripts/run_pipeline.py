from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fimrf.pipeline import run_pipeline

if __name__ == "__main__":
    result = run_pipeline(ROOT)
    print("Pipeline completed")
    print(result)
