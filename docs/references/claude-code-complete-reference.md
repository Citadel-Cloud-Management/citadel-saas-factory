# Claude Code Complete Reference

> Extracted from official documentation at code.claude.com/docs (May 2026).
> This is the definitive reference for configuring Claude Code as an agentic workflow.

---

## 1. Configuration Hierarchy

Settings are resolved by priority (highest wins):

| Priority | Scope | Location | Shared? |
|----------|-------|----------|---------|
| 1 | Managed | `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS), `/etc/claude-code/managed-settings.json` (Linux), `C:\Program Files\ClaudeCode\managed-settings.json` (Windows) | Org-wide |
| 2 | CLI args | `--model`, `--max-turns`, etc. | Session only |
| 3 | Local | `.claude/settings.local.json` (gitignored) | No |
| 4 | Project | `.claude/settings.json` (committed) | Yes |
| 5 | User | `~/.claude/settings.json` | No |

**Key rules:**
- Deny rules always win (merge, never override)
- Most restrictive setting applies for security
- Managed settings cannot be overridden

---

## 2. Settings File Structure

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run *)", "Read(~/.zshrc)"],
    "deny": ["Bash(curl *)", "Read(./.env*)"],
    "ask": ["Bash(git push *)"],
    "additionalDirectories": ["../docs/"],
    "defaultMode": "acceptEdits"
  },
  "model": "claude-sonnet-4-6",
  "alwaysThinkingEnabled": true,
  "autoMemoryEnabled": true,
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  }
}
```

### Core Settings

| Setting | Type | Description |
|---------|------|-------------|
| `model` | string | Default model (`claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5`) |
| `effortLevel` | string | `low`, `medium`, `high`, `xhigh` |
| `alwaysThinkingEnabled` | boolean | Extended thinking by default |
| `autoMemoryEnabled` | boolean | Auto memory on/off |
| `spinnerTipsEnabled` | boolean | Show tips while processing |
| `language` | string | Response language |
| `tui` | string | `"fullscreen"` for alt-screen renderer |

### Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Prompt for each action |
| `acceptEdits` | Auto-accept edits, prompt for dangerous ops |
| `plan` | View plan before execution |
| `auto` | AI classifier decides |
| `bypassPermissions` | Skip all checks (dangerous) |

### Permission Rule Syntax

```
Tool                    → All uses of that tool
Tool(specifier)         → Matching uses only
Bash(npm run *)         → Commands starting with "npm run"
Read(./.env)            → Reading specific file
Edit(./src/**)          → Editing files in src recursively
WebFetch(domain:x.com)  → Fetch requests to domain
MCP(*)                  → All MCP operations
Skill(deploy *)         → Specific skill invocations
```

---

## 3. CLAUDE.md Memory System

### File Locations (load order, broadest to most specific)

| Scope | Location | Purpose |
|-------|----------|---------|
| Managed | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Org-wide |
| User | `~/.claude/CLAUDE.md` | Personal all-projects |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared |
| Local | `./CLAUDE.local.md` (gitignored) | Personal per-project |

### Writing Effective CLAUDE.md

- Target under 200 lines per file
- Use markdown headers and bullets
- Be specific: "Use 2-space indentation" not "format code properly"
- Import files with `@path/to/import` syntax
- Import AGENTS.md: `@AGENTS.md` at top of CLAUDE.md

### Auto Memory

- Stored at `~/.claude/projects/<project>/memory/`
- `MEMORY.md` is the index (first 200 lines loaded per session)
- Topic files loaded on demand
- Claude writes memories automatically based on corrections

### Path-Scoped Rules (.claude/rules/)

```yaml
# .claude/rules/api-design.md
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- Use RESTful naming conventions
- Return consistent error formats
```

Rules without `paths` load unconditionally. Path-scoped rules trigger when Claude reads matching files.

---

## 4. Skills System

### Skill Directory Structure

```
.claude/skills/<skill-name>/
├── SKILL.md           # Required — main instructions
├── references/        # Optional — detailed docs
├── scripts/           # Optional — executable scripts
├── templates/         # Optional — output templates
└── examples/          # Optional — example outputs
```

### Skill Locations

| Location | Path | Scope |
|----------|------|-------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled |

### SKILL.md Frontmatter

