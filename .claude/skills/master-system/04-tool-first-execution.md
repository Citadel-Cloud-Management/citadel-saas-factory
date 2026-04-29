---
name: ms-tool-first-execution
description: Always prioritize MCP tools, repositories, project files, runtime context, and infrastructure state over assumptions. Never invent information when tools can verify it.
type: directive
priority: 4
---

# Tool-First Execution Model

## Core Rule

Always use available tools to verify state before making claims or taking action. Do not invent information when systems can verify it.

## Priority Order

1. **MCP tools** — query live systems (GitHub, databases, K8s, monitoring)
2. **Available repositories** — read actual code, configs, manifests
3. **Project files** — check existing implementations, schemas, tests
4. **Runtime context** — environment variables, running processes, logs
5. **Infrastructure state** — cluster status, service health, resource usage
6. **Memory/context systems** — prior decisions, patterns, preferences

## Before Any Claim

| Claim Type | Verify With |
|------------|-------------|
| "File X exists" | Glob/Read tool |
| "Function Y is defined" | Grep tool |
| "Service is running" | Bash (docker ps, kubectl get) |
| "API returns Z" | WebFetch or API test |
| "Dependency version" | Read package.json/pyproject.toml |
| "Environment configured" | Read .env.example, check vars |
| "Tests pass" | Bash (run test suite) |
| "Branch is clean" | Bash (git status) |

## When Tools Are Unavailable

If a tool cannot verify the claim:

1. **State assumptions explicitly** — "Assuming PostgreSQL 16 based on docker-compose.yml"
2. **Estimate confidence level** — HIGH (seen in code), MEDIUM (inferred), LOW (assumed)
3. **Identify unknowns** — "Cannot verify cluster state without kubectl access"

## Anti-Patterns

- Assuming a file exists without checking
- Claiming a function signature without reading it
- Recommending a package version without checking compatibility
- Describing infrastructure state without querying it
- Making deployment decisions without checking current state

## Tool Selection Matrix

| Task | Primary Tool | Fallback |
|------|-------------|----------|
| Find files | Glob | Bash (find) |
| Search code | Grep | Agent (Explore) |
| Read configs | Read | Bash (cat) |
| Check git state | Bash (git) | — |
| Query APIs | WebFetch | Bash (curl) |
| Database state | MCP postgres | Bash (psql) |
| Container state | Bash (docker) | MCP docker |
| K8s resources | Bash (kubectl) | MCP kubernetes |
| CI/CD status | MCP github | Bash (gh) |
