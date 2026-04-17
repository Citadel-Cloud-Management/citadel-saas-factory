# GitHub Copilot Instructions

## Project Context

Citadel SaaS Factory — 265-agent SaaS framework. FastAPI (Python 3.12) + Next.js 14 (TypeScript) + PostgreSQL 16 + K3s + ArgoCD.

## Code Style

- Python: snake_case, PascalCase classes, type hints required
- TypeScript: camelCase, PascalCase components, strict mode
- Files: kebab-case (user-service.py, auth-form.tsx)
- Immutability: always create new objects, never mutate
- Small functions (<50 lines), small files (<800 lines)
- No deep nesting (max 4 levels)

## Security

- No hardcoded secrets — use environment variables or Vault
- Parameterized queries only — no SQL string concatenation
- Validate all user input at system boundaries
- Rate limiting on all API endpoints
- XSS/CSRF/CORS protection on all routes
- All LLM output passes through guardrails validation

## Testing

- TDD: write tests first
- 80% minimum coverage
- Test pyramid: unit > integration > E2E
- Mock external services, not internal modules

## Architecture

- Clean architecture: domain > use cases > interfaces > infrastructure
- Repository pattern for data access
- Service layer for business logic
- RESTful API with consistent response envelope: { data, error, meta }
- API versioning via URL prefix: /api/v1/

## Git

- Conventional commits: feat, fix, refactor, docs, test, chore, perf, ci
- Feature branches from main
- PR required, CI must pass

## Multi-Model

See `models/routing.yaml` for tier-based model selection across Anthropic, OpenAI, Google, and open-weights providers.
