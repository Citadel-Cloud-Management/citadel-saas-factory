---
name: Wiki Overview
description: Evolving synthesis of the entire Citadel knowledge base.
tags: [wiki, overview, synthesis]
layer: wiki
last_synthesized: 2026-04-12
---

# Wiki Overview

> **The elevator pitch.** This page is an evolving narrative synthesis of everything the wiki knows about Citadel. Rewritten periodically as the knowledge base grows.

## What Citadel is

Citadel SaaS Factory is an infrastructure-agnostic SaaS framework driven by **265 autonomous business agents** across 15 domains. It runs on any Linux host with SSH + Docker, has zero cloud vendor lock-in, and carries a $0/month software bill. See the full project file: `CLAUDE.md`.

## How the wiki fits in

This wiki is the **persistent brain memory** of the Citadel agent fleet. Following the LLM Wiki pattern, it compounds knowledge across sessions instead of re-deriving everything from scratch on every question.

The wiki has three layers:

1. **`raw/`** — immutable source documents the LLM reads but never modifies
2. **`wiki/`** — compiled, LLM-maintained knowledge pages (this directory)
3. **`SCHEMA.md`** — the governance file, co-evolved between human and LLM

## The three operations

- **Ingest** — fold a raw source into the wiki, updating 10–15 entity and concept pages per pass
- **Query** — answer a question against the wiki, then file the valuable answer back as a new page
- **Lint** — health-check the wiki for orphans, stale claims, missing cross-references, and data gaps

## What the wiki currently knows

_As the wiki grows, this section will summarize the major content clusters (agent fleet, architecture, operations, decisions, patterns, open questions) in 1–2 paragraphs each._

## Vault Links

- [[index|Wiki Index]]
- [[log|Activity Log]]
- [[../SCHEMA|Wiki Schema]]
- [[../raw/README|Raw Sources Layer]]
- [[../_index|Vault Home]]
