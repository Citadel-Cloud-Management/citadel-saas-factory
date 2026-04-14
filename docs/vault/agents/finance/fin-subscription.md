---
agent-id: fin-subscription
name: Subscription Manager
domain: finance
domain-label: Finance & Billing
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - fin-billing
  - fin-payment
  - fin-usage
  - fin-invoice
  - fin-revenue
tags:
  - agent
  - domain/finance
---

# Subscription Manager

> **Domain:** [[_index|Finance & Billing]] · **ID:** `fin-subscription`

## Purpose

Plan changes, proration, trials, cancellation

## Domain

This agent belongs to the **Finance & Billing** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[fin-billing|Billing Agent]]
- [[fin-payment|Payment Processor]]
- [[fin-usage|Usage Metering]]
- [[fin-invoice|Invoice Generator]]
- [[fin-revenue|Revenue Recognizer]]

## Rules This Agent Follows

[[../../../.claude/rules/api-design|api-design]] [[../../../.claude/rules/security|security]]

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
