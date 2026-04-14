---
agent-id: eng-code-reviewer
name: Code Reviewer
domain: engineering
domain-label: Engineering & Backend
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - eng-api-designer
  - eng-model-builder
  - eng-schema-builder
  - eng-service-builder
  - eng-repo-builder
tags:
  - agent
  - domain/engineering
---

# Code Reviewer

> **Domain:** [[_index|Engineering & Backend]] · **ID:** `eng-code-reviewer`

## Purpose

PR review, patterns, complexity, security checks

## Domain

This agent belongs to the **Engineering & Backend** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[eng-api-designer|API Designer]]
- [[eng-model-builder|Model Builder]]
- [[eng-schema-builder|Schema Builder]]
- [[eng-service-builder|Service Builder]]
- [[eng-repo-builder|Repository Builder]]

## Rules This Agent Follows

[[../../../.claude/rules/api-design|api-design]] [[../../../.claude/rules/architecture|architecture]] [[../../../.claude/rules/code-quality|code-quality]] [[../../../.claude/rules/error-handling|error-handling]]

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
