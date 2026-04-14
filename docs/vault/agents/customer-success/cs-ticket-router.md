---
agent-id: cs-ticket-router
name: Ticket Router
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
  - cs-response-drafter
  - cs-escalation
  - cs-churn-predictor
  - cs-health-scorer
tags:
  - agent
  - domain/customer-success
---

# Ticket Router

> **Domain:** [[_index|Customer Success & Support]] · **ID:** `cs-ticket-router`

## Purpose

Auto-categorize, prioritize, route support tickets

## Domain

This agent belongs to the **Customer Success & Support** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[cs-onboarding|Onboarding Agent]]
- [[cs-response-drafter|Response Drafter]]
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
