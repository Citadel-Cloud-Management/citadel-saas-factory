# Obsidian Backlinks Rule (MANDATORY)

**Every markdown file created anywhere in the repository must be cross-linked into the Obsidian vault at `docs/vault/`.** No orphan notes.

## Core Rules

1. **`## Vault Links` section is mandatory.** Every new `.md` file — including `CLAUDE.md`, rule files, skill definitions, command definitions, agent definitions, ADRs, runbooks, READMEs, and design docs — must end with a `## Vault Links` section containing `[[wikilink]]` references to all related notes in `docs/vault/`.

2. **`## Linked Notes` block for vault notes.** Every file under `docs/vault/` must additionally include a `## Linked Notes` block delimited by HTML markers so the [[../skills/obsidian-linker/SKILL|obsidian-linker]] skill can manage backlinks idempotently:

   ```markdown
   ## Linked Notes

   <!-- linked-notes:start -->
   <!-- linked-notes:end -->
   ```

3. **Bidirectional linking.** When file A links to file B, file B must also link to file A. The `/project:vault-link` command and the obsidian-linker skill enforce this.

4. **Specific link requirements by file type:**

   | File type | Must backlink to |
   |-----------|------------------|
   | Agent definition (`.claude/agents/**/*.md`) | Its domain index, the skills it uses, the MCP servers it calls, the rules it follows |
   | Rule (`.claude/rules/*.md`) | Every agent and skill that follows the rule |
   | Skill (`.claude/skills/**/SKILL.md`) | Every agent that invokes it, every related rule |
   | Command (`.claude/commands/*.md`) | Every agent or skill it dispatches |
   | ADR (`docs/adr/*.md`) | Every agent and component the decision affects |
   | Runbook (`docs/runbooks/*.md`) | Every agent and service the procedure references |
   | Memory (`.claude/memory/*.md`) | Every agent or runbook that the memory informs |

5. **Use relative wikilinks** — `[[../agents/engineering/eng-api-designer]]`, not absolute paths or markdown links. The vault is configured with `newLinkFormat: relative`.

## Enforcement

- **PostToolUse hook** in `.claude/settings.json` matching `Write(docs/vault/*.md)` runs the linker script after every vault write to auto-insert backlinks.
- **Skill** — invoke [[../skills/obsidian-linker/SKILL|obsidian-linker]] when writing any markdown file outside the vault to compute backlinks.
- **Slash command** — `/project:vault-link <path>` regenerates backlinks for any file on demand.
- **Curator agent** — invoke the `obsidian-curator` subagent to audit the entire vault for orphan notes, broken wikilinks, and missing frontmatter. Run via `make vault-audit`.
- **Code review** — reviewers must reject any new `.md` file lacking `## Vault Links` or (for vault notes) the `## Linked Notes` markers.

## Why

The Citadel SaaS Factory has 265 agents across 15 domains. Without enforced cross-linking, the architecture is unnavigable. Obsidian's graph view turns the entire repository into an explorable knowledge graph — but only if every file participates.

## Vault Links

- [[../../docs/vault/_index|Vault Home]]
- [[../skills/obsidian-linker/SKILL|obsidian-linker skill]]
- [[../commands/vault-link|vault-link command]]
- [[../agents/obsidian-curator|obsidian-curator agent]]
- [[../../docs/vault/agents/_index|All Agents]]
