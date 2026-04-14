---
name: vault-link
description: Scan a markdown file for vault concepts and insert bidirectional [[wikilinks]] into both the file and every note it references
argument-hint: "<file-path>"
allowed-tools: Read, Write, Edit, Grep, Glob
---

# /project:vault-link $ARGUMENTS

Regenerate Obsidian backlinks for the file at `$ARGUMENTS`.

## What this command does

1. **Read** the target file `$ARGUMENTS`.
2. **Scan** it for key concepts:
   - Agent names and IDs (`exec-ceo-strategist`, `eng-api-designer`, etc.)
   - Service names (`FastAPI`, `PostgreSQL`, `Redis`, `K3s`, `ArgoCD`, `Linkerd`, `MinIO`, `RabbitMQ`, `Keycloak`, `Vault`)
   - Technology names from the tech stack
   - Rule references (anything matching `.claude/rules/*.md`)
   - Skill references (anything matching `.claude/skills/**/SKILL.md`)
   - MCP server references
3. **Match** each concept to a note in `docs/vault/`.
4. **Insert wikilinks**:
   - Inside the target file, populate `## Vault Links` (outside the vault) or the `<!-- linked-notes:start -->`…`<!-- linked-notes:end -->` block (inside the vault).
   - In every linked note, add a backlink to `$ARGUMENTS` so the link is bidirectional.
5. **Report** what was added.

## Invocation

Invoke the [[../skills/obsidian-linker/SKILL|obsidian-linker]] skill with `$ARGUMENTS` as the target. The skill performs the actual scanning, matching, and bidirectional insertion.

## Examples

```
/project:vault-link backend/app/services/billing.py.md
/project:vault-link .claude/agents/finance/fin-billing.md
/project:vault-link docs/adr/ADR-006-stripe.md
```

## Vault Links

- [[../skills/obsidian-linker/SKILL|obsidian-linker skill]]
- [[../rules/obsidian-backlinks|obsidian-backlinks rule]]
- [[../agents/obsidian-curator|obsidian-curator agent]]
- [[../../docs/vault/_index|Vault Home]]
