# AI Agent Architecture

> For full project context, see [`context.md`](../context.md).
> For runtime agent system details, see [`agents.md`](agents.md).

## Overview

The Citadel SaaS Factory uses a multi-layered AI agent architecture spanning model routing, autonomous orchestration, guardrails validation, and multi-tool integration via MCP.

## Model Routing

Agents reference **tiers**, not specific models. Routing is defined in `models/routing.yaml`:

| Tier | Primary Model | Use Case |
|------|--------------|----------|
| `reasoning_deep` | Claude Opus 4.6 | Architecture, critical decisions |
| `reasoning_fast` | Claude Sonnet 4.6 | Default coding tasks |
| `cheap_fast` | Claude Haiku 4.5 | Tab completion, boilerplate |
| `long_context` | Gemini 3.1 Pro | Full codebase analysis (2M tokens) |
| `code_specialist` | Codestral 25 | Code generation and review |
| `vision` | Claude Opus 4.6 | Screenshot/design to code |
| `local_only` | Llama 4 Maverick | Air-gapped, zero cost |

Full catalog: `models/catalog.yaml` | 12 providers supported.

## Agent Registry

All agents are defined in `.claude/agents/_registry.yaml` with the schema:

```yaml
- id: <domain-role>
  domain: <one of 30 domains>
  name: "<display name>"
  description: "<what the agent does>"
  model: <model tier>
  skills_required: [<skill-ids>]
```

Agent definition files (`.md`) live in `.claude/agents/<domain>/` and contain system prompts, tool permissions, and workflow definitions.

## Backbone Orchestrator

The `backbone/` directory contains the Python runtime for agent orchestration:

- **Supervisor** (`backbone/orchestrator/supervisor.py`) — 6 autonomy levels from ASSISTANT to CLOSED_LOOP with approval gates
- **Router** (`backbone/orchestrator/router.py`) — Exact-match and domain-fallback routing
- **Planner** (`backbone/orchestrator/planner.py`) — Task decomposition
- **State Manager** (`backbone/orchestrator/state_manager.py`) — Execution state tracking
- **RBAC** (`backbone/governance/rbac.py`) — Role-based agent access control
- **Safety** (`backbone/policies/safety.py`) — SafetyGovernor with configurable policies

## Memory Architecture

The backbone provides 10+ memory types in `backbone/memory/`:

| Type | Purpose |
|------|---------|
| Long-term | Persistent knowledge across sessions |
| Short-term | Current session context |
| Episodic | Past interaction recall |
| Semantic | Concept relationships |
| Procedural | How-to knowledge |
| Entity | Named entity tracking |
| Working | Active task state |
| Shared | Cross-agent knowledge |

## Guardrails Pipeline

Every LLM call routes through `backend/app/middleware/guardrails.py`:

```
LLM Call → Schema Check → HallucinationFree (≥0.85) → ProvenanceLLM → ToxicLanguage → DetectPII → Output
```

- Re-ask up to 3 times on failure, then reject
- Fail-closed: if guardrails library unavailable, outputs are rejected
- All validations logged with correlation ID and scores

## MCP Connections

Tool servers configured in `.mcp.json`:

| Server | Package | Purpose |
|--------|---------|---------|
| GitHub | `@modelcontextprotocol/server-github` | Repos, PRs, issues |
| Filesystem | `@modelcontextprotocol/server-filesystem` | File access |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Database queries |
| Docker | `@modelcontextprotocol/server-docker` | Container management |
| Kubernetes | `@modelcontextprotocol/server-kubernetes` | Cluster operations |

Additional servers cataloged in `mcp/registry.yaml` (15+ available).

## Evaluation

- **promptfoo** (`evals/promptfoo.yaml`) — Model evaluation with concrete test cases
- **DeepEval** (`evals/deepeval/`) — CI integration for hallucination detection (≤5% per PR)
- **AI layer evals** (`ai/evals/`) — Task-specific evaluation with Council Framework

## Governance Rules

- No autonomous agent receives unrestricted production access
- All LLM output passes through guardrails validation
- Agent tool permissions are scoped per agent definition
- Human override capability required at all autonomy levels
- Budget limits enforced per agent tier

## Key Files

| What | Where |
|------|-------|
| Agent registry | `.claude/agents/_registry.yaml` |
| Agent definitions | `.claude/agents/<domain>/*.md` |
| Backbone runtime | `backbone/` |
| Guardrails middleware | `backend/app/middleware/guardrails.py` |
| Model routing | `models/routing.yaml` |
| Model catalog | `models/catalog.yaml` |
| MCP config | `.mcp.json` |
| MCP registry | `mcp/registry.yaml` |
| Evaluations | `evals/` |
| Skills | `.claude/skills/` |
