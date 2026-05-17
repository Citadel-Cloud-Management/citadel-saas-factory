# Team Preferences

## Code Style
- Immutability by default — create new objects, never mutate
- Small files: 200-400 lines typical, 800 max
- Functions under 50 lines, max 4 levels nesting
- Explicit over implicit: clear names, no magic

## Git
- Conventional commits: feat, fix, refactor, docs, test, chore, perf, ci
- Feature branches from main, squash merge
- No force push to main/production

## Testing
- TDD mandatory: RED → GREEN → IMPROVE
- 80% minimum coverage (95% for auth, payments)
- Unit + Integration + E2E required

## Security
- No hardcoded secrets — env vars or Vault
- Parameterized queries only
- Rate limiting on all endpoints
- Every LLM call through guard_llm_call()

## Agentic Workflow
- Plan before executing (use plan mode for non-trivial tasks)
- Subagents for investigation (keep primary context clean)
- /clear between unrelated tasks
- After corrections: update tasks/lessons.md
- Verification before completion: tests, lint, type check, no regressions

## Documentation
- Obsidian backlinks on all .md files
- Wiki-first lookup before grepping raw sources
- ADRs for significant architectural decisions