```yaml
---
name: my-skill                      # Display name (lowercase, hyphens, max 64 chars)
description: What it does           # Used for auto-discovery
when_to_use: Additional triggers    # Appended to description
argument-hint: "[issue-number]"     # Autocomplete hint
arguments: [issue, branch]          # Named positional args
disable-model-invocation: true      # Only user can invoke
user-invocable: false               # Only Claude can invoke
allowed-tools: Read Grep Bash(git *)# Pre-approved tools
model: opus                         # Model override for this skill
effort: high                        # Effort level override
context: fork                       # Run in subagent
agent: Explore                      # Which agent type for fork
paths: "src/api/**"                 # Path-scoped activation
shell: bash                         # Shell for !`command`
hooks:                              # Scoped hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./check.sh"
---
```

### Dynamic Context Injection

```markdown
## Current state
!`git status --short`
!`git diff --cached --stat`

## Environment
```!
node --version
npm --version
```
```

### String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed |
| `$ARGUMENTS[N]` / `$N` | Nth argument (0-based) |
| `$name` | Named argument from `arguments` field |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_EFFORT}` | Current effort level |
| `${CLAUDE_SKILL_DIR}` | Skill directory path |

---

## 5. Subagents (.claude/agents/)

### Agent Definition Format

```yaml
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
skills: [security-audit, owasp-check]
memory: true
---

You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Display name |
| `description` | When Claude should delegate to this agent |
| `tools` | Comma-separated tool list (Read, Grep, Glob, Bash, Edit, Write, Agent, etc.) |
| `model` | Model to use (`opus`, `sonnet`, `haiku`, or full ID) |
| `skills` | Skills to preload into the subagent |
| `memory` | Enable persistent auto memory for the subagent |
| `hooks` | Scoped hooks for this agent's lifecycle |

### Built-in Agent Types

| Type | Tools | Use For |
|------|-------|---------|
| `general-purpose` | All tools | Multi-step tasks |
| `Explore` | Read-only (Glob, Grep, Read) | Codebase research |
| `Plan` | Read-only + planning | Architecture design |

---

## 6. Hooks System

### Hook Events

| Event | When | Can Block? |
|-------|------|------------|
| `SessionStart` | Session begins/resumes | No |
| `SessionEnd` | Session terminates | No |
| `UserPromptSubmit` | User sends prompt | Yes |
| `PreToolUse` | Before tool execution | Yes |
| `PostToolUse` | After tool succeeds | Yes |
| `PostToolUseFailure` | After tool fails | Yes |
| `PermissionRequest` | Permission dialog | Yes |
| `Stop` | Claude finishes responding | Yes |
| `StopFailure` | Turn ends due to error | No |
| `SubagentStart` | Subagent spawned | No |
| `SubagentStop` | Subagent finishes | Yes |
| `FileChanged` | Watched file changes | No |
| `CwdChanged` | Working directory changes | No |
| `ConfigChange` | Config file changes | Yes |

### Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "timeout": 600,
            "statusMessage": "Validating command..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write ${tool_input.file_path}"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Types

| Type | Description |
|------|-------------|
| `command` | Shell command (receives JSON on stdin) |
| `http` | HTTP POST to endpoint |
| `mcp_tool` | Call MCP server tool |
| `prompt` | Send prompt to Claude for yes/no |
| `agent` | Spawn subagent for verification |

### Hook Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Project root |
| `CLAUDE_PLUGIN_ROOT` | Plugin installation directory |
| `CLAUDE_PLUGIN_DATA` | Persistent plugin data directory |
| `CLAUDE_ENV_FILE` | File to persist env vars |
| `CLAUDE_CODE_REMOTE` | `"true"` in web environments |
| `CLAUDE_EFFORT` | Current effort level |

### Command Hook Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (parse stdout for JSON) |
| 2 | Blocking error (tool call prevented) |
| Other | Non-blocking error (continues) |

---

## 7. MCP Server Configuration

### .mcp.json Format

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "..."
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

### CLI Management

```bash
claude mcp add <name> <command> [args...]   # Add server
claude mcp remove <name>                     # Remove server
claude mcp list                              # List servers
claude mcp test <name>                       # Test connection
```

### Settings for MCP

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["github", "memory"],
  "disabledMcpjsonServers": ["filesystem"],
  "allowedMcpServers": [{"serverName": "github"}],
  "deniedMcpServers": [{"serverName": "filesystem"}]
}
```

---

## 8. GitHub Actions Integration

### Official Action (v1)

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          trigger_phrase: "@claude"
```

### Action Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `prompt` | Instructions (plain text or skill name) | No |
| `claude_args` | CLI arguments | No |
| `anthropic_api_key` | API key | Yes* |
| `github_token` | GitHub token | No |
| `trigger_phrase` | Custom trigger (default: "@claude") | No |
| `use_bedrock` | Use Amazon Bedrock | No |
| `use_vertex` | Use Google Vertex AI | No |
| `plugin_marketplaces` | Plugin marketplace URLs | No |
| `plugins` | Plugins to install | No |

