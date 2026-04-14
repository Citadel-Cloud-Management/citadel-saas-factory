---
agent-id: devops-gitops
name: GitOps Sync
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
  - devops-cd
  - devops-image-build
  - devops-image-scan
  - devops-image-sign
tags:
  - agent
  - domain/devops
---

# GitOps Sync

> **Domain:** [[_index|DevOps & Infrastructure]] · **ID:** `devops-gitops`

## Purpose

ArgoCD management, sync policy, drift

## Domain

This agent belongs to the **DevOps & Infrastructure** domain. See the [[_index|domain index]] for related agents.

## Related Agents

- [[devops-ci|CI Orchestrator]]
- [[devops-cd|CD Deployer]]
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
