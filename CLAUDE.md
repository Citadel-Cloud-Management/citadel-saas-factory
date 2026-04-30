# Citadel SaaS Factory — Claude Code

> **Canonical context**: [`context.md`](context.md) — all architecture, standards, conventions, and agent system details.
> This file contains Claude Code-specific extensions only.

---

## Quick Start

```bash
make dev          # Start Docker stack
make backend      # Backend dev server (port 8000)
make frontend     # Frontend dev server (port 3000)
make test         # Run all tests
make lint         # Run linters
make status       # System health report
```

Full command reference: see [context.md § 9](context.md#9-repository-execution-map)

## Claude Code Extensions

### Hooks (settings.json)

| Event | Trigger | Action |
|-------|---------|--------|
| PreToolUse | Write `*.py` | `ruff check` |
| PreToolUse | Write `*.ts`/`*.tsx` | `npx eslint` |
| PreToolUse | Grep/Glob | Remind to check LLM Wiki first |
| PostToolUse | Write `*.py` | `ruff format` |
| PostToolUse | Write `*.ts`/`*.tsx` | `npx prettier` |
| PostToolUse | Write `docs/vault/*.md` | `vault-autolink.sh` |

### MCP Connections

Configured in `.claude/mcp/` and `.mcp.json`:

| Server | Config | Purpose |
|--------|--------|---------|
| GitHub | `.claude/mcp/github.json` | Repos, PRs, issues, Actions |
| PostgreSQL | `.claude/mcp/postgres.json` | Database queries |
| Docker | `.claude/mcp/docker.json` | Container management |
| Kubernetes | `.claude/mcp/kubernetes.json` | Cluster operations |
| Filesystem | `.claude/mcp/filesystem.json` | File access |
| Redis | `.claude/mcp/redis.json` | Cache operations |
| Vault | `.claude/mcp/vault.json` | Secret management |
| Prometheus | `.claude/mcp/prometheus.json` | Metrics queries |

### Knowledge Layer

#### Obsidian Vault (`docs/vault/`)
- Every `.md` file must have a `## Vault Links` section with `[[wikilinks]]`
- Bidirectional linking enforced by `vault-autolink.sh`
- Graph view: `docs/vault/_index.md` is the entry point

#### LLM Wiki (Karpathy Pattern)
- `docs/vault/raw/` — immutable source documents (LLM reads, never modifies)
- `docs/vault/wiki/` — LLM-maintained compiled knowledge
- `docs/vault/wiki/index.md` — **always consult before grepping raw sources**
- `docs/vault/SCHEMA.md` — governance, co-evolved between human and LLM

### Intelligence Layer

```
.claude/
├── agents/       ← 500+ agent definitions + _registry.yaml
├── commands/     ← /deploy, /review, /test, /audit, etc.
├── hooks/        ← pre-commit, post-deploy, vault-autolink
├── rules/        ← 23 coding standards
├── skills/       ← specialist capabilities
├── memory/       ← persistent project memory
├── mcp/          ← MCP server configs
├── templates/    ← code generation templates
└── settings.json ← hooks, permissions, model routing
```

### Do / Don't

DO:
- Run `make test` before every commit
- Update `.env.example` when adding env vars
- Write ADRs for architectural decisions (`docs/adr/`)
- Use `.claude/templates/` for code generation
- Check `docs/vault/wiki/index.md` before grepping the codebase
- Keep startup deterministic: clone → env → bootstrap → run

DON'T:
- Commit to `main` directly
- Commit secrets (`.env`, `*.pem`, `*.key`)
- Install new top-level deps without a PR discussion
- Introduce a new framework without an ADR
- Bypass guardrails or skip validation
- Force push to main/production
