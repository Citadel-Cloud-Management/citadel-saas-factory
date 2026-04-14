---
name: Entities
description: One wiki page per agent, service, tool, or component.
tags: [wiki, entities]
layer: wiki
---

# Entities

One page per **noun** in the Citadel universe: agents, services, tools, components. All 265 Citadel agents eventually get a page here with backlinks to related entities, the skills they use, the rules they follow, and the decisions that shaped them.

## Page format

Every entity page should use this template (see [[../../SCHEMA|SCHEMA]] for details):

```markdown
---
name: <entity name>
description: <one-line>
tags: [entity, <kind>, <domain>]
kind: agent | service | tool | component
sources: [<source-page-1>, <source-page-2>]
confidence: 0.0 - 1.0
status: draft | stable | superseded
date: YYYY-MM-DD
---

# <Entity Name>

## What it is
## How it works
## Related entities
## Sources
## Open questions
```

## Vault Links

- [[../index|Wiki Index]]
- [[../../SCHEMA|Wiki Schema]]
- [[../concepts/_index|Concepts]]
- [[../sources/_index|Sources]]
