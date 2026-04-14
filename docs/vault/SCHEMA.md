---
name: Wiki Schema
description: Governance file for the LLM Wiki. Co-evolved between human and LLM as the wiki grows.
tags: [wiki, schema, governance]
layer: schema
version: 0.1.0
last_updated: 2026-04-12
---

# Wiki Schema

> **Governance, not scripture.** This file defines the current conventions of the Citadel LLM Wiki. It is **co-evolved** between the human curator and the LLM. When the wiki outgrows a rule here, update the schema first, then reshape the wiki to match.

## The three layers

| Layer | Path | Who writes | Who reads | Mutability |
|-------|------|------------|-----------|------------|
| Raw | `docs/vault/raw/` | Humans, ingest pipelines, Obsidian Web Clipper | LLM | **Immutable** |
| Wiki | `docs/vault/wiki/` | LLM (wiki-curator agent) | LLM + humans | Append + edit |
| Schema | `docs/vault/SCHEMA.md` | Human ↔ LLM dialogue | Both | Edit by consensus |

## Wiki structure conventions

```
wiki/
├── index.md               # Content catalog — always the first lookup
├── log.md                 # Append-only activity log
├── overview.md            # Evolving narrative synthesis
├── entities/              # One page per agent, service, tool, component
├── concepts/              # Cross-cutting topics (multi-tenancy, canary-deploys, ...)
├── sources/               # One summary per ingested raw source
├── comparisons/           # Analysis pages from queries
├── contradictions/        # Flagged conflicts between sources
└── knowledge-graph/       # Graphify output (auto-generated)
```

### When to create a new page

- **Entity page** — any agent, service, tool, or component referenced by ≥2 sources or ≥1 source plus code.
- **Concept page** — any cross-cutting idea referenced by ≥3 sources.
- **Source page** — one per raw file ingested.
- **Comparison page** — any query whose answer is non-trivial and likely to be re-asked.
- **Contradiction page** — any conflict between sources the LLM cannot resolve unilaterally.

## Page format template

Every wiki page (except `index.md`, `log.md`, `overview.md`) uses this YAML frontmatter:

```yaml
---
name: <human-readable title>
description: <one-line summary used in index.md>
tags: [<kind>, <domain>, ...]
date: YYYY-MM-DD
source_count: <integer>   # how many raw sources back this page
confidence: 0.0 - 1.0     # curator's confidence in the claims
status: draft | stable | superseded
---
```

Every page ends with a `## Vault Links` section containing relative `[[wikilinks]]` to at least: the wiki index, the SCHEMA, and every related page.

## Naming rules

- **Files**: `kebab-case.md` (e.g., `hallucination-prevention.md`, `eng-api-designer.md`)
- **Titles**: Title Case in the `name` frontmatter and the H1
- **Tags**: lowercase, hyphenated, singular nouns (`agent`, not `Agents`)
- **Cross-references**: relative wikilinks only (`[[../concepts/foo]]`), never absolute paths or markdown links

## Ingest workflow

1. A raw source lands in `docs/vault/raw/<kind>/<file>`.
2. Human or hook invokes `/project:wiki-ingest raw/<kind>/<file>`.
3. The [[../../.claude/agents/wiki-curator|wiki-curator agent]]:
   - Reads the source end-to-end.
   - Drafts a summary page at `wiki/sources/<slug>.md`.
   - Updates every entity page the source touches (create if missing).
   - Updates every concept page the source touches (create if missing).
   - Appends an entry to `wiki/log.md` with prefix `## [YYYY-MM-DD] ingest — <title>`.
   - Updates `wiki/index.md` with new pages and updated metadata.
   - Flags any contradictions as `wiki/contradictions/<slug>.md` with `[!contradiction]` callouts.
4. A single ingest touches **10–15 pages** on average. That's the point.

## Query workflow

1. Human or agent invokes `/project:wiki-query <question>`.
2. The curator:
   - Searches `wiki/index.md` for relevant entries.
   - Reads the matching pages.
   - Synthesizes an answer with citations back to the wiki pages (not raw sources, unless necessary).
   - **Offers to file the answer back** as a comparison/concept/entity page if the question is likely to recur.
   - Appends a `## [YYYY-MM-DD] query — <short>` entry to `log.md`.

## Lint checklist

Run `/project:wiki-lint` or `make wiki-lint`. The curator checks for:

- [ ] **Orphan pages** — wiki pages with zero inbound links (excluding index/log/overview).
- [ ] **Stale claims** — pages marked `status: stable` that a newer source has superseded.
- [ ] **Missing cross-references** — entity A mentioned by name in entity B's page without a wikilink.
- [ ] **Concepts without pages** — terms used ≥3 times across the wiki that have no concept page.
- [ ] **Data gaps** — open questions in page footers that could be filled with a web search or new raw source.
- [ ] **Contradictions unresolved** — contradiction pages with `status: open` older than 7 days.
- [ ] **Low-confidence stable pages** — pages with `confidence < 0.7` but `status: stable`.

The lint report lands at `wiki/log.md` as a `## [YYYY-MM-DD] lint — <count> findings` entry.

## Co-evolution rules

- The human can **edit this schema directly** at any time.
- The LLM **proposes schema edits** via the wiki-curator agent when it notices patterns the schema doesn't cover. Proposals land in `log.md` as `## [YYYY-MM-DD] action — schema proposal: <change>`.
- When the schema changes, the wiki curator is responsible for **reshaping existing pages** to match (or proposing a migration plan if the change is large).

## Vault Links

- [[wiki/index|Wiki Index]]
- [[wiki/log|Activity Log]]
- [[wiki/overview|Wiki Overview]]
- [[raw/README|Raw Sources Layer]]
- [[_index|Vault Home]]
- [[../../.claude/skills/llm-wiki/SKILL|llm-wiki skill]]
- [[../../.claude/agents/wiki-curator|wiki-curator agent]]
- [[../../.claude/rules/llm-wiki|llm-wiki rule]]
