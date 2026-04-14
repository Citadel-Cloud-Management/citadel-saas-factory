---
name: wiki-ingest
description: Ingest a raw source into the LLM Wiki. Updates entity, concept, index, and log pages.
argument-hint: <path-under-docs/vault/raw/>
---

# /project:wiki-ingest

Fold a raw source document into the compiled wiki layer. Follows the [[../skills/llm-wiki/SKILL|llm-wiki skill]] ingest workflow.

**Target source:** `$ARGUMENTS`

## What this does

1. **Reads** the raw file at `docs/vault/raw/$ARGUMENTS` (or the path you pass directly).
2. **Extracts** key information — claims, entities mentioned, concepts invoked, open questions.
3. **Discusses** the takeaways with you in 5–10 bullets before writing anything.
4. **Writes** a summary page to `docs/vault/wiki/sources/<slug>.md` with YAML frontmatter per [[../../docs/vault/SCHEMA|SCHEMA]].
5. **Updates** every affected entity page under `docs/vault/wiki/entities/` (creating new ones as needed).
6. **Updates** every affected concept page under `docs/vault/wiki/concepts/` (creating new ones as needed).
7. **Updates** `docs/vault/wiki/index.md` to register the new source + touched pages in the right categories.
8. **Appends** an entry to `docs/vault/wiki/log.md`:
   ```
   ## [YYYY-MM-DD] ingest — <source title>
   ```
   listing every page touched in a checklist.
9. **Flags contradictions** — if the new source conflicts with existing claims, creates a page under `docs/vault/wiki/contradictions/` with a `[!contradiction]` callout. **Never silently overwrites.**

## Expected output

A single ingest typically touches **10–15 pages**. If this run touched fewer than 3, you probably missed cross-references — re-run with broader matching.

## Instructions for Claude

1. Invoke the `llm-wiki` skill via the Skill tool before touching any files.
2. Delegate to the `wiki-curator` subagent if the source is large (>5000 words) or touches many unfamiliar entities — the curator can touch 15 files in one pass without getting bored.
3. Always end with a confirmation: `Ingested <source>. Touched <N> pages. <M> contradictions flagged.`

## Vault Links

- [[../skills/llm-wiki/SKILL|llm-wiki skill]]
- [[../agents/wiki-curator|wiki-curator agent]]
- [[../../docs/vault/wiki/index|Wiki Index]]
- [[../../docs/vault/SCHEMA|Wiki Schema]]
- [[wiki-query|/project:wiki-query]]
- [[wiki-lint|/project:wiki-lint]]
