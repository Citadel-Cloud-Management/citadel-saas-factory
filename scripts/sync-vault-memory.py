"""Mirror .claude/memory/*.md into docs/vault/memory/ with vault-friendly frontmatter and backlinks."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / ".claude" / "memory"
DST = REPO / "docs" / "vault" / "memory"
DST.mkdir(parents=True, exist_ok=True)

MEMORY_FILES = [
    ("project-context.md", "Project Context", "project"),
    ("architecture-decisions.md", "Architecture Decisions", "architecture"),
    ("agent-learnings.md", "Agent Learnings", "agents"),
    ("error-patterns.md", "Error Patterns", "errors"),
    ("deployment-history.md", "Deployment History", "deployment"),
    ("team-preferences.md", "Team Preferences", "team"),
]

for fname, title, tag in MEMORY_FILES:
    src = SRC / fname
    if not src.exists():
        body = "_Source file not yet created. Will be populated as the project evolves._"
    else:
        body = src.read_text(encoding="utf-8")
    note = f"""---
title: {title}
type: memory
source-doc: .claude/memory/{fname}
tags: [memory, {tag}]
---

# {title}

> Mirrored from [`.claude/memory/{fname}`](../../../.claude/memory/{fname}). Run `make vault-sync` to refresh.

{body}

## Vault Links

- [[_index|Memory Index]]
- [[../_index|Vault Home]]
- [[../agents/_index|All Agents]]
- [[../architecture/_index|Architecture]]
- [[../runbooks/_index|Runbooks]]

## Linked Notes

<!-- linked-notes:start -->
<!-- linked-notes:end -->
"""
    (DST / fname).write_text(note, encoding="utf-8")

(DST / "_index.md").write_text("""---
title: Memory Index
type: index
tags: [index, memory]
---

# Memory

Project memory mirrored from `.claude/memory/`. Refreshed via `make vault-sync`.

## Notes

- [[project-context|Project Context]]
- [[architecture-decisions|Architecture Decisions]]
- [[agent-learnings|Agent Learnings]]
- [[error-patterns|Error Patterns]]
- [[deployment-history|Deployment History]]
- [[team-preferences|Team Preferences]]

## Vault Links

- [[../_index|Vault Home]]
- [[../agents/_index|All Agents]]
- [[../runbooks/_index|Runbooks]]
""", encoding="utf-8")

print(f"mirrored {len(MEMORY_FILES)} memory files")
