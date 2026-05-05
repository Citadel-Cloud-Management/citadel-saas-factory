FROM python:3.12-slim AS base

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

# Install dependencies in a separate layer for better caching
FROM base AS deps
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

FROM deps AS production

COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
