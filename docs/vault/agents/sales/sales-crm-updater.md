---
agent-id: sales-crm-updater
name: CRM Updater
domain: sales
domain-label: Sales & Revenue
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - sales-lead-qualifier
  - sales-outbound-writer
  - sales-proposal-gen
  - sales-demo-prepper
  - sales-contract-drafter
tags:
  - agent
  - domain/sales
---

# CRM Updater

> **Domain:** [[_index|Sales & Revenue]] · **ID:** `sales-crm-updater`

## Purpose

Deal stage updates, activity logging, pipeline hygiene

## Domain

This agent belongs to the **Sales & Revenue** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[sales-lead-qualifier|Lead Qualifier]]
- [[sales-outbound-writer|Outbound Writer]]
- [[sales-proposal-gen|Proposal Generator]]
- [[sales-demo-prepper|Demo Prepper]]
- [[sales-contract-drafter|Contract Drafter]]

## Rules This Agent Follows

[[../../../.claude/rules/api-design|api-design]]

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
