from __future__ import annotations

from pathlib import Path
import hashlib
import json
import platform
import sys
import pandas as pd


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_reproducibility_manifest(root: Path) -> tuple[pd.DataFrame, dict]:
    """Create file-hash manifest for configs, source code, scripts, tests, reports, and outputs."""
    include_dirs = ["configs", "src", "scripts", "tests", "reports", "outputs"]
    rows = []
    for d in include_dirs:
        base = root / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".pyc":
                continue
            # Avoid hashing very large artifacts if a future user adds them.
            size = p.stat().st_size
            if size > 10 * 1024 * 1024:
                continue
            rows.append({
                "relative_path": str(p.relative_to(root)).replace("\\", "/"),
                "bytes": int(size),
                "sha256": sha256_file(p),
            })
    manifest = pd.DataFrame(rows)
    metadata = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "file_count": int(len(manifest)),
        "total_hashed_bytes": int(manifest["bytes"].sum()) if not manifest.empty else 0,
        "claim_boundary": "offline/public-data-compatible/synthetic-portfolio/proxy framework; not production or regulatory-certified",
    }
    return manifest, metadata
