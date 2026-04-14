---
agent-id: legal-incident
name: Incident Notifier
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
  - legal-contract
  - legal-ip
  - legal-gdpr
tags:
  - agent
  - domain/legal
---

# Incident Notifier

> **Domain:** [[_index|Legal & Governance]] · **ID:** `legal-incident`

## Purpose

Breach notifications, regulatory timelines

## Domain

This agent belongs to the **Legal & Governance** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[legal-tos|ToS Writer]]
- [[legal-dpa|DPA Drafter]]
- [[legal-contract|Contract Reviewer]]
- [[legal-ip|IP Protector]]
- [[legal-gdpr|GDPR Agent]]

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
