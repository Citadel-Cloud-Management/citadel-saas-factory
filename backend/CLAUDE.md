# Backend — FastAPI

- Python 3.12, FastAPI 0.115+, SQLAlchemy 2.0+
- Run: `cd backend && pip install -e ".[dev]" && uvicorn app.main:app --reload`
- Test: `pytest --cov=app --cov-report=term-missing`
- Lint: `ruff check . && ruff format --check .`
- Architecture: Clean layers — routes -> services -> repositories -> models
- All endpoints under /api/v1/
- Pydantic schemas for request/response validation
- Alembic for database migrations
- Async-first: use async def for all endpoints
- Multi-tenant: tenant_id set via middleware on every request
