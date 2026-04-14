---
name: Contradictions
description: Where new sources conflict with existing claims.
tags: [wiki, contradictions]
layer: wiki
---

# Contradictions

When a newly-ingested source conflicts with an existing wiki claim, the conflict is **flagged here, not silently overwritten**. Every contradiction gets a page, a `[!contradiction]` callout, and backlinks to both sides.

## Why flag, not overwrite?

Overwriting loses the history. The old claim may have been right and the new source wrong; or the truth may depend on context. Flagging gives the curator (human or LLM) the evidence to resolve properly.

## Page format

```markdown
---
name: <contradiction title>
description: <one-line>
tags: [contradiction, <domain>]
claim_a: <page>
claim_b: <page>
status: open | resolved | stale
date: YYYY-MM-DD
---

# <Contradiction Title>

> [!contradiction]
> **Claim A** (from [[<page-a>]]): ...
> **Claim B** (from [[<page-b>]]): ...

## Resolution
## Which claim wins
## Updated pages
```

## Vault Links

- [[../index|Wiki Index]]
- [[../../SCHEMA|Wiki Schema]]
