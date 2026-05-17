# Research Report: Claude Code CLAUDE.md Structure & Cloneable Agentic Workflow

**Date:** 2026-05-17
**Researcher:** Claude Opus 4.6
**Scope:** Complete extraction of Claude Code configuration patterns for making a SaaS factory repo cloneable as an agentic workflow

---

## Executive Summary

Claude Code's architecture is **98.4% deterministic infrastructure, 1.6% AI decision logic** (VILA-Lab research). The differentiator for production agents is the harness — not the model. This report extracts every configuration pattern needed to make a repo instantly functional as an agentic workflow when cloned.

Key findings: CLAUDE.md must stay under 200 lines using `@imports`; `.claude/rules/` replaces bloated CLAUDE.md sections; hooks provide deterministic enforcement (27 event types); skills are the new commands; subagents isolate context; settings.json controls permissions with deny-first security.

---

## Key Findings

### 1. The .claude Directory — Complete Structure

Official structure from [code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory):

```
your-project/
├── CLAUDE.md                    # Project instructions (committed)
├── CLAUDE.local.md              # Personal overrides (gitignored)
├── .claude/
│   ├── CLAUDE.md                # Alternative location for project instructions
│   ├── settings.json            # Shared settings (committed)
│   ├── settings.local.json      # Personal overrides (gitignored)
│   ├── rules/                   # Path-scoped modular instructions
│   │   ├── code-style.md        # Always-on rules (no paths frontmatter)
│   │   ├── testing.md
│   │   ├── api-design.md
│   │   └── frontend/
│   │       └── react-patterns.md  # Path-scoped (paths: "src/**/*.tsx")
│   ├── skills/                  # Reusable workflows (replaces commands/)
│   │   └── <skill-name>/
│   │       ├── SKILL.md         # Required — instructions + frontmatter
│   │       ├── references/      # Optional deep docs
│   │       ├── scripts/         # Optional executable scripts
│   │       └── templates/       # Optional output templates
│   ├── agents/                  # Custom subagent definitions
│   │   └── <agent-name>.md     # YAML frontmatter + system prompt
│   ├── commands/                # Legacy (still works, skills preferred)
│   │   └── deploy.md
│   ├── hooks/                   # Shell scripts for lifecycle hooks
│   │   └── format-on-save.sh
│   ├── mcp/                     # MCP server configs
│   ├── templates/               # Code generation templates
│   ├── memory/                  # Auto memory (gitignored, auto-generated)
│   └── plugins/                 # Installed plugin manifests
├── .mcp.json                    # MCP server registry
├── AGENTS.md                    # Cross-IDE universal instructions
├── GEMINI.md                    # Gemini/Jules specific
└── AGENT.md                     # Cursor agent config
```

**User-level (~/.claude/):**
```
~/.claude/
├── CLAUDE.md              # Personal global instructions
├── settings.json          # Personal global settings
├── rules/                 # Personal global rules
├── skills/                # Personal skills (all projects)
├── agents/                # Personal subagents
├── keybindings.json       # Custom keyboard shortcuts
└── projects/<hash>/       # Auto memory per project
    └── memory/
        ├── MEMORY.md      # Index (first 200 lines loaded)
        └── <topic>.md     # Topic files (loaded on demand)
```

### 2. CLAUDE.md Best Practices (2026 Consensus)

