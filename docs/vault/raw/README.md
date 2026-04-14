---
name: Raw Sources Layer
description: Immutable ground-truth source documents. Read by the LLM, never modified.
tags: [wiki, layer, raw]
layer: raw
---

# Raw Sources — Layer 1 of the LLM Wiki

This directory is the **immutable source-of-truth layer** of the Citadel LLM Wiki (Karpathy pattern).

## Rules

- **Immutable.** The LLM reads files here but **never modifies** them. If a source is wrong, it stays wrong — the correction lives in the wiki layer as a contradiction callout.
- **Append-only.** New sources are added; existing sources are never edited in place.
- **Anything goes.** Articles, papers, images, data files, Obsidian Web Clipper output, agent session transcripts, architecture docs, meeting notes, customer feedback, incident reports, exported Slack threads, PDFs.

## Suggested layout

```
raw/
├── articles/        # External articles, papers, blog posts
├── transcripts/     # Agent session transcripts, meeting notes
├── architecture/    # Design docs, ADR drafts, whiteboard exports
├── incidents/       # Postmortems, incident timelines
├── customer/        # Customer feedback, interviews, support tickets
├── clippings/       # Obsidian Web Clipper output
└── data/            # CSVs, JSON dumps, exported datasets
```

## Ingest workflow

When a new source lands here, run:

```bash
make wiki-ingest FILE=raw/articles/karpathy-llm-wiki.md
# or inside Claude Code:
# /project:wiki-ingest raw/articles/karpathy-llm-wiki.md
```

The [[../../../.claude/agents/wiki-curator|wiki-curator agent]] reads the source, writes a summary page to `wiki/sources/`, updates the entity and concept pages it touches, and appends an entry to `wiki/log.md`.

## Vault Links

- [[../_index|Vault Home]]
- [[../wiki/index|Wiki Index]]
- [[../SCHEMA|Wiki Schema]]
- [[../../../.claude/skills/llm-wiki/SKILL|llm-wiki skill]]
- [[../../../.claude/agents/wiki-curator|wiki-curator agent]]
