---
agent-id: data-migration
name: Migration Builder
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
  - data-index
  - data-query
  - data-rls
  - data-backup
tags:
  - agent
  - domain/data-analytics
---

# Migration Builder

> **Domain:** [[_index|Data & Analytics]] · **ID:** `data-migration`

## Purpose

Safe DDL, zero-downtime, rollback

## Domain

This agent belongs to the **Data & Analytics** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[data-schema|Schema Designer]]
- [[data-index|Index Optimizer]]
- [[data-query|Query Optimizer]]
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
