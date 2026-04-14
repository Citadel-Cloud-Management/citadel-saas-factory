---
agent-id: qa-e2e
name: E2E Writer
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
  - qa-api
  - qa-load
  - qa-performance
tags:
  - agent
  - domain/qa-testing
---

# E2E Writer

> **Domain:** [[_index|QA & Testing]] · **ID:** `qa-e2e`

## Purpose

Playwright/Cypress E2E, user flows

## Domain

This agent belongs to the **QA & Testing** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[qa-unit|Unit Test Writer]]
- [[qa-integration|Integration Writer]]
- [[qa-api|API Tester]]
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
