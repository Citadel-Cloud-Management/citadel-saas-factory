---
description: Project walkthrough for new developers
---

# Welcome to Citadel SaaS Factory

Walk through the project structure and explain:

1. **Architecture** — Clean layers: FastAPI backend, Next.js frontend, PostgreSQL, Redis
2. **Key Files** — CLAUDE.md, docker-compose.yml, Makefile, _registry.yaml
3. **Setup** — How to run `./scripts/bootstrap.sh` and get started
4. **265 Agents** — 15 domains, autonomous execution, CYCLE_INTERVAL=0
5. **Development Workflow** — TDD, code review, conventional commits
6. **Deployment** — GitOps via ArgoCD, staging then production
7. **Security** — Vault, Kyverno, Falco, scanning pipeline
