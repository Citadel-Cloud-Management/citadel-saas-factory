---
agent-id: qa-api
name: API Tester
domain: qa-testing
domain-label: QA & Testing
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - qa-unit
  - qa-integration
  - qa-e2e
  - qa-load
  - qa-performance
tags:
  - agent
  - domain/qa-testing
---

# API Tester

> **Domain:** [[_index|QA & Testing]] · **ID:** `qa-api`

## Purpose

REST/GraphQL testing, contract validation

## Domain

This agent belongs to the **QA & Testing** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[qa-unit|Unit Test Writer]]
- [[qa-integration|Integration Writer]]
- [[qa-e2e|E2E Writer]]
- [[qa-load|Load Tester]]
- [[qa-performance|Perf Tester]]

## Rules This Agent Follows

[[../../../.claude/rules/testing|testing]] [[../../../.claude/rules/code-quality|code-quality]]

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
