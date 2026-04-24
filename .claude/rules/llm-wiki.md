---
name: llm-wiki
description: Governance for the Citadel LLM Wiki — compounding-knowledge pattern.
tags: [wiki, rule, mandatory]
---

# LLM Wiki Rule (MANDATORY)

**The wiki is the first place Claude looks.** Before opening raw source files, before grepping the codebase for a factual question, before re-deriving knowledge the agent fleet has already compiled — read `docs/vault/wiki/index.md`.

This rule operationalizes the LLM Wiki pattern for the Citadel SaaS Factory.

## Core Rules

1. **Wiki-first lookup.** Before `Grep`/`Glob` against raw sources or application code for a factual or conceptual question, `Read docs/vault/wiki/index.md`. If the compiled knowledge answers the question, use it. This parallels the Graphify knowledge-graph navigation principle: compiled structure beats raw search.

2. **Every ingest updates index + log.** A run of `/project:wiki-ingest` (or any manual ingest) **must** update `docs/vault/wiki/index.md` (new pages registered under the right categories) **and** append `## [YYYY-MM-DD] ingest — <title>` to `docs/vault/wiki/log.md`. A silent ingest is a broken ingest.

3. **Every valuable query answer is offered for filing.** When `/project:wiki-query` produces a non-trivial answer likely to recur, the agent must **explicitly offer** to file the answer back into the wiki as a new `comparisons/`, `concepts/`, or entity-update page. Explorations must compound.

4. **Contradictions are flagged, never silently overwritten.** When a newly-ingested source conflicts with an existing wiki claim, create a page under `docs/vault/wiki/contradictions/` with a `[!contradiction]` callout and cross-links to both claims. Overwriting loses evidence.

5. **`raw/` is immutable.** The LLM reads files under `docs/vault/raw/` but **never modifies** them. Corrections, clarifications, and rebuttals live in the wiki layer, not in the source.

6. **Schema is co-evolved.** `docs/vault/SCHEMA.md` is the governance file. The human may edit it directly at any time. The LLM proposes schema edits via the `wiki-curator` agent by appending `## [YYYY-MM-DD] action — schema proposal: <change>` to `log.md`. Never invent conventions silently.

7. **Touch many pages per ingest.** A healthy ingest updates **10–15 pages**. If an ingest touches fewer than 3, cross-references were missed — redo the pass.

8. **Cite wiki, not raw.** When answering questions, cite `[[wiki/entities/foo]]` style wikilinks over raw file paths. The wiki is the compiled knowledge; raw is the ground truth only when the wiki is thin.

## Problem → Solution Matrix

| Problem | Solution |
|---------|----------|
| Agent re-derives the same answer each session | Wiki compounds — file the answer back |
| Knowledge lives only in chat history | Wiki persists across sessions |
| Raw sources contradict each other silently | Contradiction pages flag the conflict |
| Orphan pages accumulate | `/project:wiki-lint` catches them |
| Human can't see what the agent knows | Obsidian graph view of `docs/vault/` |

## Enforcement

- **PreToolUse hook** — before Grep/Glob on the repo, the harness checks whether `docs/vault/wiki/index.md` exists and reminds Claude to consult it first. Same pattern as the Graphify knowledge-graph hook.
- **Code review** — reviewers reject PRs that add LLM-authored knowledge to docs, commit messages, or chat logs without updating the wiki.
- **Curator agent** — the `wiki-curator` subagent owns the wiki layer and can touch 15 files in one pass without getting bored.
- **Lint command** — `/project:wiki-lint` or `make wiki-lint` runs a health check on a schedule.

## Why

The Citadel agent fleet (265 agents across 15 domains) runs hundreds of sessions. Without a compiled knowledge layer, each session re-reads raw sources from scratch — expensive, slow, and lossy. The LLM Wiki is the **persistent brain memory** that makes the fleet compound across sessions: every ingest adds; every valuable query answer is filed back; the index grows; the graph densifies.

## Vault Links

- [[../../docs/vault/SCHEMA|Wiki Schema]]
- [[../../docs/vault/wiki/index|Wiki Index]]
- [[../../docs/vault/wiki/log|Activity Log]]
- [[../../docs/vault/wiki/overview|Wiki Overview]]
- [[../../docs/vault/raw/README|Raw Sources Layer]]
- [[../skills/llm-wiki/SKILL|llm-wiki skill]]
- [[../agents/wiki-curator|wiki-curator agent]]
- [[../commands/wiki-ingest|/project:wiki-ingest]]
- [[../commands/wiki-query|/project:wiki-query]]
- [[../commands/wiki-lint|/project:wiki-lint]]
- [[obsidian-backlinks|obsidian-backlinks rule]]
