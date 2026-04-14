# Citadel SaaS Factory

**Universal Full-Stack SaaS Production Framework — 265 Autonomous Business Agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-blueviolet)](https://claude.ai/code) [![Agents](https://img.shields.io/badge/Agents-265-orange)](.claude/agents/_registry.yaml) [![Free Tools](https://img.shields.io/badge/Tools-$0/month-brightgreen)](#free-toolchain) [![Infrastructure](https://img.shields.io/badge/Infrastructure-Any-blue)](#infrastructure-agnostic)

**Clone. Configure. Deploy. Any infrastructure. Zero software cost.**

---

## Quick Start

```bash
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git
cd citadel-saas-factory
cp .env.example .env
./scripts/bootstrap.sh
./scripts/verify-install.sh
claude
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTS                                  │
│              Browser / Mobile / API Consumers                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                     REVERSE PROXY                               │
│                  Traefik (TLS, Routing)                          │
└──────────┬───────────────┬───────────────┬──────────────────────┘
           │               │               │
┌──────────▼───┐  ┌────────▼───┐  ┌────────▼──────────┐
│   FRONTEND   │  │  BACKEND   │  │    AUTH GATEWAY    │
│  Next.js 14  │  │  FastAPI   │  │   Keycloak 24      │
│  TypeScript  │  │ Python 3.12│  │ OAuth2/RBAC/MFA    │
└──────────────┘  └─────┬──────┘  └────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼───┐  ┌────────▼───┐  ┌───────▼────────┐
│ DATABASE  │  │   CACHE    │  │   MESSAGING    │
│ Postgres  │  │  Redis 7   │  │   RabbitMQ     │
│    16     │  │            │  │                │
└───────────┘  └────────────┘  └────────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│                    STORAGE & SECRETS                    │
│          MinIO (S3-compatible)  |  HashiCorp Vault      │
└───────────────────────────────────────────────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│                   ORCHESTRATION                        │
│     K3s + ArgoCD (GitOps) | Linkerd (mTLS mesh)       │
└───────────────────────────────────────────────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│                    OBSERVABILITY                       │
│       Prometheus | Grafana | Loki | Tempo | Falco     │
└───────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | FastAPI (Python 3.12) | REST/GraphQL API, business logic |
| Frontend | Next.js 14 (TypeScript) | SSR/SSG UI, React components |
| Database | PostgreSQL 16 | Primary data store, RLS, pgvector |
| Cache | Redis 7 | Session cache, rate limiting, pub/sub |
| Auth | Keycloak 24 | OAuth2, RBAC, MFA, SSO |
| Storage | MinIO | S3-compatible object storage |
| Messaging | RabbitMQ | Async messaging, event bus, DLQ |
| Orchestration | K3s + ArgoCD | Lightweight K8s, GitOps deployment |
| Reverse Proxy | Traefik | TLS termination, routing, middleware |
| Service Mesh | Linkerd | mTLS, traffic policies, observability |
| Secrets | HashiCorp Vault | Secret management, rotation, encryption |
| Monitoring | Prometheus + Grafana + Loki | Metrics, dashboards, log aggregation |

---

## Infrastructure Agnostic

Runs on any Linux server with SSH and Docker. No cloud vendor lock-in.

- Any VPS provider (Hetzner, DigitalOcean, Linode, Vultr)
- Bare metal servers
- On-premises infrastructure
- Edge deployments
- Home lab

---

## `.claude/` Directory Structure

```
.claude/
├── CLAUDE.md                          # Master intelligence file
├── settings.json                      # Claude Code configuration
├── memory/
│   ├── MEMORY.md                      # Auto-memory (persists across sessions)
│   ├── project_citadel_saas_factory.md
│   └── adrs/                          # Architecture Decision Records
├── agents/
│   ├── _registry.yaml                 # Master agent registry (265 agents)
│   ├── executive/                     # 12 executive & strategy agents
│   ├── marketing/                     # 22 marketing & growth agents
│   ├── sales/                         # 18 sales & revenue agents
│   ├── customer-success/              # 15 customer success agents
│   ├── design/                        # 20 product & UI/UX agents
│   ├── engineering/                   # 25 engineering agents
│   ├── frontend/                      # 18 frontend agents
│   ├── devops/                        # 28 DevOps agents
│   ├── security/                      # 22 security agents
│   ├── data/                          # 18 data & analytics agents
│   ├── qa/                            # 22 QA & testing agents
│   ├── hr/                            # 12 HR & people agents
│   ├── finance/                       # 15 finance & billing agents
│   ├── legal/                         # 8 legal & governance agents
│   └── content/                       # 10 content & comms agents
├── hooks/
│   ├── pre-commit.sh                  # Secret scanning, lint, format
│   ├── post-commit.sh                 # Coverage check, changelog update
│   ├── pre-push.sh                    # Security scan, test run
│   ├── pre-tool-use.sh                # Parameter validation
│   ├── post-tool-use.sh               # Auto-format, checks
│   ├── pre-deploy.sh                  # Image scan, smoke test
│   ├── post-deploy.sh                 # Health check, notification
│   ├── pre-rollback.sh                # State snapshot
│   ├── post-rollback.sh               # Verification, alerting
│   └── stop.sh                        # Final verification on session end
├── rules/
│   ├── accessibility.md               # WCAG 2.1 AA compliance
│   ├── api-design.md                  # RESTful conventions, OpenAPI
│   ├── architecture.md                # Clean architecture, DDD
│   ├── code-quality.md                # Immutability, small files
│   ├── database.md                    # Migrations, RLS, indexes
│   ├── dependencies.md                # Lock files, audits
│   ├── devops.md                      # GitOps, immutable infra
│   ├── documentation.md               # API docs, ADRs
│   ├── error-handling.md              # Structured errors, retry
│   ├── frontend.md                    # Components, a11y, perf
│   ├── git.md                         # Conventional commits
│   ├── monitoring.md                  # Structured logging, RED
│   ├── naming.md                      # snake_case, camelCase
│   ├── performance.md                 # Caching, lazy loading
│   ├── review.md                      # PR process, checklists
│   ├── secrets.md                     # Vault, rotation, scanning
│   ├── security.md                    # Input validation, XSS, CSRF
│   └── testing.md                     # TDD, 80% coverage
├── commands/
│   ├── deploy.md                      # Deploy to environment
│   ├── rollback.md                    # Emergency rollback
│   ├── scaffold.md                    # Code generation
│   ├── audit.md                       # Security & quality audit
│   ├── status.md                      # System & agent status
│   ├── migrate.md                     # Database migrations
│   ├── seed.md                        # Seed data
│   ├── test.md                        # Run test suites
│   ├── lint.md                        # Run linters
│   ├── format.md                      # Run formatters
│   ├── build.md                       # Build artifacts
│   ├── release.md                     # Create release
│   ├── backup.md                      # Database backup
│   ├── restore.md                     # Database restore
│   ├── monitor.md                     # View dashboards
│   ├── logs.md                        # View logs
│   ├── secrets.md                     # Manage secrets
│   ├── certs.md                       # Manage TLS certs
│   ├── scale.md                       # Scale services
│   └── perf.md                        # Performance profiling
├── templates/
│   ├── api-endpoint.py                # FastAPI endpoint template
│   ├── model.py                       # SQLAlchemy model template
│   ├── schema.py                      # Pydantic schema template
│   ├── service.py                     # Service layer template
│   ├── repository.py                  # Repository template
│   ├── migration.py                   # Alembic migration template
│   ├── test-unit.py                   # Unit test template
│   ├── test-integration.py            # Integration test template
│   ├── test-e2e.py                    # E2E test template
│   ├── component.tsx                  # React component template
│   ├── page.tsx                       # Next.js page template
│   ├── form.tsx                       # Form component template
│   ├── table.tsx                      # Data table template
│   ├── hook.ts                        # Custom hook template
│   ├── store.ts                       # Zustand store template
│   ├── dockerfile                     # Multi-stage Dockerfile
│   ├── helm-chart/                    # Helm chart template
│   ├── github-action.yml              # CI/CD workflow template
│   ├── kyverno-policy.yaml            # Admission policy template
│   └── grafana-dashboard.json         # Dashboard template
├── skills/
│   ├── api-patterns.md                # API design patterns
│   ├── auth-patterns.md               # Authentication flows
│   ├── cache-patterns.md              # Caching strategies
│   ├── db-patterns.md                 # Database patterns
│   ├── event-patterns.md              # Event-driven architecture
│   ├── frontend-patterns.md           # React/Next.js patterns
│   ├── k8s-patterns.md               # Kubernetes patterns
│   ├── security-patterns.md           # Security patterns
│   ├── testing-patterns.md            # Testing strategies
│   ├── monitoring-patterns.md         # Observability patterns
│   ├── gitops-patterns.md             # GitOps workflows
│   ├── multi-tenant-patterns.md       # Multi-tenancy patterns
│   ├── migration-patterns.md          # Zero-downtime migrations
│   ├── performance-patterns.md        # Performance optimization
│   └── deployment-patterns.md         # Deployment strategies
└── mcp/
    ├── github.json                    # GitHub MCP server config
    ├── filesystem.json                # Filesystem MCP server config
    ├── postgres.json                  # PostgreSQL MCP server config
    ├── docker.json                    # Docker MCP server config
    ├── kubernetes.json                # Kubernetes MCP server config
    ├── ruflo.json                     # Ruflo swarm MCP server config
    ├── graphify.json                  # Graphify knowledge graph config
    └── context7.json                  # Context7 docs MCP server config
```

---

## All 265 Agents — 15 Domains

### Domain 1: Executive & Strategy (12 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `exec-ceo-strategist` | CEO Strategist | Business strategy, OKR generation, competitive analysis, board decks |
| 2 | `exec-coo-operations` | COO Operations | Process optimization, cross-department coordination, resource allocation |
| 3 | `exec-cfo-finance` | CFO Finance | Financial modeling, revenue forecasting, burn rate, unit economics |
| 4 | `exec-cto-technology` | CTO Technology | Tech stack decisions, architecture reviews, build vs buy, tech debt |
| 5 | `exec-cmo-marketing` | CMO Marketing | Marketing strategy, brand positioning, channel mix, growth planning |
| 6 | `exec-cpo-product` | CPO Product | Product vision, roadmap, feature prioritization (RICE/ICE), market fit |
| 7 | `exec-vp-engineering` | VP Engineering | Engineering velocity, team structure, hiring plans, incident escalation |
| 8 | `exec-vp-sales` | VP Sales | Sales strategy, pipeline analysis, territory planning, quota setting |
| 9 | `exec-okr-tracker` | OKR Tracker | Company/team OKR tracking, progress reports, at-risk identification |
| 10 | `exec-board-reporter` | Board Reporter | Board reports, investor updates, KPI dashboards, milestone tracking |
| 11 | `exec-competitive-intel` | Competitive Intel | Competitor monitoring, market trends, competitive battle cards |
| 12 | `exec-decision-logger` | Decision Logger | Strategic decision recording with context, rationale, and outcomes |

### Domain 2: Marketing & Growth (22 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `mktg-seo-strategist` | SEO Strategist | Keyword research, on-page optimization, technical SEO, content gaps |
| 2 | `mktg-content-writer` | Content Writer | Blog posts, landing pages, emails, case studies, whitepapers |
| 3 | `mktg-social-media` | Social Media | Post scheduling, captions, hashtags, engagement analysis |
| 4 | `mktg-email-marketer` | Email Marketer | Campaigns, subject lines, segmentation, A/B testing, flows |
| 5 | `mktg-ppc-manager` | PPC Manager | Ad copy, bid strategy, audience targeting, ROAS optimization |
| 6 | `mktg-analytics` | Marketing Analytics | UTM tracking, attribution, funnel analysis, conversion optimization |
| 7 | `mktg-landing-page` | Landing Page | High-conversion page design and copy, CTA optimization |
| 8 | `mktg-brand-voice` | Brand Voice | Brand consistency, tone guidelines, style guide enforcement |
| 9 | `mktg-pr-outreach` | PR Outreach | Press releases, journalist pitching, media lists, coverage tracking |
| 10 | `mktg-influencer` | Influencer Agent | Influencer ID, outreach scripts, partnership terms, ROI tracking |
| 11 | `mktg-video-scripting` | Video Scriptwriter | YouTube scripts, social hooks, demo scripts, webinar outlines |
| 12 | `mktg-podcast` | Podcast Producer | Episode outlines, show notes, guest research, transcripts |
| 13 | `mktg-community` | Community Manager | Community engagement, UGC curation, feedback collection |
| 14 | `mktg-growth-hacker` | Growth Hacker | Viral loops, referral programs, PLG mechanics, activation experiments |
| 15 | `mktg-ab-tester` | A/B Test Designer | Hypothesis generation, stat significance, result analysis |
| 16 | `mktg-competitor` | Competitor Monitor | Competitor marketing moves, pricing changes, feature launches |
| 17 | `mktg-newsletter` | Newsletter Agent | Content curation, subject lines, send time optimization |
| 18 | `mktg-webinar` | Webinar Planner | Planning, registration copy, follow-up sequences, engagement |
| 19 | `mktg-affiliate` | Affiliate Manager | Program setup, commissions, partner recruitment, payouts |
| 20 | `mktg-product-launch` | Product Launch | Launch playbook, announcement copy, drip campaigns, press |
| 21 | `mktg-persona` | Persona Builder | ICP definition, buyer personas, jobs-to-be-done analysis |
| 22 | `mktg-retention` | Retention Agent | Churn signals, re-engagement campaigns, NPS follow-up |

### Domain 3: Sales & Revenue (18 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `sales-lead-qualifier` | Lead Qualifier | Lead scoring, data enrichment, ICP matching, routing |
| 2 | `sales-outbound-writer` | Outbound Writer | Cold emails, LinkedIn messages, follow-ups, objection handling |
| 3 | `sales-proposal-gen` | Proposal Generator | Custom proposals, SOWs, pricing tables, ROI calculations |
| 4 | `sales-crm-updater` | CRM Updater | Deal stage updates, activity logging, pipeline hygiene |
| 5 | `sales-demo-prepper` | Demo Prepper | Pre-demo research, custom scripts, competitive positioning |
| 6 | `sales-contract-drafter` | Contract Drafter | MSA and order forms, redline tracking, approval routing |
| 7 | `sales-forecast` | Forecast Analyst | Pipeline forecasting, deal velocity, revenue prediction |
| 8 | `sales-win-loss` | Win/Loss Analyst | Post-deal analysis, pattern identification, CI extraction |
| 9 | `sales-pricing` | Pricing Optimizer | Pricing models, discount impact, WTP estimation, tier optimization |
| 10 | `sales-territory` | Territory Planner | Territory mapping, account distribution, quota allocation |
| 11 | `sales-upsell` | Upsell Detector | Expansion opportunities, usage triggers, health signals |
| 12 | `sales-scheduler` | Meeting Scheduler | Calendar coordination, timezone handling, no-show follow-up |
| 13 | `sales-objection` | Objection Handler | Objection responses, battle cards, value proposition framing |
| 14 | `sales-referral` | Referral Agent | Referral program, ask timing, reward fulfillment, tracking |
| 15 | `sales-partner` | Partner Manager | Deal registration, co-selling, partner enablement content |
| 16 | `sales-call-analyzer` | Call Analyzer | Transcript analysis, talk ratio, next-step extraction |
| 17 | `sales-pipeline-cleaner` | Pipeline Cleaner | Stale deal ID, missing data alerts, stage-appropriate actions |
| 18 | `sales-commission` | Commission Calculator | Commission calculation, plan modeling, quota attainment |

### Domain 4: Customer Success (15 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `cs-onboarding` | Onboarding Agent | Welcome sequences, setup guides, milestone tracking, TTV |
| 2 | `cs-ticket-router` | Ticket Router | Auto-categorize, prioritize, route support tickets |
| 3 | `cs-response-drafter` | Response Drafter | Draft support responses from knowledge base, tone consistency |
| 4 | `cs-escalation` | Escalation Agent | Escalation signals, senior routing, escalation summaries |
| 5 | `cs-churn-predictor` | Churn Predictor | Usage analysis, engagement scoring, risk flagging, save offers |
| 6 | `cs-health-scorer` | Health Scorer | Account health scoring (usage, tickets, NPS, adoption) |
| 7 | `cs-nps` | NPS Collector | Survey distribution, response collection, follow-up automation |
| 8 | `cs-knowledge` | Knowledge Builder | FAQ generation, help articles, KB maintenance, search |
| 9 | `cs-chatbot` | Chatbot Trainer | Support chatbot training, intent refinement, accuracy |
| 10 | `cs-feedback` | Feedback Analyzer | Categorize feedback, trends, route feature requests |
| 11 | `cs-renewal` | Renewal Manager | Renewal tracking, pricing prep, contract generation |
| 12 | `cs-qbr` | QBR Generator | QBR deck generation with usage data and ROI metrics |
| 13 | `cs-adoption` | Adoption Tracker | Feature adoption, usage depth, enablement gaps |
| 14 | `cs-sla` | SLA Monitor | SLA compliance, breach alerts, response time monitoring |
| 15 | `cs-voc` | Voice of Customer | Aggregate feedback across channels into actionable insights |

### Domain 5: Product & UI/UX Design (20 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `design-ui` | UI Designer | Component design, layout, spacing/typography, visual hierarchy |
| 2 | `design-ux-research` | UX Researcher | Interview scripts, surveys, usability tests, persona refinement |
| 3 | `design-wireframe` | Wireframer | Lo-fi wireframes, user flows, information architecture |
| 4 | `design-prototype` | Prototype Builder | Interactive prototype specs, click-through flows |
| 5 | `design-system` | Design System | Token management, component library, pattern docs |
| 6 | `design-a11y` | Accessibility | WCAG 2.1 AA audit, contrast, screen reader, ARIA |
| 7 | `design-responsive` | Responsive Design | Breakpoints, mobile-first, touch targets, viewport |
| 8 | `design-color` | Color Palette | Color theory, palette generation, dark/light theming |
| 9 | `design-typography` | Typography | Font pairing, type scale, readability, web font perf |
| 10 | `design-icon` | Icon System | Icon library, SVG optimization, consistent metaphors |
| 11 | `design-animation` | Animation | Micro-interactions, transitions, loading, skeletons |
| 12 | `design-illustration` | Illustration | Brand illustration style, spot illustrations, empty states |
| 13 | `design-data-viz` | Data Visualization | Chart selection, dashboard layout, data storytelling |
| 14 | `design-user-flow` | User Flow | Task flow mapping, happy path, error states, edge cases |
| 15 | `design-heuristic` | Heuristic Eval | Nielsen heuristics, usability scoring, recommendations |
| 16 | `design-onboarding` | Onboarding UX | First-run experience, progressive disclosure, tooltips |
| 17 | `design-form` | Form UX | Form optimization, validation, multi-step, autofill |
| 18 | `design-search` | Search UX | Search interface, filters, autocomplete, results display |
| 19 | `design-notification` | Notification UX | Notification design, frequency, channels, preferences |
| 20 | `design-mobile` | Mobile UX | Native patterns, gestures, thumb-zone, offline states |

### Domain 6: Engineering (25 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `eng-api-designer` | API Designer | REST/GraphQL design, OpenAPI spec, versioning |
| 2 | `eng-model-builder` | Model Builder | ORM models, relationships, constraints, indexes |
| 3 | `eng-schema-builder` | Schema Builder | Pydantic schemas, validation, serialization |
| 4 | `eng-service-builder` | Service Builder | Business logic, service layer patterns, DI |
| 5 | `eng-repo-builder` | Repository Builder | Data access, query builders, pagination, filtering |
| 6 | `eng-migration-gen` | Migration Generator | Schema migrations, safe rollback, zero-downtime |
| 7 | `eng-middleware` | Middleware Builder | Auth, rate limit, CORS, logging, metrics, headers |
| 8 | `eng-event-handler` | Event Handler | Event-driven, message bus, async, saga patterns |
| 9 | `eng-worker-builder` | Worker Builder | Background jobs, retry logic, DLQ, scheduling |
| 10 | `eng-auth-builder` | Auth Builder | JWT, OAuth2, RBAC, permission guards |
| 11 | `eng-cache-builder` | Cache Builder | Cache strategies, invalidation, TTL management |
| 12 | `eng-search-builder` | Search Builder | Full-text, vector (pgvector), hybrid ranking |
| 13 | `eng-webhook` | Webhook Builder | Dispatch, retry, signature verification, logging |
| 14 | `eng-email` | Email Builder | Transactional email, templates, queue, tracking |
| 15 | `eng-file-handler` | File Handler | Upload validation, scanning, storage, signed URLs |
| 16 | `eng-pagination` | Pagination Agent | Cursor/offset pagination, ordering, optimization |
| 17 | `eng-rate-limiter` | Rate Limiter | Per-endpoint/user limits, sliding window, token bucket |
| 18 | `eng-health` | Health Builder | Liveness, readiness, startup probes, dep checks |
| 19 | `eng-websocket` | WebSocket Builder | Real-time, rooms, broadcast, heartbeat, reconnect |
| 20 | `eng-graphql` | GraphQL Builder | Schema, resolvers, dataloaders, subscriptions |
| 21 | `eng-multi-tenant` | Multi-Tenant | RLS, tenant middleware, data isolation |
| 22 | `eng-error-handler` | Error Handler | Structured errors, exception hierarchy, codes |
| 23 | `eng-logging` | Logging Agent | JSON logging, correlation IDs, PII redaction |
| 24 | `eng-config` | Config Manager | Env config, feature flags, dynamic config |
| 25 | `eng-code-reviewer` | Code Reviewer | PR review, patterns, complexity, security checks |

### Domain 7: Frontend (18 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `fe-component` | Component Builder | React scaffolding, props typing, composition |
| 2 | `fe-page` | Page Builder | Next.js pages, SSR/SSG, metadata, routing |
| 3 | `fe-layout` | Layout Builder | Navigation, sidebar, responsive shell |
| 4 | `fe-form` | Form Builder | RHF and Zod, multi-step, validation, errors |
| 5 | `fe-table` | Table Builder | Data tables, sorting, filtering, pagination, export |
| 6 | `fe-chart` | Chart Builder | Recharts/D3 visualizations, real-time updates |
| 7 | `fe-auth` | Auth Flow | Login, signup, reset, MFA, session management |
| 8 | `fe-state` | State Manager | Zustand stores, selectors, middleware |
| 9 | `fe-api-client` | API Client | TanStack Query hooks, errors, loading, optimistic |
| 10 | `fe-a11y` | A11y Auditor | axe-core, ARIA, keyboard nav, focus management |
| 11 | `fe-responsive` | Responsive | Mobile-first, breakpoints, touch, viewports |
| 12 | `fe-i18n` | i18n Agent | Translations, locale, RTL, date/number format |
| 13 | `fe-seo` | SEO Agent | Meta tags, structured data, sitemap, Open Graph |
| 14 | `fe-performance` | Performance | Bundle analysis, code splitting, lazy load, CWV |
| 15 | `fe-testing` | Frontend Testing | Vitest, Playwright E2E, visual regression |
| 16 | `fe-animation` | Animation Builder | CSS transitions, Framer Motion, scroll animations |
| 17 | `fe-error-boundary` | Error Boundary | Error boundaries, fallbacks, reporting, recovery |
| 18 | `fe-pwa` | PWA Builder | Service worker, offline, push notifications |

### Domain 8: DevOps (28 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `devops-ci` | CI Orchestrator | GitHub Actions pipeline, caching, stages |
| 2 | `devops-cd` | CD Deployer | Deployment execution, promotion, health |
| 3 | `devops-gitops` | GitOps Sync | ArgoCD management, sync policy, drift |
| 4 | `devops-image-build` | Image Builder | Multi-stage Docker, layer optimization, hardening |
| 5 | `devops-image-scan` | Image Scanner | Trivy/Grype CVE scanning, base image updates |
| 6 | `devops-image-sign` | Image Signer | Cosign signing, SBOM generation (Syft) |
| 7 | `devops-helm` | Helm Manager | Chart creation, values, release lifecycle |
| 8 | `devops-terraform` | Terraform Ops | Plan, apply, state, modules, drift detection |
| 9 | `devops-ansible` | Ansible Runner | Playbooks, roles, inventory management |
| 10 | `devops-k8s` | K8s Manager | Deployments, services, configmaps, secrets |
| 11 | `devops-scaler` | K8s Scaler | HPA tuning, VPA, cluster autoscaler |
| 12 | `devops-debugger` | K8s Debugger | Pod diagnostics, log analysis, crash analysis |
| 13 | `devops-canary` | Canary Manager | Progressive rollout 10/30/60/100 percent |
| 14 | `devops-rollback` | Rollback Agent | Emergency rollback, version pinning, state restore |
| 15 | `devops-release` | Release Manager | Semantic versioning, changelog, tags |
| 16 | `devops-cert` | Cert Manager | TLS lifecycle, auto-renewal, ACME |
| 17 | `devops-dns` | DNS Manager | DNS records, health checks, failover |
| 18 | `devops-backup` | Backup Agent | DB backup, object storage backup, retention |
| 19 | `devops-restore` | Restore Agent | Backup validation, restore, DR testing |
| 20 | `devops-monitoring` | Monitoring Setup | Prometheus, Grafana, Loki, Tempo deployment |
| 21 | `devops-alerts` | Alert Builder | Alert rules, routing, escalation, silencing |
| 22 | `devops-logs` | Log Manager | Promtail/Loki pipeline, retention, format |
| 23 | `devops-mesh` | Service Mesh | Linkerd deployment, mTLS, traffic policies |
| 24 | `devops-ingress` | Ingress Manager | Traefik/NGINX, routing, rate limits, headers |
| 25 | `devops-storage` | Storage Manager | PV/PVC, MinIO, backup storage |
| 26 | `devops-queue` | Queue Manager | RabbitMQ/NATS, depth monitoring, DLQ |
| 27 | `devops-cost` | Cost Analyzer | Utilization analysis, rightsizing recommendations |
| 28 | `devops-capacity` | Capacity Planner | Growth forecasting, resource planning |

### Domain 9: Security (22 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `sec-sast` | SAST Scanner | Semgrep static analysis, vulnerability finding |
| 2 | `sec-sca` | SCA Scanner | Trivy dependency scanning, CVE, license |
| 3 | `sec-dast` | DAST Scanner | OWASP ZAP dynamic testing, API fuzzing |
| 4 | `sec-secret` | Secret Scanner | TruffleHog detection, pre-commit, prevention |
| 5 | `sec-container` | Container Scanner | Image CVE scanning, base image audit |
| 6 | `sec-iac` | IaC Scanner | Checkov Terraform/K8s scanning |
| 7 | `sec-runtime` | Runtime Monitor | Falco anomaly detection, container escapes |
| 8 | `sec-policy` | Policy Enforcer | Kyverno admission, OPA/Rego rules |
| 9 | `sec-incident` | Incident Responder | IR automation, evidence, containment |
| 10 | `sec-vuln` | Vuln Prioritizer | CVSS, exploitability, risk prioritization |
| 11 | `sec-patch` | Patch Manager | Security patching, dep updates, rollout |
| 12 | `sec-access` | Access Reviewer | IAM audit, permission review, least privilege |
| 13 | `sec-rbac` | RBAC Manager | Role definitions, permissions, grants |
| 14 | `sec-encryption` | Encryption Agent | At-rest/transit encryption, key rotation |
| 15 | `sec-audit` | Audit Logger | Immutable audit log, compliance reporting |
| 16 | `sec-compliance` | Compliance Checker | SOC2, HIPAA, GDPR, PCI, ISO 27001 |
| 17 | `sec-pentest` | Pentest Runner | Automated pentesting, Nuclei, validation |
| 18 | `sec-threat` | Threat Hunter | Proactive detection, IOC, SIGMA rules |
| 19 | `sec-network` | Network Segmenter | NetworkPolicies, micro-segmentation, zero-trust |
| 20 | `sec-waf` | WAF Manager | WAF rules, DDoS protection, bot detection |
| 21 | `sec-pii` | PII Detector | PII in logs/data, classification, masking |
| 22 | `sec-supply-chain` | Supply Chain | SBOM analysis, provenance, Cosign verification |

### Domain 10: Data & Analytics (18 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `data-schema` | Schema Designer | DB schema, normalization, relationships |
| 2 | `data-migration` | Migration Builder | Safe DDL, zero-downtime, rollback |
| 3 | `data-index` | Index Optimizer | Query plans, index recs, bloat detection |
| 4 | `data-query` | Query Optimizer | Slow queries, N+1, rewriting |
| 5 | `data-rls` | RLS Manager | Row-level security, tenant isolation |
| 6 | `data-backup` | Backup Validator | Integrity checks, restore testing |
| 7 | `data-etl` | ETL Builder | Data pipelines, transformations |
| 8 | `data-analytics` | Analytics Builder | Business metrics, KPI calculation |
| 9 | `data-vector` | Vector Manager | pgvector embeddings, similarity search |
| 10 | `data-warehouse` | Warehouse Builder | Star schema, materialized views |
| 11 | `data-report` | Report Generator | Automated reports, PDF, scheduling |
| 12 | `data-dashboard` | Dashboard Builder | Grafana/Metabase dashboards, drill-down |
| 13 | `data-events` | Event Tracker | Event schema, tracking, funnels |
| 14 | `data-cohort` | Cohort Analyzer | Retention curves, behavioral segmentation |
| 15 | `data-ab` | A/B Analyzer | Statistical significance, sample size |
| 16 | `data-forecast` | Forecast Model | Time series, trends, seasonality |
| 17 | `data-anomaly` | Anomaly Detector | Metric anomalies, baseline deviation |
| 18 | `data-privacy` | Privacy Agent | Anonymization, retention, GDPR |

### Domain 11: QA & Testing (22 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `qa-unit` | Unit Test Writer | Unit tests, assertions, edge cases, mocks |
| 2 | `qa-integration` | Integration Writer | DB/cache integration, fixtures |
| 3 | `qa-e2e` | E2E Writer | Playwright/Cypress E2E, user flows |
| 4 | `qa-api` | API Tester | REST/GraphQL testing, contract validation |
| 5 | `qa-load` | Load Tester | k6/Locust load tests, breakpoints |
| 6 | `qa-performance` | Perf Tester | Regression detection, benchmarks |
| 7 | `qa-security` | Security Tester | Auth bypass, injection, fuzzing |
| 8 | `qa-a11y` | A11y Tester | WCAG compliance, screen reader |
| 9 | `qa-visual` | Visual Regression | Screenshot diff, CSS regression |
| 10 | `qa-coverage` | Coverage Analyzer | Gaps, uncovered branches, dead code |
| 11 | `qa-mutation` | Mutation Tester | Mutation testing, test quality |
| 12 | `qa-contract` | Contract Tester | Consumer-driven contracts, Pact |
| 13 | `qa-chaos` | Chaos Tester | Failure injection, resilience |
| 14 | `qa-fixture` | Fixture Builder | Test data factories, fake data |
| 15 | `qa-mock` | Mock Builder | Mock/stub generation, service virtualization |
| 16 | `qa-regression` | Regression Hunter | Git bisect, regression ID, fix validation |
| 17 | `qa-flaky` | Flaky Detector | Flaky test ID, root cause, stabilization |
| 18 | `qa-prioritizer` | Test Prioritizer | Risk-based ordering, impact analysis |
| 19 | `qa-smoke` | Smoke Tester | Post-deploy smoke, critical paths |
| 20 | `qa-compat` | Compat Tester | Browser/device compatibility |
| 21 | `qa-data` | Data Validator | Data integrity, migration validation |
| 22 | `qa-reporter` | Test Reporter | Results, trends, quality metrics |

### Domain 12: HR & People (12 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `hr-job-writer` | Job Writer | Role descriptions, requirements, inclusive language |
| 2 | `hr-resume` | Resume Screener | Parsing, skill matching, scoring |
| 3 | `hr-interview` | Interview Prepper | Questions, scorecards, competencies |
| 4 | `hr-offer` | Offer Drafter | Offer letters, comp benchmarking, equity |
| 5 | `hr-onboarding` | Onboarding Manager | 30-60-90, checklists, buddy assignment |
| 6 | `hr-performance` | Perf Reviewer | Review templates, goals, feedback |
| 7 | `hr-engagement` | Engagement Survey | Pulse surveys, sentiment, action plans |
| 8 | `hr-policy` | Policy Writer | Handbook, PTO, remote work guidelines |
| 9 | `hr-comp` | Comp Analyst | Salary benchmarking, pay equity, bands |
| 10 | `hr-org-chart` | Org Chart Builder | Structure, reporting lines, span |
| 11 | `hr-training` | Training Planner | Learning paths, skill gaps, calendar |
| 12 | `hr-offboarding` | Offboarding Agent | Exit checklist, knowledge transfer, access revocation |

### Domain 13: Finance & Billing (15 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `fin-billing` | Billing Agent | Stripe integration, subscription mgmt, invoices |
| 2 | `fin-payment` | Payment Processor | Payment flow, retry, dunning, refunds |
| 3 | `fin-subscription` | Subscription Manager | Plan changes, proration, trials, cancellation |
| 4 | `fin-usage` | Usage Metering | Usage tracking, metered billing, overage |
| 5 | `fin-invoice` | Invoice Generator | PDF invoices, tax, multi-currency |
| 6 | `fin-revenue` | Revenue Recognizer | ASC 606, deferred revenue, MRR/ARR |
| 7 | `fin-expense` | Expense Tracker | Infra costs, vendor payments, budgets |
| 8 | `fin-tax` | Tax Calculator | Sales tax, VAT, GST by jurisdiction |
| 9 | `fin-reports` | Financial Reporter | P&L, cash flow, SaaS metrics (LTV, CAC) |
| 10 | `fin-budget` | Budget Planner | Budgets, variance, forecast vs actual |
| 11 | `fin-ar` | AR Agent | Outstanding invoices, collections, aging |
| 12 | `fin-pricing` | Pricing Modeler | Pricing pages, tiers, feature gating |
| 13 | `fin-fraud` | Fraud Detector | Payment fraud, velocity checks, risk |
| 14 | `fin-audit` | Audit Preparer | Financial audit prep, documentation |
| 15 | `fin-runway` | Runway Calculator | Burn rate, runway projection, scenarios |

### Domain 14: Legal & Governance (8 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `legal-tos` | ToS Writer | Terms, privacy policy, acceptable use, cookies |
| 2 | `legal-dpa` | DPA Drafter | Data processing agreements, sub-processors |
| 3 | `legal-contract` | Contract Reviewer | Clause analysis, risk flagging, redlines |
| 4 | `legal-ip` | IP Protector | License compliance, OSS audit, trademarks |
| 5 | `legal-gdpr` | GDPR Agent | Data subject requests, consent, retention |
| 6 | `legal-soc2` | SOC2 Preparer | Control docs, evidence, gap analysis |
| 7 | `legal-sla` | SLA Drafter | SLA docs, uptime commitments, penalties |
| 8 | `legal-incident` | Incident Notifier | Breach notifications, regulatory timelines |

### Domain 15: Content & Comms (10 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `content-tech-writer` | Tech Writer | API docs, guides, tutorials, SDK docs |
| 2 | `content-blog` | Blog Writer | SEO blogs, thought leadership, industry |
| 3 | `content-docs` | Docs Builder | MkDocs/Docusaurus site, nav, search |
| 4 | `content-changelog` | Changelog Writer | User-facing changelogs, release notes |
| 5 | `content-presentation` | Presentations | Slide decks, pitch decks, training |
| 6 | `content-internal` | Internal Comms | All-hands updates, newsletters, decisions |
| 7 | `content-status` | Status Writer | Incident updates, maintenance windows |
| 8 | `content-editor` | Copy Editor | Grammar, style, brand voice, proofing |
| 9 | `content-case-study` | Case Study Writer | Customer success stories, ROI metrics |
| 10 | `content-readme` | README Generator | Repo READMEs, quickstart, badges |

---

## Ruflo — Multi-Agent Swarm Orchestration

[github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)

```bash
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash
ruflo init
```

### Key Features

- **Mesh topology** — Agents communicate peer-to-peer, no central bottleneck
- **314 MCP tools** — Pre-built tool integrations for Claude Code
- **Hive-mind intelligence** — Shared context and memory across all agents
- **Self-learning neural routing** — Automatic task-to-agent matching
- **CYCLE_INTERVAL=0** — Zero-latency agent activation
- **Swarm orchestration** — Coordinate multiple agents on complex tasks
- **Memory persistence** — Agent learnings persist across sessions

---

## Graphify — Codebase Knowledge Graph

[github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)

```bash
pip install graphifyy
graphify install
graphify index .
```

### Key Features

- **Tree-sitter AST parsing** — 20 language support
- **Knowledge graph** — Queryable code relationships
- **Symbol resolution** — Cross-file dependency tracking
- **Impact analysis** — Understand change propagation
- **Architecture visualization** — Generate dependency diagrams
- **Semantic search** — Find code by meaning, not just text

---

## LLM Wiki — Brain Memory (Karpathy Pattern)

Citadel's agent fleet uses Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as persistent brain memory. Instead of re-deriving knowledge from scratch on every session, the LLM maintains a **compiled wiki** that compounds across all 265 agents.

### Three layers

```
docs/vault/
├── raw/        # Layer 1: immutable source documents
│               #   (articles, papers, transcripts, architecture docs,
│               #    meeting notes, customer feedback, incidents,
│               #    Obsidian Web Clipper output)
│               #   LLM reads, never modifies.
│
├── wiki/       # Layer 2: LLM-maintained compiled knowledge
│   ├── index.md         — content-oriented catalog (first lookup)
│   ├── log.md           — append-only chronological log
│   ├── overview.md      — evolving synthesis of everything
│   ├── entities/        — one page per agent, service, tool, component
│   ├── concepts/        — cross-cutting topics (multi-tenancy, canary-deploys, ...)
│   ├── sources/         — one summary per ingested raw source
│   ├── comparisons/     — analysis pages generated from queries
│   ├── contradictions/  — flagged conflicts between sources
│   └── knowledge-graph/ — Graphify AST output, feeds entity/concept pages
│
└── SCHEMA.md   # Layer 3: governance, co-evolved between human and LLM
```

### The three operations

| Operation | Command | What it does |
|-----------|---------|--------------|
| **Ingest** | `/project:wiki-ingest raw/<path>` | Read a raw source, write summary page, update 10–15 entity/concept/index/log pages in one pass, flag contradictions |
| **Query** | `/project:wiki-query <question>` | Consult `wiki/index.md` first, synthesize an answer with wiki citations, file valuable answers back as new pages so explorations compound |
| **Lint** | `/project:wiki-lint` | Health-check for orphans, stale claims, missing cross-references, concept gaps, and data gaps; suggest new questions and sources |

### Integration points

- **Obsidian graph view** — open `docs/vault/` as a vault; the graph is color-coded by layer (raw=gray, wiki=blue, SCHEMA=gold) and by agent domain. Dataview plugin enabled for querying YAML frontmatter across wiki pages.
- **Graphify feeds the wiki** — `graphify . --obsidian-dir docs/vault/wiki/knowledge-graph` produces backlinked wiki pages from AST-parsed code structure. The `wiki-curator` agent cross-links these into the entity and concept pages.
- **Agent sessions file back** — every valuable output from any of the 265 agents can be folded into the wiki via `/project:wiki-ingest`, so knowledge compounds across the whole fleet instead of dying with the chat session.
- **PreToolUse hook** — the harness reminds Claude to consult `wiki/index.md` before grepping raw files, same pattern as the Graphify knowledge-graph hook.
- **`wiki-curator` subagent** — owns the wiki layer entirely. Can touch 15 files in one pass without getting bored.

### Make targets

| Target | Purpose |
|--------|---------|
| `make wiki-ingest FILE=raw/<path>` | Ingest a raw source into the wiki |
| `make wiki-lint` | Run a health check on the wiki |
| `make wiki-sync` | Refresh Graphify output + run wiki lint |

See [`.claude/skills/llm-wiki/SKILL.md`](.claude/skills/llm-wiki/SKILL.md), [`.claude/rules/llm-wiki.md`](.claude/rules/llm-wiki.md), [`.claude/agents/wiki-curator.md`](.claude/agents/wiki-curator.md), and [`docs/vault/SCHEMA.md`](docs/vault/SCHEMA.md) for details.

---

## Obsidian Vault Integration

Every file in this repository is cross-referenced through Obsidian `[[wikilinks]]`. The vault at `docs/vault/` is a complete, navigable knowledge graph of the entire 265-agent architecture.

### What lives in the vault

```
docs/vault/
├── _index.md                — vault home / Map of Content
├── SCHEMA.md                — LLM Wiki governance (co-evolved)
├── .obsidian/               — Obsidian config (graph view, Dataview, templates)
├── raw/                     — immutable source documents (LLM Wiki layer 1)
├── wiki/                    — LLM-maintained compiled knowledge (LLM Wiki layer 2)
├── agents/                  — one note per agent (265 total) + per-domain indexes
├── architecture/            — ADR notes, tech stack, system component notes
├── runbooks/                — operational runbooks linked to agents/services
├── memory/                  — mirrors of .claude/memory/ (project context, decisions, learnings…)
└── knowledge-graph/         — Graphify-generated entity, god-node, community, surprising-connection notes
```

### Open the vault in Obsidian

1. Install [Obsidian](https://obsidian.md/).
2. Open `docs/vault/` as a vault.
3. Press `Ctrl/Cmd+G` to launch the graph view — every agent, ADR, runbook, and service appears as a node, color-coded by domain.
4. Click any node and use the **Backlinks pane** to navigate to everything that references it.

### Automatic backlinking

- **Rule** — [`.claude/rules/obsidian-backlinks.md`](.claude/rules/obsidian-backlinks.md) requires every new `.md` file in the repo to include a `## Vault Links` section.
- **Skill** — [`.claude/skills/obsidian-linker/SKILL.md`](.claude/skills/obsidian-linker/SKILL.md) scans new files, finds related vault notes by keyword and domain, and inserts bidirectional `[[wikilinks]]`.
- **Slash command** — `/project:vault-link <file>` regenerates backlinks for any file on demand.
- **Curator agent** — [`.claude/agents/obsidian-curator.md`](.claude/agents/obsidian-curator.md) audits the vault for orphan notes, broken wikilinks, and missing frontmatter.
- **PostToolUse hook** — Every write to `docs/vault/*.md` triggers `scripts/vault-autolink.py`, which auto-inserts backlinks into the file's `<!-- linked-notes -->` block.

### Graphify produces backlinked notes

`scripts/bootstrap.sh` runs `graphify . --obsidian-dir docs/vault/knowledge-graph` during setup, so the entire codebase knowledge graph is immediately available as backlinked Obsidian notes — every entity, god node, community cluster, and surprising connection becomes a vault note linked into the rest of the graph.

### Make targets

| Target | Purpose |
|--------|---------|
| `make vault-generate` | Regenerate the 265 agent notes from `.claude/agents/_registry.yaml` |
| `make vault-sync` | Refresh Graphify knowledge graph + memory mirrors |
| `make vault-audit` | Invoke the obsidian-curator agent to check vault integrity |

---

## MCP Servers

| Server | Purpose | Capabilities |
|--------|---------|-------------|
| `github` | GitHub integration | Repos, PRs, issues, Actions, GHCR |
| `filesystem` | Local file access | Read, write, search, watch files |
| `postgres` | Database access | Query, schema inspection, migrations |
| `docker` | Container management | Build, run, inspect, logs |
| `kubernetes` | Cluster management | Deployments, pods, services, logs |
| `ruflo` | Swarm orchestration | Agent spawning, memory, routing |

---

## Free Toolchain

Total monthly software cost: **$0**

| Name | License | Replaces |
|------|---------|----------|
| ArgoCD | Apache-2.0 | Spinnaker, Harness ($$$) |
| K3s | Apache-2.0 | EKS, GKE, AKS ($75-300/mo) |
| Traefik | MIT | AWS ALB, Cloudflare ($20+/mo) |
| Linkerd | Apache-2.0 | Istio, AWS App Mesh |
| Keycloak | Apache-2.0 | Auth0 ($23-240/mo), Okta ($2/user) |
| HashiCorp Vault | BUSL-1.1 | AWS Secrets Manager ($0.40/secret) |
| Prometheus | Apache-2.0 | Datadog ($15/host/mo) |
| Grafana | AGPL-3.0 | Datadog dashboards ($15/host/mo) |
| Loki | AGPL-3.0 | Splunk ($150+/GB), Datadog Logs |
| Tempo | AGPL-3.0 | Jaeger SaaS, Datadog APM |
| Falco | Apache-2.0 | Sysdig ($$$), Aqua Security |
| Kyverno | Apache-2.0 | OPA Gatekeeper, Styra DAS |
| Semgrep | LGPL-2.1 | SonarQube ($150+/mo), Snyk Code |
| Trivy | Apache-2.0 | Snyk Container ($25+/mo) |
| OWASP ZAP | Apache-2.0 | Burp Suite Pro ($449/yr) |
| Flagsmith | BSD-3 | LaunchDarkly ($10/seat/mo) |
| Grafana OnCall | AGPL-3.0 | PagerDuty ($21/user/mo) |
| Velero | Apache-2.0 | Kasten K10, Portworx Backup |
| MinIO | AGPL-3.0 | AWS S3 ($0.023/GB/mo) |
| Ansible | GPL-3.0 | Puppet, Chef, SaltStack |
| Certbot | Apache-2.0 | Commercial TLS certs ($100+/yr) |
| TruffleHog | AGPL-3.0 | GitGuardian ($30/dev/mo) |

---

## Docker Compose — Local Development

```bash
docker compose up -d
```

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL 16 | 5432 | Primary database |
| Redis 7 | 6379 | Cache and session store |
| Keycloak 24 | 8080 | Auth server (admin console) |
| MinIO | 9000 / 9001 | Object storage / console |
| RabbitMQ | 5672 / 15672 | Message broker / management |
| Mailpit | 1025 / 8025 | Local email capture / web UI |
| Traefik | 80 / 443 / 8082 | Proxy / TLS / dashboard |

---

## Token Setup

### Required

| Token | Source | Purpose |
|-------|--------|---------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Powers Claude Code, Ruflo, and Graphify |
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) | GitHub CLI, GHCR, Actions, MCP server |

