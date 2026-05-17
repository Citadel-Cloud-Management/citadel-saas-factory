# Project Context

## Identity
- **Name**: Citadel SaaS Factory
- **Version**: 3.1
- **Type**: Universal full-stack SaaS production framework
- **Org**: Citadel Cloud Management
- **Repo**: github.com/Citadel-Cloud-Management/citadel-saas-factory

## Current State
- Phase: Active development, agentic infrastructure complete
- 541 tracked files, 265 agents (15 domains), 24 skills, 37 commands
- 21 rules, 20 templates, 11 hooks, 8 MCP configs, 43 MCP registry entries
- 10+ IDE/agent platform configs, 8 GitHub Actions workflows
- CLAUDE.md: 112 lines with @imports (under 200-line recommended limit)

## Stack
- Backend: FastAPI (Python 3.12, SQLAlchemy, Alembic)
- Frontend: Next.js 14 (TypeScript, Zustand, TanStack Query)
- Database: PostgreSQL 16 (RLS, pgvector)
- Cache: Redis 7 | Auth: Keycloak 24 | Storage: MinIO
- Messaging: RabbitMQ | Orchestration: K3s + ArgoCD
- Proxy: Traefik | Mesh: Linkerd | Secrets: Vault
- Monitoring: Prometheus + Grafana + Loki

## Architecture Principles
- Infrastructure-agnostic: any Linux server with SSH + Docker
- Multi-model routing: 12 providers, 8 tiers (models/routing.yaml)
- Zero software cost: entire toolchain open source
- Harness > Model: 98.4% infrastructure, 1.6% AI decision logic
- Deny-first permissions, graduated trust
