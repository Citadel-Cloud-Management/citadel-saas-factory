# DeerFlow 2.0 Integration Reference

## What is DeerFlow?

DeerFlow (**D**eep **E**xploration and **E**fficient **R**esearch **Flow**) is an open-source super agent harness by ByteDance that orchestrates sub-agents, memory, and sandboxes — powered by extensible skills.

- Repository: https://github.com/bytedance/deer-flow
- License: MIT
- Stack: Python 3.12 (LangGraph backend) + Next.js (frontend)

## Why It Was Removed from This Repository

DeerFlow 2.0 was previously embedded as a `deer-flow/` subdirectory (1,099 files). It was removed because:

1. It's a full standalone project with its own CI, LICENSE, README, frontend, and backend
2. It represented 57% of the repository's tracked files
3. Embedding it blurred the boundary between this framework and DeerFlow
4. Updates required manual copy rather than standard dependency management

## How to Integrate DeerFlow

### Option 1: Git Submodule (Recommended)

```bash
git submodule add https://github.com/bytedance/deer-flow.git deer-flow
git submodule update --init --recursive
```

### Option 2: Clone Separately

```bash
git clone https://github.com/bytedance/deer-flow.git deer-flow
cd deer-flow
make install  # or follow deer-flow/Install.md
```

### Option 3: Docker

```bash
cd deer-flow
docker compose up -d
```

## Connection Points

DeerFlow connects to the Citadel SaaS Factory through:

- **Skills**: DeerFlow skills can be placed in `deer-flow/skills/public/`
- **MCP Servers**: DeerFlow supports MCP server configuration via its backend
- **Model Routing**: Configure DeerFlow to use the same model tiers defined in `models/routing.yaml`
- **Agent Orchestration**: DeerFlow sub-agents can complement the 265-agent backbone system