### Skill-Based Workflow

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "/code-review:code-review ${{ github.repository }}/pull/${{ github.event.pull_request.number }}"
```

---

## 9. CLI Reference

### Key Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive session |
| `claude -p "prompt"` | Non-interactive (headless) mode |
| `claude --continue` | Resume most recent session |
| `claude --resume` | Choose session to resume |
| `claude --model opus` | Override model |
| `claude --max-turns N` | Limit conversation turns |
| `claude --allowedTools "Edit,Bash(git *)"` | Restrict tools |
| `claude --permission-mode auto` | Use auto permission mode |
| `claude --output-format json` | JSON output (headless) |
| `claude --output-format stream-json` | Streaming JSON |
| `claude --add-dir ../other-repo` | Add directory access |
| `claude --append-system-prompt "text"` | Append to system prompt |
| `claude --init-only` | Initialize without starting session |
| `claude mcp add/remove/list` | Manage MCP servers |
| `claude config` | View/edit settings |

### Interactive Commands (Slash Commands)

| Command | Description |
|---------|-------------|
| `/init` | Generate starter CLAUDE.md |
| `/plan` | Toggle plan mode |
| `/model` | Switch models |
| `/effort` | Adjust effort level |
| `/compact` | Summarize context |
| `/clear` | Reset context window |
| `/memory` | Browse CLAUDE.md and auto memory |
| `/permissions` | Manage permission rules |
| `/mcp` | Manage MCP servers |
| `/agents` | Manage subagents |
| `/skills` | Browse and manage skills |
| `/hooks` | Browse configured hooks |
| `/tasks` | List background tasks |
| `/config` | Settings editor |
| `/doctor` | Diagnose configuration issues |
| `/context` | Visualize context window usage |
| `/rewind` | Restore to previous checkpoint |
| `/btw` | Side question (no context cost) |
| `/rename` | Rename current session |
| `/background` | Detach session to background |
| `/batch` | Decompose task across worktrees |
| `/loop` | Repeat prompt on interval |
| `/schedule` | Create recurring routine |
| `/desktop` | Hand off to desktop app |
| `/install-github-app` | Set up GitHub Actions |

### Bundled Skills (Prompt-Based Commands)

| Skill | Description |
|-------|-------------|
| `/simplify` | Review and simplify changed code |
| `/debug` | Systematic debugging workflow |
| `/batch` | Fan out work across worktrees |
| `/loop` | Repeat on interval |
| `/claude-api` | Build Claude API applications |
| `/review` | Code review |
| `/security-review` | Security audit |

### Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_MODEL` | Override default model |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable telemetry |
| `CLAUDE_CODE_DISABLE_THINKING` | Disable extended thinking |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Disable auto memory |
| `CLAUDE_CODE_EFFORT_LEVEL` | Set effort level |
| `CLAUDE_CODE_NO_FLICKER` | Fullscreen renderer |
| `DISABLE_AUTOUPDATER` | Disable auto-updates |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Esc` | Stop current action |
| `Esc + Esc` | Open rewind menu |
| `Ctrl+G` | Open plan in editor |
| `Option+T` / `Alt+T` | Toggle extended thinking |
| `Ctrl+O` | Toggle verbose/thinking output |

---

## 10. Best Practices Summary

### CLAUDE.md

- Run `/init` to generate starter file
- Keep under 200 lines
- Include only what Claude can't figure out from code
- Prune regularly — if Claude follows a rule without the instruction, delete it
- Use `@imports` for shared content

### Prompting

- Give Claude verification criteria (tests, screenshots, expected output)
- Explore first (plan mode), then plan, then implement
- Reference specific files, constraints, and patterns
- Use `@` to reference files, paste images, pipe data

### Context Management

- `/clear` between unrelated tasks
- Use subagents for investigation (keeps main context clean)
- `/compact` with instructions when context is large
- After 2 failed corrections, `/clear` and write a better prompt

### Scaling

- `claude -p` for CI/scripts/automation
- Worktrees for parallel sessions
- Fan out with `for file in $(cat list); do claude -p "..." done`
- Writer/Reviewer pattern: one session writes, another reviews

---

## Vault Links

- [[../../.claude/CLAUDE|CLAUDE.md]]
- [[../../.claude/rules/_index|Rules Index]]
- [[../../.claude/skills/_index|Skills Index]]
- [[../../.claude/agents/_registry|Agent Registry]]
