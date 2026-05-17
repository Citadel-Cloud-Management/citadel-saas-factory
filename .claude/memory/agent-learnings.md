# Agent Learnings

## Patterns Discovered
- Immutable data structures across all agents — create new, never mutate
- Composition over inheritance for agent behaviors
- Stateless agents — persist state via memory/ files and tasks/
- Subagent summary-only returns prevent parent context explosion
- Skills replace commands — same /name invocation, plus supporting files
- Hooks enforce deterministically; CLAUDE.md guides probabilistically

## Integration Notes
- Ruflo orchestrates multi-agent swarm workflows via MCP (314 tools)
- Graphify provides Tree-sitter AST codebase knowledge graph
- Wiki-first lookup: check docs/vault/wiki/index.md before grepping raw sources
- Obsidian vault at docs/vault/ enables graph visualization of all knowledge

## Context Management
- /clear between unrelated tasks to reset context window
- Use Explore subagents for codebase research (keeps main context clean)
- SessionStart hook injects branch, uncommitted count, runtime versions
- Auto-compaction preserves invoked skills (first 5K tokens each, 25K total budget)

## Common Mistakes
- Don't embed full third-party projects — use git submodules or external deps
- Don't create vault notes that duplicate _registry.yaml — registry is source of truth
- Don't write hooks that match too broadly (e.g., Bash(rm -rf *) matches all Bash)
- CLAUDE.md over 200 lines causes instruction loss — use @imports for rules
