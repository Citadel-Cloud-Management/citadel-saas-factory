# Anti-Patterns

> Patterns that have caused failures or wasted effort. Consult before starting work to avoid repeating mistakes.

## Format

```
### <anti-pattern name>
- **What it looks like:** How to recognize this pattern
- **Why it fails:** The root cause of failure
- **What to do instead:** The correct approach
```

---

### Inflating counts without expanding definitions

- **What it looks like:** Updating README/CLAUDE.md headline numbers (e.g., "385+ agents" to "430+ agents") without adding corresponding agent definitions to the registry or expanding detail tables.
- **Why it fails:** Creates documentation debt. Readers expect to find 430 agents but discover only 265 in the registry and 52 in the detail tables. Erodes trust in all project claims.
- **What to do instead:** The registry (`_registry.yaml`) is the source of truth. Update the registry first, then update all references atomically. If agents don't exist yet, use the actual count with a clear roadmap for expansion.

### Declaring TDD mandatory without writing tests

- **What it looks like:** Multiple rule files mandate "80% minimum coverage" and "TDD workflow: RED → GREEN → IMPROVE" but `backend/tests/` is empty and `backbone/` has no test files.
- **Why it fails:** Rules without enforcement are aspirational, not operational. New contributors see the mandate, check the test directory, and conclude the rules aren't real.
- **What to do instead:** Write the first test before writing the first rule about testing. Seed `backend/tests/` with at least one test per module. Add a CI gate that fails on coverage below threshold.

### Configuration-heavy, implementation-light

- **What it looks like:** 440 markdown files, 125 YAML configs, 40 commands, 21 rules, 18 templates — but minimal application code. Security configs for Falco, Kyverno, OPA that have never been deployed.
- **Why it fails:** Configuration without implementation creates the illusion of maturity. The system looks enterprise-grade on paper but can't serve a single HTTP request in production.
- **What to do instead:** Implement one vertical slice end-to-end (API endpoint + database + frontend page + test + deployment) before expanding the configuration surface. Prove the architecture works, then document it.
