---
name: Wiki Activity Log
description: Append-only chronological record of ingest, query, lint, and action events.
tags: [wiki, log, append-only]
layer: wiki
---

# Wiki Activity Log

> **Append-only.** Every ingest, query, lint, and action event is logged here with a parseable prefix so `grep "^## \[" log.md | tail -20` shows recent activity.

## Prefix format

```
## [YYYY-MM-DD] ingest | query | lint | action — short title
```

- **ingest** — a raw source was read and folded into the wiki
- **query** — a research question was answered against the wiki
- **lint** — a health check was run against the wiki
- **action** — a structural change (schema edit, new category, bulk rename)

## Recent activity

## [2026-04-12] action — Initialize LLM Wiki

Bootstrapped the three-layer LLM Wiki following Karpathy's pattern:

- Created `raw/` (immutable source layer)
- Created `wiki/` (LLM-maintained compiled knowledge: index, log, overview, entities, concepts, sources, comparisons, contradictions)
- Created `SCHEMA.md` (co-evolved governance)
- Wired `/project:wiki-ingest`, `/project:wiki-query`, `/project:wiki-lint` commands
- Registered the `wiki-curator` subagent and `llm-wiki` skill
- Added PreToolUse hook so Claude consults `wiki/index.md` before grepping raw files

Touched: `docs/vault/raw/`, `docs/vault/wiki/`, `docs/vault/SCHEMA.md`, `.claude/skills/llm-wiki/`, `.claude/commands/wiki-*.md`, `.claude/agents/wiki-curator.md`, `.claude/rules/llm-wiki.md`, `.claude/settings.json`, `Makefile`, `scripts/bootstrap.sh`, `README.md`.

## Vault Links

- [[index|Wiki Index]]
- [[overview|Wiki Overview]]
- [[../SCHEMA|Wiki Schema]]
