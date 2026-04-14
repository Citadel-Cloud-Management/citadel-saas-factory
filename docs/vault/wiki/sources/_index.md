---
name: Sources
description: One summary page per ingested raw source.
tags: [wiki, sources]
layer: wiki
---

# Sources

One summary page per ingested raw source, with extracted key information and cross-references to every entity and concept page the source updated.

A source page is **not** a copy of the raw file. It is the LLM's compiled understanding of what that source contributed to the knowledge base.

## Page format

```markdown
---
name: <source title>
description: <one-line>
tags: [source, <kind>]
raw_path: raw/<path>
ingested: YYYY-MM-DD
updated_entities: [[[../entities/foo]], ...]
updated_concepts: [[[../concepts/bar]], ...]
confidence: 0.0 - 1.0
---

# <Source Title>

## Summary
## Key claims
## Updated pages
## Contradictions raised
## Open questions
```

## Vault Links

- [[../index|Wiki Index]]
- [[../../SCHEMA|Wiki Schema]]
- [[../../raw/README|Raw Sources Layer]]
