# Hermes Agent Reference Integration

> Reference: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)

## Overview

Hermes Agent is a self-improving AI agent framework by NousResearch that emphasizes autonomous learning and persistent knowledge. The Council framework adopts several key patterns from Hermes.

## Patterns Adopted by Council Framework

### 1. Skill-Based Procedural Memory
- Hermes creates skills from experience and refines them during use
- Council sessions produce ADRs, risk registers, and verdicts that persist in the LLM Wiki
- Each session compounds knowledge for the next

### 2. Delegation & Parallel Workstreams
- Hermes spawns isolated subagents for parallel execution
- Council Prompt D implements coordinated parallel workstreams with interface contracts
- Each workstream operates independently with defined file ownership boundaries

### 3. Cross-Session Recall
- Hermes uses FTS5 session search with LLM summarization
- Council results are filed to `docs/vault/wiki/council/` for cross-session persistence
- The LLM Wiki index ensures previous Council verdicts inform future sessions

### 4. Interface Contracts
- Hermes defines function signatures before parallel execution
- Council's Three Laws enforce contracts-before-code discipline
- Shared surfaces are mapped and owned by specific workstreams

### 5. Self-Improving Loop
- Hermes skills self-improve during runtime
- Council sessions include a "Lessons Learned" section that feeds back into process improvement
- The Fact-Checker agent validates and calibrates confidence across sessions

### 6. Multi-Platform Agent Loop
- Hermes operates across CLI, Telegram, Discord, Slack, WhatsApp, Signal
- Council integrates with Citadel's backbone orchestrator and MCP gateway
- Sessions can be triggered from any connected interface

### 7. Terminal Backend Abstraction
- Hermes abstracts execution across local, Docker, SSH, Daytona, Singularity, Modal
- Council workstreams can be dispatched to different compute environments via the backbone

## Key Hermes Capabilities

| Capability | Hermes Implementation | Council Adaptation |
|---|---|---|
| 40+ built-in tools | Modular toolset with approval controls | 9 specialized agents with defined lenses |
| MCP integration | Native MCP server support | Citadel MCP gateway (8 servers) |
| 200+ model support | OpenRouter, NVIDIA NIM, HuggingFace | Model routing via `models/routing.yaml` |
| Cron scheduling | Natural language scheduled tasks | Council sessions can be scheduled via `/schedule` |
| User modeling | Honcho dialectic personality modeling | Agent memory in `.claude/memory/` |

## Vault Links

- [[../../../.claude/skills/council/SKILL|Council Skill]]
- [[../../../docs/vault/raw/council-agents-saas-prompts|Council Prompts Source]]
- [[../index|Wiki Index]]
