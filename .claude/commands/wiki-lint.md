---
name: wiki-lint
description: Health-check the LLM Wiki. Flags orphans, stale claims, missing cross-references, and data gaps.
---

# /project:wiki-lint

Health-check the LLM Wiki and generate a lint report.

## What this does

Runs the [[../skills/llm-wiki/SKILL|llm-wiki skill]] lint workflow against `docs/vault/wiki/` and reports on:

- **Orphan pages** — wiki pages with zero inbound wikilinks (excluding index/log/overview).
- **Stale claims** — pages marked `status: stable` that a newer source has superseded.
- **Missing cross-references** — entity names mentioned in body text without a `[[wikilink]]`.
- **Concepts without pages** — terms used ≥3 times across the wiki without a `concepts/<term>.md` page.
- **Data gaps** — open questions in page footers that could be filled by web search or a new raw source.
- **Low-confidence stable pages** — `confidence < 0.7` + `status: stable`.
- **Unresolved contradictions** — contradiction pages with `status: open` older than 7 days.

## Output

The lint report is appended to `docs/vault/wiki/log.md`:

```
## [YYYY-MM-DD] lint — <N> findings
- <finding 1>
- <finding 2>
...

### Suggested next steps
- New questions to investigate: ...
- New sources to look for: ...
```

## Instructions for Claude

1. Invoke the `llm-wiki` skill via the Skill tool.
2. Delegate the pass to the `wiki-curator` subagent — one wide sweep is faster than many small ones.
3. End with a short summary: `Linted <N> pages. <M> findings. See wiki/log.md for details.`

## Vault Links

- [[../skills/llm-wiki/SKILL|llm-wiki skill]]
- [[../agents/wiki-curator|wiki-curator agent]]
- [[../../docs/vault/wiki/log|Activity Log]]
- [[wiki-ingest|/project:wiki-ingest]]
- [[wiki-query|/project:wiki-query]]
