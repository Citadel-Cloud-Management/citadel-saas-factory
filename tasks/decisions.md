# Architecture Decisions

> Log of significant decisions made during development. Each entry captures context, rationale, trade-offs, and outcome.

## Format

```
### [YYYY-MM-DD] <decision title>
- **Context:** What situation prompted this decision
- **Decision:** What was decided
- **Rationale:** Why this option was chosen
- **Trade-offs:** What was given up
- **Outcome:** Result (update later if needed)
```

---

### [2026-05-10] Redesign CLAUDE.md from project overview to enterprise orchestration file

- **Context:** Original CLAUDE.md was a static project overview (architecture table, agent counts, toolchain list). It provided context but no operational guidance for how Claude should behave as a production engineering agent.
- **Decision:** Merged project context with enterprise engineering standards: plan-first workflow, multi-agent delegation strategy, self-improvement loop, verification gates, autonomous debugging, and known-gaps tracking.
- **Rationale:** The CLAUDE.md is the primary instruction file for every Claude session. It must define behavior, not just describe the project. A Staff+ engineer needs orchestration rules, not a README.
- **Trade-offs:** Longer file (was 85 lines, now ~200). But every section is actionable — no filler.
- **Outcome:** CLAUDE.md now enforces planning, delegation, verification, and self-improvement across all sessions.
