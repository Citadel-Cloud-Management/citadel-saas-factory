# Backbone — 10-Layer Autonomous Agent Framework

Python framework for orchestrating 265 autonomous business agents across 15 domains.

## Architecture

```
Layer 10: Governance     Policy enforcement, RBAC, approval gates
Layer  9: Observability  Tracing, metrics, audit logging
Layer  8: Validation     Input/output validation, schema enforcement
Layer  7: Workflows      Task graphs, DAG execution, dependencies
Layer  6: Memory         Agent state, cross-session persistence
Layer  5: Orchestrator   Planning, routing, supervision, state management
Layer  4: Tools          Tool registry, MCP integration, capabilities
Layer  3: Policies       Safety guardrails, rate limits, scope control
Layer  2: Runtime        Engine execution, model routing, retries
Layer  1: Agents         Base agent class, registry, 9-agent thinking panel
```

## Run

```bash
cd backbone
pip install -e .
python -m backbone --agent ceo-strategist
python -m backbone --domain marketing
python -m backbone --list
```

## Add an Agent

1. Add entry to `.claude/agents/_registry.yaml`
2. Create definition in `.claude/agents/<name>.md`
3. Register tools in `backbone/tools/registry.py`

## Key Modules

| Module | Purpose |
|--------|---------|
| `agents/base.py` | Base agent class all agents extend |
| `agents/registry.py` | Agent discovery and instantiation |
| `agents/thinking.py` | 9-agent cognitive thinking panel |
| `orchestrator/planner.py` | Task decomposition and planning |
| `orchestrator/router.py` | Model tier routing |
| `orchestrator/supervisor.py` | Multi-agent coordination |
| `memory/manager.py` | Cross-session state persistence |
| `governance/rbac.py` | Role-based access control |
| `tools/registry.py` | Tool discovery and registration |
