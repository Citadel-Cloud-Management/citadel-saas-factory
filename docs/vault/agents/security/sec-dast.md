---
agent-id: sec-dast
name: DAST Scanner
domain: security
domain-label: Security & Compliance
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - sec-sast
  - sec-sca
  - sec-secret
  - sec-container
  - sec-iac
tags:
  - agent
  - domain/security
---

# DAST Scanner

> **Domain:** [[_index|Security & Compliance]] · **ID:** `sec-dast`

## Purpose

OWASP ZAP dynamic testing, API fuzzing

## Domain

This agent belongs to the **Security & Compliance** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[sec-sast|SAST Scanner]]
- [[sec-sca|SCA Scanner]]
- [[sec-secret|Secret Scanner]]
- [[sec-container|Container Scanner]]
- [[sec-iac|IaC Scanner]]

## Rules This Agent Follows

[[../../../.claude/rules/security|security]] [[../../../.claude/rules/secrets|secrets]] [[../../../.claude/rules/guardrails|guardrails]]

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
