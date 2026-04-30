# Auto-Update Preamble — Injected at Every Skill Launch

> This prompt is prepended to every agent and skill invocation to ensure context alignment,
> state awareness, and continuous improvement across all 500+ agents.

---

## MANDATORY CONTEXT LOAD

Before executing any task, you MUST:

1. **Read `context.md`** at the repository root — this is the canonical source of truth for all architecture, standards, conventions, security rules, and agent governance.

2. **Read the relevant `CLAUDE.md`** for your working directory — root for project-wide context, `backend/CLAUDE.md` for backend work, `frontend/CLAUDE.md` for frontend work.

3. **Check `docs/vault/wiki/index.md`** before grepping raw sources — the compiled wiki answers most factual questions faster than codebase search.

4. **Check `.claude/rules/`** for the specific coding standard that applies to your task domain (security, testing, api-design, database, frontend, etc.).

## STATE AWARENESS

Before making changes:

1. **Run `git status`** — understand the current branch, uncommitted changes, and working state.
2. **Check for in-progress work** — read any open TODO lists, task trackers, or plan documents in the conversation.
3. **Verify file existence** before modifying — use `Read` before `Edit`, never assume a file's contents.
4. **Check model routing** — read `models/routing.yaml` to understand which model tier applies to your task.

## EXECUTION STANDARDS

Every agent invocation MUST follow:

### Quality Gates
- **Immutability**: create new objects, never mutate existing ones
- **Small files**: 200-400 lines typical, 800 max
- **Small functions**: under 50 lines, single responsibility
- **Type hints**: required for all Python and TypeScript code
- **Error handling**: handle at every level, never swallow silently

### Security Gates
- **No hardcoded secrets** — use environment variables or Vault
- **Validate all input** at system boundaries
- **Parameterized queries only** — no SQL string concatenation
- **All LLM output** must pass through guardrails validation

### Testing Gates
- **TDD mandatory**: write tests first (RED), implement (GREEN), refactor (IMPROVE)
- **80% minimum** code coverage
- **Mock external services, not internal modules**

### Git Gates
- **Conventional commits**: feat, fix, refactor, docs, test, chore, perf, ci
- **No force push** to main/production
- **PR required** for all changes

## POST-EXECUTION CHECKLIST

After completing your task:

1. **Verify your changes compile/lint** — run `make lint` or equivalent
2. **Run relevant tests** — run `make test` or targeted test command
3. **Check for regressions** — verify existing functionality still works
4. **Update documentation** if you changed behavior, APIs, or architecture
5. **Update `context.md`** if you changed something documented there (stack, commands, architecture)
6. **Report blockers** — if you encountered issues you couldn't resolve, document them clearly

## CONTINUOUS IMPROVEMENT

After each task, evaluate:

- Did I find information that should be in the wiki but wasn't? → Offer to file it
- Did I encounter a pattern that should be a rule? → Propose it for `.claude/rules/`
- Did I build something reusable? → Consider extracting to `.claude/skills/` or `.claude/templates/`
- Did I discover a security issue? → Flag immediately, do not continue until resolved
- Did I notice stale documentation? → Update it or flag for update

## AGENT COORDINATION

When working alongside other agents:

- **Check for file conflicts** — don't modify files another agent is actively changing
- **Use the backbone router** — check `.claude/agents/_registry.yaml` for specialized agents that should handle subtasks
- **Delegate research to subagents** — keep the main context clean
- **Log decisions** — append significant decisions to `.claude/memory/architecture-decisions.md`

## FAILURE PROTOCOL

If you encounter an error:

1. **Diagnose before retrying** — read the error, check assumptions, understand root cause
2. **Fix incrementally** — make one change at a time, verify after each
3. **Escalate if stuck** — ask the user after 3 failed attempts, not as a first response
4. **Never bypass safety** — don't skip tests, linting, or security checks to "make it work"
5. **Document the failure** — if it's a novel error pattern, log it to `.claude/memory/error-patterns.md`
