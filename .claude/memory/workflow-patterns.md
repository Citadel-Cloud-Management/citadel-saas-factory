# Workflow Patterns

## Context Engineering
- CLAUDE.md loaded every session (keep under 200 lines)
- .claude/rules/ for path-scoped modular instructions
- Skills load on demand (not every session) — use for procedures
- Hooks execute deterministically — use for enforcement
- Auto memory compounds across sessions at ~/.claude/projects/<project>/memory/

## Harness Engineering
- 98.4% infrastructure, 1.6% AI decision logic (VILA-Lab finding)
- Seven pillars: Interfaces, Agent Loop, Permissions, Tools, State, Context, Execution
- Deny-first permissions with graduated trust
- 5 compaction layers: Budget → Snip → Microcompact → Collapse → Auto-Compact
- Summary-only returns from subagents prevent context explosion

## Memory Engineering
- 8 memory types: project-context, architecture-decisions, agent-learnings, error-patterns, deployment-history, team-preferences, workflow-patterns, tool-integrations
- MEMORY.md index (first 200 lines loaded per session)
- Topic files loaded on demand
- Vault wiki at docs/vault/wiki/ for compiled knowledge
- tasks/ for persistent cross-session tracking (lessons, decisions, anti-patterns)

## Agentic Patterns
- Plan → Explore → Implement → Verify (4-phase workflow)
- Writer/Reviewer: one session writes, another reviews
- Fan-out: `for file in list; do claude -p "..." done`
- Worktrees for parallel isolated sessions
- /batch for decomposing across worktrees
- /loop for recurring tasks within a session
- /schedule for cron-based recurring remote agents

## Orchestration Engines
- Claude Code: Primary agent harness (skills, hooks, subagents, MCP)
- Ruflo: Multi-agent swarm orchestration (314 MCP tools, mesh topology)
- Graphify: Codebase knowledge graph (Tree-sitter AST, 25 languages)
- GitHub Actions: CI/CD with claude-code-action@v1
- ArgoCD: GitOps continuous delivery
- Backbone: 10-layer autonomous agent framework (Python)
