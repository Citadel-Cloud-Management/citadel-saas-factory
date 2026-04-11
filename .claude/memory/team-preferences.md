# Team Preferences

Conventions and preferences agreed upon by the team.

## Code Style
- Immutability by default
- Small files (200-400 lines typical, 800 max)
- Functions under 50 lines
- No deep nesting (max 4 levels)

## Git
- Conventional commits: feat, fix, refactor, docs, test, chore, perf, ci
- Feature branches from main
- Squash merge to main

## Testing
- TDD: write tests first
- 80% minimum coverage
- Unit + Integration + E2E

## Security
- No hardcoded secrets
- Environment variables for configuration
- Parameterized queries only
- Rate limiting on all endpoints
