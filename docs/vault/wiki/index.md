---
name: Wiki Index
description: Content-oriented catalog of every wiki page. The LLM's first lookup when answering questions.
tags: [wiki, index, catalog]
layer: wiki
page_count: 0
last_updated: 2026-04-12
---

# Wiki Index

> **The compiled knowledge base.** Every page the LLM has written lives here, categorized by what it describes. Consult this file **before** grepping raw sources — the wiki is what the LLM has already learned.

## How to use this index

1. **Search this file first** for the entity, concept, or source you need.
2. **Follow the wikilink** to read the compiled page.
3. If the answer isn't here, read the relevant raw sources and **file a new wiki page** back into the appropriate category.

```dataview
TABLE file.mtime AS "Updated", tags
FROM "wiki"
WHERE !contains(file.path, "index") AND !contains(file.path, "log") AND !contains(file.path, "overview")
SORT file.mtime DESC
LIMIT 30
```

---

## Entities

> One page per agent, service, tool, or component. All 265 Citadel agents eventually get their own page here.

_No entity pages yet. Run `/project:wiki-ingest` on raw sources to start populating this section._

### Agents
<!-- wiki-index:entities:agents:start -->
<!-- wiki-index:entities:agents:end -->

### Services
<!-- wiki-index:entities:services:start -->
<!-- wiki-index:entities:services:end -->

### Tools
<!-- wiki-index:entities:tools:start -->
<!-- wiki-index:entities:tools:end -->

### Components
<!-- wiki-index:entities:components:start -->
<!-- wiki-index:entities:components:end -->

---

## Concepts

> Cross-cutting topics that span multiple entities. When the same idea shows up in three or more sources, it earns its own concept page.

<!-- wiki-index:concepts:start -->
- _multi-tenancy_ — pending
- _canary-deploys_ — pending
- _hallucination-prevention_ — pending
- _knowledge-graphs_ — pending
- _swarm-orchestration_ — pending
<!-- wiki-index:concepts:end -->

---

## Sources

> One summary page per ingested raw source with extracted key information and cross-references to the entity and concept pages the source updated.

<!-- wiki-index:sources:start -->
<!-- wiki-index:sources:end -->

---

## Architecture

> System-level design pages. Fed by Graphify's AST output and human-authored ADRs.

<!-- wiki-index:architecture:start -->
<!-- wiki-index:architecture:end -->

---

## Operations

> Runbooks, incident playbooks, deployment procedures — as distilled by the wiki curator, not the raw runbook text.

<!-- wiki-index:operations:start -->
<!-- wiki-index:operations:end -->

---

## Decisions

> Compiled ADR summaries with full cross-references to affected entities.

<!-- wiki-index:decisions:start -->
<!-- wiki-index:decisions:end -->

---

## Patterns

> Reusable design patterns distilled from multiple sources — the Citadel playbook as it accumulates.

<!-- wiki-index:patterns:start -->
<!-- wiki-index:patterns:end -->

---

## Comparisons

> Analysis pages generated from queries and filed back into the wiki so explorations compound.

<!-- wiki-index:comparisons:start -->
<!-- wiki-index:comparisons:end -->

---

## Contradictions

> Where new sources conflict with existing claims. Flagged, never silently overwritten.

<!-- wiki-index:contradictions:start -->
<!-- wiki-index:contradictions:end -->

## Vault Links

- [[../_index|Vault Home]]
- [[log|Activity Log]]
- [[overview|Wiki Overview]]
- [[../SCHEMA|Wiki Schema]]
- [[../raw/README|Raw Sources Layer]]
- [[../../../.claude/skills/llm-wiki/SKILL|llm-wiki skill]]
