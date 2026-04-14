# Citadel SaaS Factory — Master Intelligence File

> Universal Full-Stack SaaS Production Framework with 265 Autonomous Business Agents
> Version 3.0 | citadelcloudmanagement.com

## Overview

Citadel SaaS Factory is an infrastructure-agnostic SaaS framework. It runs on any Linux server with SSH and Docker. No cloud vendor lock-in. No proprietary APIs. Supports any VPS, bare metal, on-prem, edge, or home lab. Total software cost: $0/month.

## Architecture

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.12) |
| Frontend | Next.js 14 (TypeScript) |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Auth | Keycloak 24 (OAuth2, RBAC, MFA) |
| Storage | MinIO (S3-compatible) |
| Messaging | RabbitMQ |
| Orchestration | K3s + ArgoCD (GitOps) |
| Reverse Proxy | Traefik |
| Service Mesh | Linkerd (mTLS) |
| Secrets | HashiCorp Vault |

## Agent System

265 specialized agents across 15 domains. Full registry: `agents/_registry.yaml`

| Domain | Count | Examples |
|--------|-------|---------|
| Executive & Strategy | 12 | CEO Strategist, CTO Technology, OKR Tracker |
| Marketing & Growth | 22 | SEO, Content, Social, Email, PPC, PR |
| Sales & Revenue | 18 | Lead Qualifier, Proposals, CRM, Forecast |
| Customer Success | 15 | Onboarding, Tickets, Churn Predictor, NPS |
| Product & UI/UX | 20 | UI Designer, Wireframes, Design System, A11y |
| Engineering | 25 | API, Models, Auth, Cache, Search, WebSocket |
| Frontend | 18 | Components, Pages, Forms, Charts, State, PWA |
| DevOps | 28 | CI/CD, GitOps, K8s, Helm, Terraform, Canary |
| Security | 22 | SAST, DAST, Secrets, Falco, Kyverno, Pentest |
| Data & Analytics | 18 | Schema, ETL, Dashboards, Forecasting, Vector |
| QA & Testing | 22 | Unit, E2E, Load, Chaos, Mutation, Visual |
| HR & People | 12 | Jobs, Interviews, Onboarding, Performance |
| Finance & Billing | 15 | Stripe, Subscriptions, Tax, Revenue, Runway |
| Legal & Governance | 8 | ToS, DPA, GDPR, SOC2, SLA |
| Content & Comms | 10 | Tech Writing, Docs, Changelogs, Case Studies |

## Tool Integrations

- **Ruflo** — Multi-agent swarm orchestration (314 MCP tools, mesh topology)
- **Graphify** — Codebase knowledge graph (Tree-sitter AST, 20 languages)
- **GitHub Actions** — CI/CD with security gates (SAST, SCA, secret scan, container scan)

## Free Toolchain

ArgoCD, K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Falco, Kyverno, Semgrep, Trivy, ZAP, Flagsmith, Grafana OnCall, Velero, MinIO, Ansible.

## Commands

| Command | Purpose |
|---------|---------|
| `/deploy` | Deploy to target environment |
| `/rollback` | Emergency rollback |
| `/scaffold` | Generate code from templates |
| `/audit` | Run security and quality audit |
| `/status` | Check system and agent status |

## Conventions

- **Immutability**: Always create new objects, never mutate
- **Small files**: 200-400 lines typical, 800 max
- **TDD**: Write tests first, 80% minimum coverage
- **Conventional commits**: feat, fix, refactor, docs, test, chore, perf, ci
- **Error handling**: Handle errors at every level, never swallow silently

## Security Rules

- No hardcoded secrets — use environment variables or Vault
- Validate all user input at system boundaries
- Parameterized queries only — no SQL string concatenation
- Rate limiting on all API endpoints
- CORS, CSRF, XSS protection on all routes
- Container image scanning before deployment
- Secret scanning in pre-commit hooks
