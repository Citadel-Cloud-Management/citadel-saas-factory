# Lessons Learned

> Append-only log. After every correction, failed assumption, or discovered root cause, add an entry.

## Format

```
### [YYYY-MM-DD] <title>
- **Root cause:** What actually went wrong
- **Failure pattern:** The category of mistake
- **Corrective action:** What was done to fix it
- **Prevention rule:** How to avoid this in the future
- **Automation opportunity:** Can this be caught automatically?
```

---

### [2026-05-10] Agent count mismatch across README, CLAUDE.md, and registry

- **Root cause:** README was updated with inflated agent counts (430+) without updating the registry or expanding agent definitions. The domain table summed to 416, the registry had 265, and the expandable sections listed even fewer.
- **Failure pattern:** Documentation drift — numbers updated in one place without verifying against source of truth.
- **Corrective action:** Corrected README to 416+ (matching domain table sum). Fixed expandable section headers to match actual listed agents. Flagged 265 vs 416 discrepancy as known gap.
- **Prevention rule:** Always verify counts against `_registry.yaml` before updating README. The registry is the source of truth for agent counts.
- **Automation opportunity:** CI check that sums domain table counts and compares to README headline number.
