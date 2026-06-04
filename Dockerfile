FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt pyproject.toml README.md ./
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt
COPY src ./src
RUN python -m pip install --no-cache-dir -e . --no-deps
COPY configs ./configs
COPY scripts ./scripts
COPY tests ./tests
COPY data ./data
ENV PYTHONPATH=/app/src
CMD ["bash", "-lc", "python scripts/create_public_compatible_samples.py && python scripts/run_pipeline.py && python scripts/run_small_data_validation.py && python -m pytest -q && python scripts/verify_required_artifacts.py"]
