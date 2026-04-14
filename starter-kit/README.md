# Citadel SaaS Factory — Starter Kit

A **deterministic, compile-only** SaaS starter kit designed for clone-and-run use across projects. This is a **minimal standalone scaffold** kept inside the main Citadel SaaS Factory framework as an alternative entry point.

> **Relationship to the parent repo:** The top-level repository is the full Citadel SaaS Factory v3.0 framework (265 agents, 3 LLM engines, Obsidian vault, Karpathy LLM Wiki brain memory, Guardrails, Graphify, Ruflo). This `starter-kit/` subdirectory is a **simpler, single-purpose scaffold** intended for people who want a clone-and-run Next.js + FastAPI + Postgres + Prometheus + Grafana stack without the full agent framework on top. Pick whichever fits your use case.

## What this includes

- Next.js UI template
- FastAPI backend
- PostgreSQL
- Prometheus and Grafana
- Docker Compose orchestration
- GitHub Actions CI
- Claude and Goose project configuration

## Quick start

```bash
cd starter-kit
cp .env.example .env
make up
```

Then open:

- UI: http://localhost:3000
- API: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## Stop

```bash
make down
```

## Reset

```bash
make reset
```

## How to use standalone

If you want *just* this starter kit without the parent framework, copy the `starter-kit/` directory to a new repository:

```bash
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory
cp -r citadel-saas-factory/starter-kit my-new-project
cd my-new-project
cp .env.example .env
make up
```

## Notes

- This kit is intentionally deterministic.
- UI generation is represented as reusable templates, not live runtime generation.
- Auth and deployment are safe placeholders ready to extend per project.
- For server-side calls inside the UI container, use `INTERNAL_API_BASE_URL=http://api:8000`.
- For browser calls from the host machine, use `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`.
- Run `docker compose config` before first launch if you want a quick config sanity check.
