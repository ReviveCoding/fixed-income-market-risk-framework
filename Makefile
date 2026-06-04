PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e . --no-deps

run:
	$(PYTHON) scripts/run_pipeline.py

test:
	$(PYTHON) -m pytest -q

verify-artifacts:
	$(PYTHON) scripts/verify_required_artifacts.py

clean:
	rm -rf .pytest_cache **/__pycache__ **/*.pyc build dist *.egg-info

small-validate:
	$(PYTHON) scripts/run_small_data_validation.py

all-checks:
	$(PYTHON) scripts/run_all_checks.py

ci-local: all-checks
