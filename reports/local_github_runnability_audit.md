# Local and GitHub Runnability Audit

## Local commands

`python scripts/create_public_compatible_samples.py`, `python scripts/run_pipeline.py`, `python scripts/run_small_data_validation.py`, and `pytest -q` are the canonical local checks.

## GitHub-ready artifacts

The project includes requirements, pyproject, Makefile, tests, deterministic cached samples, deterministic fallback, governance reports, and GitHub Actions CI workflow.

## Cleanup

Generated Python bytecode and pytest cache are excluded from the packaged artifact. Runtime outputs are reproducible and can be regenerated.

## Remaining caveat

Live public downloads require internet access. The default repository path remains offline-runnable through cached public-compatible samples and deterministic fallback.
