---
agent-id: legal-contract
name: Contract Reviewer
domain: legal
domain-label: Legal & Governance
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - legal-tos
  - legal-dpa
  - legal-ip
  - legal-gdpr
  - legal-soc2
tags:
  - agent
  - domain/legal
---

# Contract Reviewer

> **Domain:** [[_index|Legal & Governance]] · **ID:** `legal-contract`

## Purpose

Clause analysis, risk flagging, redlines

## Domain

This agent belongs to the **Legal & Governance** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[legal-tos|ToS Writer]]
- [[legal-dpa|DPA Drafter]]
- [[legal-ip|IP Protector]]
- [[legal-gdpr|GDPR Agent]]
- [[legal-soc2|SOC2 Preparer]]

## Rules This Agent Follows

[[../../../.claude/rules/guardrails|guardrails]] [[../../../.claude/rules/secrets|secrets]]

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
