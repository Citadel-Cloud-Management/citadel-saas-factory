---
name: ms-engineering-standards
description: Required engineering standards — backend (TypeScript/Python/Go, clean architecture), frontend (Next.js/React/Tailwind), infrastructure (K8s/Terraform/GitOps), database (indexing, migrations, pooling, replication).
type: standard
priority: 10
---

# Required Engineering Standards

## Backend Standards

### Preferred Languages (in order)
1. **TypeScript** — Node.js services, serverless, full-stack
2. **Python** — ML/AI, data processing, scripting, FastAPI
3. **Go** — High-performance services, infrastructure tools, CLIs

### Architecture Requirements
- **Clean architecture** — domain > use cases > interfaces > infrastructure
- **Modular monolith or microservices** — justify the choice with scale/team requirements
- **OpenAPI specs** — every endpoint documented, generated from code
- **Async processing** — queues for long-running tasks (Bull, Celery, NATS)
- **Events** — event-driven for cross-service communication
- **Idempotency** — all mutation endpoints are idempotent (idempotency keys)
- **Retry handling** — exponential backoff with jitter, configurable limits

### Code Quality
```
[ ] Functions < 50 lines
[ ] Files < 400 lines (800 absolute max)
[ ] No deep nesting (max 4 levels)
[ ] Immutable data patterns
[ ] Comprehensive error handling
[ ] Input validation at boundaries
[ ] No hardcoded configuration
```

## Frontend Standards

### Preferred Stack
- **Next.js 14** — App Router, RSC, streaming
- **React 18+** — functional components, hooks
- **TypeScript** — strict mode, no `any`
- **Tailwind CSS** — utility-first, design system tokens

### Requirements
- **Responsive design** — mobile-first breakpoints
- **Accessibility** — WCAG 2.1 AA, semantic HTML, ARIA
- **Performance** — LCP < 2.5s, FID < 100ms, CLS < 0.1
- **Error boundaries** — graceful error handling at component level
- **State management** — Zustand for global, React Query for server state
- **SSR/ISR** — where SEO or initial load performance matters
- **Code splitting** — dynamic imports for heavy components

## Infrastructure Standards

### Preferred Stack
- **Kubernetes** (K3s/EKS/GKE) — orchestration
- **Docker** — containerization (multi-stage builds)
- **Terraform** — infrastructure as code
- **GitOps** — ArgoCD/FluxCD for deployments
- **Helm** — package management for K8s

### Deployment Patterns
- **Blue/green** — zero-downtime with instant rollback
- **Canary** — gradual rollout with automated rollback
- **Autoscaling** — HPA based on CPU/memory/custom metrics
- **HA architecture** — multi-AZ minimum, multi-region for critical
- **DR strategy** — RTO/RPO defined, tested quarterly

## Database Standards

### Requirements
- **Indexing strategy** — B-tree for equality, GIN for JSONB/arrays, partial indexes
- **Migration safety** — backward-compatible, zero-downtime migrations
- **Backup policies** — automated daily, point-in-time recovery
- **Replication** — read replicas for read-heavy workloads
- **Query optimization** — no N+1, EXPLAIN ANALYZE for complex queries
- **Connection pooling** — PgBouncer/connection limits configured
- **Schema versioning** — all changes via migration files, never manual DDL

### Performance Targets
| Metric | Target |
|--------|--------|
| p50 query latency | < 5ms |
| p95 query latency | < 50ms |
| p99 query latency | < 200ms |
| Connection pool utilization | < 80% |
| Index hit ratio | > 99% |
