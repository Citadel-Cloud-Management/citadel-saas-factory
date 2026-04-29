---
name: ms-cicd-standards
description: CI/CD standards — linting, unit tests, integration tests, security scans (SAST, SCA, container, IaC), artifact signing, staging deployment, smoke testing, approval gates, production deployment. GitHub Actions + ArgoCD + Trivy + Checkov.
type: standard
priority: 17
---

# CI/CD Standards

## Core Rule

Every code change must pass through a comprehensive pipeline before reaching production. No manual deployments.

## Pipeline Stages

### Stage 1: Code Quality
```yaml
lint:
  - Python: ruff check + ruff format --check
  - TypeScript: eslint + prettier --check
  - Shell: shellcheck
  - Markdown: markdownlint
  - YAML: yamllint
  - Docker: hadolint
```

### Stage 2: Testing
```yaml
unit-tests:
  - Backend: pytest --cov=app --cov-report=xml
  - Frontend: vitest --coverage
  - Minimum coverage: 80%

integration-tests:
  - API tests against real database (testcontainers)
  - Service-to-service communication tests
  - External service contract tests
```

### Stage 3: Security Scans
```yaml
sast:
  - Semgrep with custom rules
  - CodeQL for language-specific analysis

sca:
  - npm audit / pip-audit
  - License compliance check

secrets:
  - TruffleHog / gitleaks scan
  - Detect hardcoded credentials

container:
  - Trivy image scan (CRITICAL/HIGH = block)
  - Dockerfile best practices (hadolint)

iac:
  - Checkov for Terraform
  - Kubesec for K8s manifests
  - OPA/Conftest for policy violations

dependency:
  - Dependabot / Renovate for updates
  - Known vulnerability database check
```

### Stage 4: Build
```yaml
build:
  - Multi-stage Docker build
  - Build arguments from CI environment
  - Layer caching for speed
  - SBOM generation (syft)
  - Artifact signing (cosign)
```

### Stage 5: Staging Deployment
```yaml
deploy-staging:
  - ArgoCD sync to staging namespace
  - Wait for rollout complete
  - Health check verification
  - Automatic on main branch merge

smoke-tests:
  - Critical path API tests
  - Authentication flow verification
  - Core business logic validation
  - Performance baseline check
```

### Stage 6: Production Deployment
```yaml
approval-gate:
  - Required reviewers: 1 minimum
  - All staging tests passed
  - No CRITICAL security findings
  - Change approval record created

deploy-production:
  - Canary deployment (10% → 50% → 100%)
  - Automated rollback on error rate spike
  - Post-deploy smoke tests
  - Monitoring verification
  - Notification to team channel
```

## Preferred Tooling

| Tool | Purpose |
|------|---------|
| GitHub Actions | CI orchestration |
| ArgoCD | GitOps CD |
| FluxCD | Alternative GitOps CD |
| Terraform Cloud | IaC management |
| SonarQube | Code quality gate |
| Trivy | Container + IaC scanning |
| Checkov | IaC security scanning |
| Cosign | Artifact signing |
| Syft | SBOM generation |

## Pipeline Performance Targets

| Metric | Target |
|--------|--------|
| Lint + Unit tests | < 5 minutes |
| Full pipeline (no deploy) | < 15 minutes |
| Staging deployment | < 10 minutes |
| Production deployment | < 20 minutes |
| Rollback | < 5 minutes |

## Branch Protection Rules

```yaml
main:
  required_reviews: 1
  required_checks:
    - lint
    - test
    - security-scan
  dismiss_stale_reviews: true
  require_up_to_date: true
  restrict_pushes: true
```
