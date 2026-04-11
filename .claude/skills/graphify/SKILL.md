# Graphify — Knowledge Graph Integration

## Description
Build and query a knowledge graph from the codebase using Graphify. Navigate code by structure and relationships instead of raw file search.

## When to Use
- Before exploring an unfamiliar codebase
- When understanding cross-module dependencies
- When answering architectural questions
- Before making changes that span multiple files

## Commands
- `/graphify .` — Build knowledge graph from current directory
- `/graphify . --update` — Incremental update
- `/graphify . --wiki` — Generate wiki documentation
- `/graphify . --obsidian-dir <path>` — Export to Obsidian

## Output
- `graphify-out/graph.html` — Interactive visual graph
- `graphify-out/GRAPH_REPORT.md` — God nodes, connections, suggested questions
- `graphify-out/graph.json` — Queryable graph data

## Integration
The PreToolUse hook ensures Claude consults the graph before every Glob and Grep call, reducing token usage by up to 71x.
