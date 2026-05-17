# Contributing to Citadel SaaS Factory

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make changes following the conventions below
4. Open a pull request

## Development Workflow

```bash
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git
cd citadel-saas-factory
cp .env.example .env
bash scripts/setup.sh    # Verify infrastructure
claude                   # Start Claude Code
```

## Conventions

- **TDD mandatory**: Write tests first, 80%+ coverage
- **Conventional commits**: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- **Small files**: 200-400 lines typical, 800 max
- **Immutability**: Create new objects, never mutate
- **No hardcoded secrets**: Use environment variables or Vault

## Pull Request Process

1. CI must pass (lint, test, security scan)
2. 1 approval minimum
3. Squash merge to main
4. PR description includes what changed and why

## Code Style

- **Python**: snake_case functions, PascalCase classes, ruff for formatting
- **TypeScript**: camelCase functions, PascalCase components, prettier for formatting
- **Files**: kebab-case (`user-service.py`, `auth-form.tsx`)

## Agent Skills

To add a new skill, create `.claude/skills/<name>/SKILL.md`. See [skills docs](https://code.claude.com/docs/en/skills).

## Reporting Issues

Use [GitHub Issues](https://github.com/Citadel-Cloud-Management/citadel-saas-factory/issues) with the appropriate template.
