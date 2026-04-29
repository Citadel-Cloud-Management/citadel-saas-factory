---
name: ms-folder-structure
description: Default project folder structure for all new projects — apps, services, packages, infrastructure (terraform/kubernetes/helm), agents, AI, docs, monitoring, security, CI, tests, Docker, scripts.
type: template
priority: 15
---

# Default Folder Structure

## Core Rule

Use this baseline structure unless project requirements dictate otherwise. Every directory must have a clear purpose and owner.

## Standard Structure

```
project-root/
├── apps/                          # User-facing applications
│   ├── web/                       # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/               # App Router pages
│   │   │   ├── components/        # React components
│   │   │   ├── hooks/             # Custom hooks
│   │   │   ├── lib/               # Utilities
│   │   │   ├── stores/            # Zustand stores
│   │   │   └── types/             # TypeScript types
│   │   ├── public/                # Static assets
│   │   ├── tests/                 # Frontend tests
│   │   └── package.json
│   └── mobile/                    # React Native (optional)
│
├── services/                      # Backend services
│   ├── api/                       # Main API (FastAPI/Express)
│   │   ├── src/
│   │   │   ├── domain/            # Business logic
│   │   │   ├── infrastructure/    # DB, external services
│   │   │   ├── interfaces/        # Controllers, routes
│   │   │   └── use-cases/         # Application logic
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── workers/                   # Background job processors
│   └── gateway/                   # API gateway (optional)
│
├── packages/                      # Shared libraries
│   ├── shared-types/              # Cross-service types
│   ├── utils/                     # Common utilities
│   └── config/                    # Shared configuration
│
├── infrastructure/                # Infrastructure as Code
│   ├── terraform/                 # Cloud resources
│   │   ├── modules/               # Reusable modules
│   │   ├── environments/          # Per-environment configs
│   │   └── main.tf
│   ├── kubernetes/                # K8s manifests
│   │   ├── base/                  # Base configurations
│   │   └── overlays/              # Environment overlays
│   ├── helm/                      # Helm charts
│   │   └── charts/
│   └── scripts/                   # Infra automation scripts
│
├── agents/                        # AI agent definitions
│   ├── definitions/               # Agent specs
│   ├── prompts/                   # System prompts
│   └── tools/                     # Agent tool definitions
│
├── ai/                            # AI/ML components
│   ├── models/                    # Model configs
│   ├── embeddings/                # Embedding pipelines
│   ├── evals/                     # Evaluation suites
│   └── guardrails/                # Safety validators
│
├── docs/                          # Documentation
│   ├── adr/                       # Architecture Decision Records
│   ├── runbooks/                  # Operational runbooks
│   ├── api/                       # API documentation
│   └── vault/                     # Knowledge vault (Obsidian)
│
├── monitoring/                    # Observability configs
│   ├── grafana/                   # Dashboard definitions
│   ├── prometheus/                # Alert rules, recording rules
│   ├── loki/                      # Log pipeline config
│   └── alerts/                    # Alert definitions
│
├── security/                      # Security configs
│   ├── policies/                  # OPA/Kyverno policies
│   ├── scanning/                  # SAST/DAST configs
│   └── compliance/                # Compliance evidence
│
├── ci/                            # CI/CD pipelines
│   └── workflows/                 # Reusable workflow definitions
│
├── tests/                         # Cross-cutting tests
│   ├── e2e/                       # End-to-end tests
│   ├── integration/               # Integration tests
│   ├── load/                      # Load/performance tests
│   └── security/                  # Security tests
│
├── .github/                       # GitHub-specific
│   ├── workflows/                 # GitHub Actions
│   ├── CODEOWNERS
│   └── pull_request_template.md
│
├── docker/                        # Docker configs
│   ├── dev/                       # Dev environment
│   └── prod/                      # Production builds
│
├── scripts/                       # Utility scripts
│   ├── setup.sh                   # Developer setup
│   ├── seed.sh                    # Database seeding
│   └── migrate.sh                 # Migration runner
│
├── docker-compose.yml             # Local dev stack
├── Makefile                       # Command shortcuts
├── .env.example                   # Env var contract
└── README.md                      # Project overview
```

## Directory Ownership

| Directory | Owner | Review Required |
|-----------|-------|----------------|
| apps/ | Frontend team | Frontend lead |
| services/ | Backend team | Backend lead |
| infrastructure/ | DevOps team | DevOps lead + SecOps |
| security/ | SecOps team | CISO |
| monitoring/ | SRE team | SRE lead |
| ai/ | ML team | ML lead |
| docs/ | All teams | Tech writer |
