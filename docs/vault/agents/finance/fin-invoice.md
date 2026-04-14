---
agent-id: fin-invoice
name: Invoice Generator
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
  - fin-subscription
  - fin-usage
  - fin-revenue
tags:
  - agent
  - domain/finance
---

# Invoice Generator

> **Domain:** [[_index|Finance & Billing]] · **ID:** `fin-invoice`

## Purpose

PDF invoices, tax, multi-currency

## Domain

This agent belongs to the **Finance & Billing** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[fin-billing|Billing Agent]]
- [[fin-payment|Payment Processor]]
- [[fin-subscription|Subscription Manager]]
- [[fin-usage|Usage Metering]]
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
