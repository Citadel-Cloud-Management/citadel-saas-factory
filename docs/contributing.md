# Contributing to Citadel SaaS Factory

## Getting Started

```bash
git clone <repo-url>
cd citadel-saas-factory
cp .env.example .env          # Fill in required secrets
make dev                       # Start Docker stack
make backend                   # Backend dev server (port 8000)
make frontend                  # Frontend dev server (port 3000)
```

## Project Context

Read [`context.md`](../context.md) for the full project architecture, standards, and conventions before contributing.

## Development Workflow

1. **Branch from main**: `git checkout -b feature/<ticket>-<slug>`
2. **Write tests first** (TDD mandatory): RED → GREEN → REFACTOR
3. **Run quality checks**: `make test && make lint && make security`
4. **Commit with conventional commits**: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`, `ci:`
5. **Open a PR**: 1 approval minimum, CI must pass

## Code Standards

- **Immutability**: always create new objects, never mutate
- **Small files**: 200-400 lines typical, 800 max
- **Small functions**: under 50 lines
- **80% test coverage** minimum
- **No hardcoded secrets**: use `.env` (dev) or Vault (prod)
- **Clean architecture**: domain → use cases → interfaces → infrastructure

See `.claude/rules/` for the complete set of 23 coding standards.

## Pull Request Checklist

- [ ] Tests written and passing (80%+ coverage)
- [ ] Linting passes (`make lint`)
- [ ] Security scan passes (`make security`)
- [ ] No hardcoded secrets
- [ ] `.env.example` updated if new env vars added
- [ ] ADR written if architectural decision involved
- [ ] Conventional commit messages used

## AI Agent Contributions

If adding or modifying agents:

1. Update `.claude/agents/_registry.yaml` with the new agent entry
2. Create agent definition in `.claude/agents/<domain>/<agent-id>.md`
3. Generate vault note: `make vault-generate`
4. Run `make render-agents` to sync to Cursor/Antigravity formats
5. All LLM outputs must pass through guardrails validation

## Architecture Decision Records

For decisions that affect architecture, create an ADR in `docs/adr/`:

- Follow the format in existing ADRs (e.g., `ADR-001-fastapi.md`)
- Number sequentially
- Include context, decision, and consequences

## Questions?

- Check `docs/` for documentation
- Check `docs/vault/wiki/index.md` for compiled knowledge
- Open an issue on GitHub
