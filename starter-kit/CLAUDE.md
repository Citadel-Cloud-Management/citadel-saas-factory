# Citadel SaaS Factory — Starter Kit

> This is the standalone starter kit. For the full factory, see the root [CLAUDE.md](../CLAUDE.md).

## Purpose

Deterministic, compile-only SaaS starter. Cloneable, understandable, and runnable with minimal changes.

## Stack

- Frontend: Next.js (TypeScript) — `ui/`
- Backend: FastAPI (Python 3.12) — `api/`
- Database: PostgreSQL — `database/`
- Monitoring: Prometheus + Grafana — `monitoring/`
- Infrastructure: Docker Compose — `docker-compose.yml`

## Commands

```bash
./setup.sh      # Create .env, check Docker
./start.sh      # Start all services
./stop.sh       # Stop all services
make up         # Alternative: Docker Compose up
```

## Rules

- Keep startup deterministic: clone -> env -> start
- Prefer reusable templates over generated novelty
- Maintain clear separation between ui, api, database, monitoring, infrastructure
- Make small, reviewable edits
- Document any new service in README and docker-compose
