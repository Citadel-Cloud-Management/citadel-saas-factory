---
agent-id: devops-cd
name: CD Deployer
domain: devops
domain-label: DevOps & Infrastructure
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
  - devops-ci
  - devops-gitops
  - devops-image-build
  - devops-image-scan
  - devops-image-sign
tags:
  - agent
  - domain/devops
---

# CD Deployer

> **Domain:** [[_index|DevOps & Infrastructure]] · **ID:** `devops-cd`

## Purpose

Deployment execution, promotion, health

## Domain

This agent belongs to the **DevOps & Infrastructure** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[devops-ci|CI Orchestrator]]
- [[devops-gitops|GitOps Sync]]
- [[devops-image-build|Image Builder]]
- [[devops-image-scan|Image Scanner]]
- [[devops-image-sign|Image Signer]]

## Rules This Agent Follows

[[../../../.claude/rules/devops|devops]] [[../../../.claude/rules/monitoring|monitoring]] [[../../../.claude/rules/secrets|secrets]]

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
