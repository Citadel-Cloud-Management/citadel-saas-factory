# ADR-001: FastAPI as Backend Framework

## Status

Accepted

## Context

Citadel SaaS Factory requires a Python backend framework that supports:

- High-performance async request handling for 265 concurrent agents
- Automatic API documentation for developer productivity
- Strong input validation and serialization
- Native dependency injection
- Production-grade performance comparable to Node.js and Go frameworks

The primary candidates evaluated were FastAPI, Django REST Framework, and Flask.

## Decision

We chose **FastAPI** as the backend framework.

### Key Reasons

1. **Async-first architecture**: FastAPI is built on Starlette and supports native `async`/`await`, enabling high concurrency for agent orchestration and I/O-bound operations without thread pool overhead.

2. **Pydantic integration**: Request/response validation is handled by Pydantic models, providing runtime type checking, automatic serialization, and clear error messages. This aligns with our input validation requirements at system boundaries.

3. **Automatic OpenAPI generation**: FastAPI auto-generates OpenAPI 3.1 specs from type annotations and Pydantic models. Swagger UI and ReDoc are available out of the box at `/docs` and `/redoc`, eliminating manual API documentation maintenance.

4. **Performance**: FastAPI is one of the fastest Python frameworks, benchmarking close to Node.js Express and Go Gin for JSON serialization. This matters for high-throughput agent communication.

5. **Dependency injection**: FastAPI's built-in `Depends()` system enables clean architecture by wiring repositories and services without a separate DI container.

6. **Python 3.12 compatibility**: Full support for modern Python features including type hints, `match` statements, and performance improvements in 3.12.

## Consequences

### Positive

- API documentation is always in sync with the code (auto-generated from types)
- Input validation happens at the framework level, reducing boilerplate
- Async support enables efficient handling of concurrent agent operations
- Strong typing catches errors at development time
- Large ecosystem of compatible async libraries (SQLAlchemy async, httpx, aio-pika)

### Negative

- Smaller community than Django; fewer pre-built solutions for common patterns (admin panel, ORM migrations)
- Async programming introduces complexity (async context managers, avoiding blocking calls)
- Alembic for database migrations is less integrated than Django's built-in migration system
- Team members may need ramp-up time on async Python patterns

### Mitigations

- Use Alembic with SQLAlchemy for database migrations (mature, well-documented)
- Establish async coding guidelines and patterns in the codebase
- Use `asyncio.to_thread()` for unavoidable blocking operations
