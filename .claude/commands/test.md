---
description: Run tests with optional scope
argument-hint: "[unit|e2e|all]"
---

Run **$ARGUMENTS** tests for the project.

## Test Scopes
- **unit**: `cd backend && pytest -m unit` and `cd frontend && npm test`
- **e2e**: `cd frontend && npx playwright test`
- **all**: Run unit + integration + E2E tests with coverage report

Ensure 80% minimum coverage. Report any failures with root cause analysis.
