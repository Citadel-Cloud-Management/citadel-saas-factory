Generate six execution-ready planning documents for a new SaaS project using the Six-Docs framework.

Read the full prompt template from `docs/templates/six-docs-prompt.md` and follow it exactly.

If the user provided project details as arguments: $ARGUMENTS

Then fill in the PROJECT INPUT block with those details and generate all six documents:
1. PRD (Product Requirements Document)
2. TRD (Technical Requirements Document)
3. App Flow
4. UI/UX Design Brief
5. Backend Schema
6. Implementation Plan

If no project details were provided, ask the user to fill in the PROJECT INPUT fields:
- App name
- One-line description
- Primary user (2 to 3 sentences)
- Core problem being solved
- Stack preferences or hard constraints
- Budget envelope (monthly run-rate ceiling)
- Timeline to MVP
- Compliance posture (HIPAA, SOC 2, GDPR, PCI, none)
- Distribution channel (web, iOS, Android, all)
- Anything else load-bearing

Use the Citadel SaaS Factory stack as the default when no stack preference is given:
- Backend: FastAPI (Python 3.12)
- Frontend: Next.js 14 (TypeScript)
- Database: PostgreSQL 16
- Cache: Redis 7
- Auth: Keycloak 24
- Orchestration: K3s, ArgoCD
- Monitoring: Prometheus, Grafana, Loki

Save each document to `docs/planning/` as separate files:
- `docs/planning/01-prd.md`
- `docs/planning/02-trd.md`
- `docs/planning/03-app-flow.md`
- `docs/planning/04-ui-ux-design-brief.md`
- `docs/planning/05-backend-schema.md`
- `docs/planning/06-implementation-plan.md`
