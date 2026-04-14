# Citadel SaaS Factory Project Memory

## Purpose
This repository is a deterministic, compile-only SaaS factory starter kit.
It must remain cloneable, understandable, and runnable with minimal changes.

## Rules
- Do not invent new architecture at runtime.
- Prefer reusable templates over generated novelty.
- Keep startup deterministic: clone -> env -> start.
- Maintain clear separation between ui, api, database, monitoring, and infrastructure.
- Default stack: Next.js, FastAPI, Postgres, Prometheus, Grafana, Docker Compose.

## Working style
- Make small, reviewable edits.
- Keep security defaults sane.
- Preserve one-command startup.
- Document any new service in README and docker-compose.

## Commands
- `/ui` means update reusable UI templates, not dynamic design generation.
- `/artifacts` means create or modify deterministic repo files.
- `/scout` means inspect risks, misconfigurations, or portability issues.
