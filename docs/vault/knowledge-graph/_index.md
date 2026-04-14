---
title: Knowledge Graph Index
type: index
tags: [index, knowledge-graph, graphify]
---

# Knowledge Graph

This folder receives Graphify output. Every entity, god node, community, and surprising connection becomes a vault note with Obsidian backlinks.

## Generate / Refresh

```bash
graphify . --obsidian-dir docs/vault/knowledge-graph
# or
make vault-sync
```

## What Lives Here After Sync

- **Entities** — every parsed code symbol (function, class, module) as a note
- **God nodes** — high-fan-in components flagged for review
- **Communities** — clustered subgraphs of related code
- **Surprising connections** — cross-domain edges Graphify finds

Until `graphify` runs, this index is the only file in the folder.

## Vault Links

- [[../_index|Vault Home]]
- [[../agents/_index|All Agents]]
- [[../architecture/_index|Architecture]]
- [[../runbooks/_index|Runbooks]]
