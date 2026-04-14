---
description: Structured debugging workflow for bugs and failures
argument-hint: "[issue-description-or-error]"
---

Debug: **$ARGUMENTS**

## Debugging Protocol
1. **Reproduce** — Get a reliable reproduction
2. **Isolate** — Narrow down to the smallest failing case
3. **Hypothesize** — Form a testable theory about the root cause
4. **Verify** — Add logging, run tests, check assumptions
5. **Fix** — Minimal change that addresses the root cause
6. **Prevent** — Add a regression test

Do NOT guess blindly. Do NOT apply fixes without verifying the root cause first.
