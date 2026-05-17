# Documentation

## Guides

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | Clone, configure, bootstrap, first run |
| [Architecture](architecture.md) | System design and component overview |
| [Deployment](deployment.md) | Staging and production deployment |
| [Security](security.md) | Security hardening guide |
| [Operations](operations.md) | Day-2 operations and maintenance |
| [Engines](engines.md) | Model engine configuration |

## Reference

| Directory | Description |
|-----------|-------------|
| `adr/` | Architecture Decision Records (5 ADRs) |
| `agents/` | Agent configuration and triage docs |
| `runbooks/` | Operational runbooks (deployment, incident response) |
| `references/` | Claude Code reference, DeerFlow integration, prompts |
| `templates/` | Document generation templates |

## Knowledge Vault

`vault/` contains the Obsidian knowledge vault — the persistent brain of the agent fleet. Open with Obsidian for graph visualization.

| Layer | Purpose |
|-------|---------|
| `vault/wiki/` | LLM-maintained compiled knowledge |
| `vault/architecture/` | ADR summaries and component pages |
| `vault/memory/` | 8-type memory system mirror |
| `vault/knowledge-graph/` | Graphify AST output |
| `vault/raw/` | Immutable source documents |
| `vault/runbooks/` | Operational procedure pages |
