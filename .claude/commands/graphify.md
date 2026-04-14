---
description: Build or query the Graphify knowledge graph
argument-hint: "[path-or-query]"
---

Build or query the Graphify codebase knowledge graph for **$ARGUMENTS**.

```
!graphify index .
```

```
!graphify query "$ARGUMENTS"
```

Graphify provides Tree-sitter AST-based knowledge graphs across 20 languages. Use for:
- Finding symbol definitions and references
- Tracing call graphs
- Understanding cross-file dependencies
- Impact analysis for refactoring
