---
agent-id: cs-response-drafter
name: Response Drafter
domain: customer-success
domain-label: Customer Success & Support
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - cs-onboarding
  - cs-ticket-router
  - cs-escalation
  - cs-churn-predictor
  - cs-health-scorer
tags:
  - agent
  - domain/customer-success
---

# Response Drafter

> **Domain:** [[_index|Customer Success & Support]] · **ID:** `cs-response-drafter`

## Purpose

Draft support responses from knowledge base, tone consistency

## Domain

This agent belongs to the **Customer Success & Support** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[cs-onboarding|Onboarding Agent]]
- [[cs-ticket-router|Ticket Router]]
- [[cs-escalation|Escalation Agent]]
- [[cs-churn-predictor|Churn Predictor]]
- [[cs-health-scorer|Health Scorer]]

## Rules This Agent Follows

[[../../../.claude/rules/documentation|documentation]]

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
