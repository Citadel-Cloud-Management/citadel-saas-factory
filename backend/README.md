# Backend — FastAPI (Python 3.12)

REST/GraphQL API with SQLAlchemy ORM and Alembic migrations.

## Run

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

## Structure

```
app/
├── main.py           Application entrypoint, middleware registration
├── api/v1/           Versioned API routers
├── auth/             Keycloak integration, JWT validation, RBAC
├── core/             Config, database, logging, base classes
├── middleware/        Audit, CORS, rate limiting, guardrails, metrics
├── models/           SQLAlchemy ORM models
├── schemas/          Pydantic request/response schemas
├── services/         Business logic layer
├── repositories/     Data access layer (repository pattern)
├── events/           RabbitMQ event producers/consumers
├── workers/          Background task processors
└── routes/           API route definitions
```

## Test

```bash
pytest --cov=app --cov-report=html
```

## Add an Endpoint

1. Create schema in `app/schemas/`
2. Create model in `app/models/`
3. Create repository in `app/repositories/`
4. Create service in `app/services/`
5. Create route in `app/routes/`
6. Register router in `app/main.py`

Use template: `.claude/templates/api-endpoint.py.tmpl`