### Optional

| Token | Source | Purpose |
|-------|--------|---------|
| `STRIPE_SECRET_KEY` | [dashboard.stripe.com](https://dashboard.stripe.com) | Payment processing (billing agents) |
| `SENDGRID_API_KEY` | [sendgrid.com](https://sendgrid.com) | Transactional email delivery |
| `SENTRY_DSN` | [sentry.io](https://sentry.io) | Error tracking and monitoring |
| `SLACK_WEBHOOK_URL` | [api.slack.com](https://api.slack.com) | Deployment and alert notifications |

```bash
cp .env.example .env
# Edit .env with your tokens
```

---

## Hallucination Prevention

Every LLM call in Citadel SaaS Factory routes through a **Guardrails AI** validation layer. No agent output reaches users or downstream agents without passing through guardrails. Paired with **confident-ai/deepeval** for hallucination rate evaluation and **NVIDIA NeMo-Guardrails** for conversational and agent-level guardrails.

### Quick Install

```bash
./scripts/setup-guardrails.sh
```

This installs `guardrails-ai` and `deepeval`, configures the guardrails CLI, and installs the core Hub validators (`hallucination_free`, `provenance_llm`, `toxic_language`, `detect_pii`).

### Validation Flow

```
Agent Output
    ↓
Guardrails Validator
    ↓
Schema Check (structured output enforcement)
    ↓
Hallucination Score (threshold 0.85)
    ↓
Factuality Check (against source data / RAG context)
    ↓
Provenance Verification (RAG grounding validators)
    ↓
[PASS] → Validated Output
[FAIL] → Retry with grounding (max 3) → Reject if still failing
```

### Problem → Solution Matrix

| Problem | Solution |
|---------|----------|
| Model makes things up | Validates against rules and source data |
| No grounding | RAG provenance validators |
| Inconsistent answers | Schema enforcement with deterministic outputs |
| Unsafe agent behavior | Pre/post execution guardrails |

### Minimal Usage Example

```python
from guardrails import Guard
from guardrails.hub import HallucinationFree, ProvenanceLLM

guard = Guard.from_rail_string("""
<rail version="0.1">
<output>
  <string name="answer" description="Factual answer grounded in sources" />
</output>
<prompt>
  Answer the question using ONLY the provided sources.
  Question: ${question}
  Sources: ${sources}
</prompt>
</rail>
""").use_many(
    HallucinationFree(on_fail="reask"),
    ProvenanceLLM(validation_method="sentence", on_fail="reask"),
)

validated = guard(
    llm_api=openai.chat.completions.create,
    prompt_params={"question": query, "sources": rag_docs},
)
# validated.validation_passed → True/False
# validated.validated_output → structured, hallucination-free answer
```

In the backend, all LLM calls go through `backend/app/middleware/guardrails.py`:

```python
from app.middleware.guardrails import guard_llm_call

answer = await guard_llm_call(
    llm.complete,
    prompt=user_query,
    source_context=rag_docs,
    schema={"type": "object", "properties": {"answer": {"type": "string"}}},
)
```

### Integrated Stack

| Tool | Purpose |
|------|---------|
| **guardrails-ai** | Structured output, hallucination detection, schema enforcement |
| **deepeval** | Hallucination rate evaluation, LLM test suite, CI/CD integration |
| **NVIDIA NeMo-Guardrails** | Conversational and agent-level guardrails |

### Configuration

- **Hub validators**: see `security/guardrails/validators.yaml`
- **Backend middleware**: `backend/app/middleware/guardrails.py`
- **Validator subagent**: `.claude/agents/guardrails-validator.md`
- **Skill**: `.claude/skills/guardrails/SKILL.md`
- **Rules**: `.claude/rules/guardrails.md`

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests first (TDD mandatory)
4. Ensure 80%+ code coverage
5. Run security scan: `make security`
6. Run linter: `make lint`
7. Commit with conventional format: `feat: add user auth`
8. Open a pull request
9. Wait for CI to pass (lint, test, security scan)
10. Get 1 approval minimum before merge

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

MIT License. See [LICENSE](LICENSE) for full terms.

Copyright (c) Citadel Cloud Management

---

Citadel Cloud Management | [citadelcloudmanagement.com](https://citadelcloudmanagement.com)
