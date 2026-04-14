---
agent-id: cs-escalation
name: Escalation Agent
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
  - cs-response-drafter
  - cs-churn-predictor
  - cs-health-scorer
tags:
  - agent
  - domain/customer-success
---

# Escalation Agent

> **Domain:** [[_index|Customer Success & Support]] · **ID:** `cs-escalation`

## Purpose

Escalation signals, senior routing, escalation summaries

## Domain

This agent belongs to the **Customer Success & Support** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[cs-onboarding|Onboarding Agent]]
- [[cs-ticket-router|Ticket Router]]
- [[cs-response-drafter|Response Drafter]]
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