From [Anthropic official docs](https://code.claude.com/docs/en/best-practices), [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [ObviousWorks](https://www.obviousworks.ch/en/designing-claude-md-right-the-2026-architecture-that-finally-makes-claude-code-work/):

**Size:** Under 200 lines. Some teams run < 60 lines. Shorter = better adherence.

**Three-layer structure:**
1. **WHAT** — Project identity (stack, repo map)
2. **WHY** — Architecture decisions, non-obvious constraints
3. **HOW** — Workflow rules, commands, conventions

**What to include:**
- Commands Claude can't guess (`make lint`, `uv run pytest`)
- Conventions that differ from defaults
- Architecture decisions specific to this project
- Developer environment quirks
- Common gotchas

**What to exclude:**
- Anything Claude can figure out from reading code
- Standard language conventions
- Long explanations or tutorials
- File-by-file descriptions
- Self-evident practices

**Pruning test:** For each line ask "Would removing this cause Claude to make mistakes?" If no → delete it.

**`@import` pattern** (critical for staying under 200 lines):
```markdown
@.claude/rules/code-quality.md
@.claude/rules/testing.md
@.claude/rules/security.md
```

### 3. Settings.json — Complete Reference

From [code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings):

**Priority:** Managed > CLI args > Local > Project > User

**Permission rules use glob-like syntax:**
```
Tool(specifier)         # E.g., Bash(npm run *)
Read(./.env*)           # Deny reading secrets
Edit(./src/**)          # Allow editing src recursively
Skill(deploy *)         # Control skill access
MCP(github)             # Control MCP access
```

**Key settings for cloneable repos:**
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-sonnet-4-6",
  "alwaysThinkingEnabled": true,
  "autoMemoryEnabled": true,
  "effortLevel": "high",
  "permissions": {
    "allow": ["Read", "Edit", "Write", "Glob", "Grep", "Agent", "Skill(*)"],
    "deny": ["Read(.env)", "Read(.env.*)", "Bash(rm -rf /)"],
    "defaultMode": "acceptEdits"
  }
}
```

### 4. Hooks — 27 Lifecycle Events

From [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks):

**Five hook types:** command, http, mcp_tool, prompt, agent

**Critical events for cloneable projects:**

| Event | Use Case |
|-------|----------|
| `SessionStart` | Inject git branch, uncommitted count, env info |
| `PreToolUse(Bash)` | Block destructive commands |
| `PostToolUse(Write\|Edit)` | Auto-format (ruff, prettier) |
| `PostToolUse(Write(docs/vault/*.md))` | Auto-link Obsidian |
| `Stop` | Validate work before completion |
| `UserPromptSubmit` | Inject project context |

**Hook exit codes:** 0 = success (parse JSON), 2 = blocking error, other = non-blocking

### 5. Skills — The New Commands

From [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills):

Commands and skills are now the same mechanism. Skills are preferred because they support:
- Supporting files (references/, scripts/, templates/)
- Frontmatter control (model, effort, context, allowed-tools)
- Dynamic context injection (`!`command``)
- Subagent execution (`context: fork`)
- Path-scoped activation (`paths: "src/api/**"`)

**Key frontmatter fields:**
```yaml
---
name: deploy
description: Deploy the application
disable-model-invocation: true    # User-only invocation
allowed-tools: Bash(git *) Bash(make *)
context: fork                     # Run in subagent
agent: general-purpose
model: sonnet
effort: high
---
```

### 6. Subagents — Context Isolation

From [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents):

```yaml
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
skills: [security-audit]
memory: true
---
You are a senior security engineer...
```

**Built-in types:** `general-purpose` (all tools), `Explore` (read-only), `Plan` (read-only + planning)

**Key pattern:** Summary-only returns — child verbosity doesn't explode parent context.

### 7. Harness Architecture — Seven Pillars

From [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code):

| Pillar | What It Does |
|--------|--------------|
| User & Interfaces | CLI, SDK, IDE entry points |
| Agent Loop | ReAct-pattern async generator, 9-step per-turn pipeline |
| Permission System | 7 modes, deny-first, graduated trust |
| Tools | 54 built-in + MCP extensibility |
| State & Persistence | Append-only JSONL transcripts, file-based memory |
| Context Management | 5 compaction layers (Budget → Snip → Microcompact → Collapse → Auto-Compact) |
| Execution Environment | Sandboxing, subagent isolation, session recovery |

**Key insight:** "The loop is easy to copy; hooks, classifier, compaction, and isolation are not."

### 8. GitHub Actions — Official Integration

From [code.claude.com/docs/en/github-actions](https://code.claude.com/docs/en/github-actions):

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "/skill-name"  # Can invoke skills directly
    claude_args: "--model claude-sonnet-4-6 --max-turns 15"
```

**Three job pattern:** @claude interaction, PR review, issue resolution.

---

## Implementation Recommendations

### What This Project Already Has (Verified)

| Component | Count | Status |
|-----------|-------|--------|
| CLAUDE.md | 112 lines | Under 200-line limit, uses @imports |
| settings.json | Full config | SessionStart hook, permissions, auto-format |
| Skills (SKILL.md) | 24 | Proper directory structure |
| Agent definitions | 11 | YAML frontmatter + system prompts |
| Commands | 37 | Mix of .md and .yaml |
| Hooks | 11 | Shell scripts |
| Rules | 21 | .claude/rules/ with topic files |
| Templates | 20 | Code generation templates |
| MCP configs | 8 | Server definitions |
| IDE configs | 13 | 10+ AI coding platforms |
| GitHub Actions | 8 | Including claude-code-action@v1 |
| Model catalog | 3 | catalog.yaml, routing.yaml, embeddings.yaml |
| Setup script | 1 | scripts/setup.sh validates everything |

### What Makes This Repo Clone-Ready

1. **`scripts/setup.sh`** — Validates all 15 infrastructure components on clone
2. **`.claude/settings.json`** — Production permissions, hooks, auto-format
3. **`.github/workflows/claude.yml`** — Official `anthropics/claude-code-action@v1`
4. **`.env.example`** — Complete environment template
5. **`AGENTS.md`** — Cross-IDE universal instructions
6. **`GEMINI.md`** — Gemini/Jules config
7. **`AGENT.md`** — Cursor agent config
8. **10+ IDE configs** — Codex, Continue, Devin, Jules, Factory, Antigravity, Windsurf, Daytona, Codegen

---

## Resources & References

### Official Documentation
- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [.claude Directory Explorer](https://code.claude.com/docs/en/claude-directory)
- [CLAUDE.md & Memory](https://code.claude.com/docs/en/memory)
- [Settings Reference](https://code.claude.com/docs/en/settings)
- [Hooks Guide](https://code.claude.com/docs/en/hooks)
- [Skills](https://code.claude.com/docs/en/skills)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Best Practices](https://code.claude.com/docs/en/best-practices)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)

### Research & Analysis
- [Dive into Claude Code — VILA-Lab](https://github.com/VILA-Lab/Dive-into-Claude-Code) — 98.4% infrastructure finding
- [Harness Architecture: Seven Pillars](https://community.sap.com/t5/artificial-intelligence-blogs-posts/agentic-harness-architecture-seven-pillars-that-make-claude-code-production/ba-p/14395198)
- [10 Agentic AI Harness Patterns](https://kenhuangus.substack.com/p/the-claude-code-leak-10-agentic-ai)
- [Awesome Harness Engineering](https://github.com/ai-boost/awesome-harness-engineering)

### Community Templates & Showcases
- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) — Comprehensive config example
- [diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) — 6 months production-tested
- [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) — Visual guide, v2.1.138
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — Curated skill/hook list
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) — Hooks deep-dive
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — Agent harness optimization

### Guides
- [Complete Guide to CLAUDE.md — MikeWang](https://medium.com/@n913239/the-complete-guide-to-claude-md-make-claude-code-truly-understand-your-project-d9d026b808f1)
- [Writing a Good CLAUDE.md — HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Designing CLAUDE.md Correctly — ObviousWorks](https://www.obviousworks.ch/en/designing-claude-md-right-the-2026-architecture-that-finally-makes-claude-code-work/)
- [CLAUDE.md Guide — Braincuber](https://www.braincuber.com/tutorial/writing-best-claude-md-complete-guide)
- [Claude Code Best Practices — ranthebuilder](https://ranthebuilder.cloud/blog/claude-code-best-practices-lessons-from-real-projects/)
- [Claude Code Cheat Sheet — SkillsPlayground](https://skillsplayground.com/guides/claude-code-cheat-sheet/)

---

## Unresolved Questions

1. **Managed settings deployment** — How to distribute managed-settings.json across teams without MDM?
2. **Skill marketplace** — No official skill registry beyond plugins; community fragmented across GitHub repos
3. **Agent registry validation** — No official schema for _registry.yaml; our 265-agent registry is project-specific
4. **Cross-session memory sync** — Auto memory is machine-local; no built-in sync across machines
5. **Hook testing** — No official test harness for hooks; must test manually with `--debug`
