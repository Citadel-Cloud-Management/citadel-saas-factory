---
agent-id: data-query
name: Query Optimizer
domain: data-analytics
domain-label: Data & Analytics
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - data-schema
  - data-migration
  - data-index
  - data-rls
  - data-backup
tags:
  - agent
  - domain/data-analytics
---

# Query Optimizer

> **Domain:** [[_index|Data & Analytics]] · **ID:** `data-query`

## Purpose

Slow queries, N+1, rewriting

## Domain

This agent belongs to the **Data & Analytics** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[data-schema|Schema Designer]]
- [[data-migration|Migration Builder]]
- [[data-index|Index Optimizer]]
- [[data-rls|RLS Manager]]
- [[data-backup|Backup Validator]]

## Rules This Agent Follows

[[../../../.claude/rules/database|database]] [[../../../.claude/rules/performance|performance]]

## Vault Links

- Domain index: [[_index]]
- Agent registry root: [[../_index|All Agents]]
- Vault home: [[../../_index|Vault Home]]
- Architecture: [[../../architecture/_index|Architecture Index]]
- Memory: [[../../memory/_index|Memory Index]]

## Linked Notes

<!-- Auto-managed by .claude/skills/obsidian-linker — do not edit between markers -->
<!-- linked-notes:start -->
<!-- linked-notes:end -->
