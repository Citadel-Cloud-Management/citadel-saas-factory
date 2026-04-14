---
title: Citadel SaaS Factory — Vault Home
type: index
tags: [index, home, moc]
---

# Citadel SaaS Factory — Vault Home

Welcome to the Obsidian vault for the Citadel SaaS Factory. Every file in this repository is cross-referenced through Obsidian `[[wikilinks]]`. Open this folder in Obsidian to explore the entire 265-agent architecture as a graph.

## Map of Content

- [[agents/_index|All Agents]] — 265 agents across 15 domains
- [[architecture/_index|Architecture]] — ADRs, tech stack, system components
- [[runbooks/_index|Runbooks]] — operational procedures
- [[memory/_index|Memory]] — project context, decisions, learnings
- [[knowledge-graph/_index|Knowledge Graph]] — Graphify-generated entities & communities

## How to Use

1. Install Obsidian.
2. Open `docs/vault/` as a vault.
3. Use **Graph View** (Ctrl/Cmd+G) to see all 265 agents and their relationships.
4. Use **Backlinks pane** to navigate from any note to everything that references it.
5. Run `make vault-sync` to refresh the knowledge graph from Graphify.
6. Run `make vault-audit` to check for orphan notes and broken links.

## Conventions

- Every note has YAML frontmatter with `tags`, `type`, and a `## Vault Links` section.
- Backlinks live in a `## Linked Notes` block managed by the [[../../.claude/skills/obsidian-linker/SKILL|obsidian-linker]] skill.
- New markdown files anywhere in the repo must follow [[../../.claude/rules/obsidian-backlinks|obsidian-backlinks rule]].

## Vault Links

- [[agents/_index]]
- [[architecture/_index]]
- [[runbooks/_index]]
- [[memory/_index]]
- [[knowledge-graph/_index]]
