# Council Implementation Session

Convene a Council of 9 specialized agents for module-level code generation, testing, and security.

## Instructions

1. Load the Council skill: `.claude/skills/council/SKILL.md`
2. Load the full Prompt B template from: `docs/vault/raw/council-agents-saas-prompts.md` (lines 362-715)
3. If the user has not provided a filled module brief, prompt them to fill in:
   - Module Identity (name, system role, owner)
   - Technical Contract (language, framework, database, auth, deployment)
   - Functional Specification (purpose, triggers, inputs, outputs, state changes, events)
   - Business Rules (complete list — becomes the test matrix)
   - Dependencies (internal, external, database, cache)
   - Security Invariants (non-negotiable constraints)
   - Architecture Context (paste from Architecture Session output)
4. Run each agent in sequence: Researcher -> Strategist -> Creative -> Critic -> Devil's Advocate -> Ethicist -> Implementer -> Fact-Checker -> Orchestrator
5. Implementer must produce COMPLETE code — no placeholders, no TODOs, every function complete
6. Code standards enforced: clean architecture, typed exceptions, security guards, observability, idempotency
7. Output: Complete module code, test suite, deployment checklist, follow-on module brief
8. File results to `docs/vault/wiki/council/` for cross-session persistence

## Usage

```
/council-implement
```

Then paste your module brief and architecture context when prompted.
