from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + ENV.get("PYTHONPATH", "")
commands = [
    [sys.executable, "-m", "pip", "install", "-e", ".", "--no-deps"],
    [sys.executable, "-c", "import fimrf; print('fimrf import ok')"],
    [sys.executable, "scripts/create_public_compatible_samples.py"],
    [sys.executable, "scripts/run_pipeline.py"],
    [sys.executable, "scripts/run_small_data_validation.py"],
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "scripts/verify_required_artifacts.py"],
]

for cmd in commands:
    print("\n$", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True, env=ENV)
print("\nAll local/GitHub runnable checks passed.")
