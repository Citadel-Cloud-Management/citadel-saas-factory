# Council Parallel Fix Session

Convene a Council of 9 specialized agents for simultaneous multi-front remediation across all findings.

## Instructions

1. Load the Council skill: `.claude/skills/council/SKILL.md`
2. Load the full Prompt D template from: `docs/vault/raw/council-agents-saas-prompts.md` (lines 1057-1660)
3. If the user has not provided a parallel fix brief, prompt them to fill in:
   - System under remediation (name, codebase size, language, test baseline, CI, deployment, rollback)
   - Findings input (paste complete findings table from Validation Session)
   - Current codebase (paste all files)
   - Constraints on fixes (no-go zones, dependency freeze, style contract, API surface freeze, coverage floor, deploy window)
4. Execute 3 phases:
   - **Phase 0 — Pre-Work**: Researcher maps dependencies, Strategist designs workstreams, defines interface contracts
   - **Phase 1 — Parallel Execution**: Implementer runs multiple parallel workstreams simultaneously
   - **Phase 2 — Integration**: Critic audits merge conflicts, Devil's Advocate finds regressions, Fact-Checker verifies fixes
   - **Phase 3 — Deployment**: Orchestrator manages merge sequence, deployment protocol, monitoring
5. Enforce the Three Laws:
   - Contracts Before Code
   - Own Your Files, Borrow Nothing
   - Devil's Advocate Is Always Right Until Proven Wrong
6. Output: Workstream diffs, merge sequence, deployment protocol, final findings closure table
7. File results to `docs/vault/wiki/council/` for cross-session persistence

## When to collapse to serial

- Fewer than 5 findings: run single Implementer session
- All findings in a single file
- Hotfix required within 2 hours

## Usage

```
/council-fix
```

Then paste your findings table and complete codebase when prompted.
