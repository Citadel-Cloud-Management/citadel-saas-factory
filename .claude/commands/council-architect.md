# Council Architecture Session

Convene a Council of 9 specialized agents for system design, infrastructure, and strategic foundation.

## Instructions

1. Load the Council skill: `.claude/skills/council/SKILL.md`
2. Load the full Prompt A template from: `docs/vault/raw/council-agents-saas-prompts.md` (lines 26-357)
3. If the user has not provided a filled product brief, prompt them to fill in:
   - Product Identity (name, core problem, personas, business model)
   - Customer Profile (segment, deal size, compliance, data sensitivity)
   - Technical Context (cloud, regions, team size, existing stack)
   - Scale Requirements (launch users, 6mo/18mo targets, peak load, data volume)
   - Core Feature Modules
   - Integration Surface (SSO, third-party APIs, webhooks, data export)
   - Business Constraints (timeline, budget, must-haves, deferred features)
4. Run each agent in sequence: Researcher -> Strategist -> Creative -> Critic -> Devil's Advocate -> Ethicist -> Implementer -> Fact-Checker -> Orchestrator
5. Each agent must:
   - State their role and lens
   - Deliver full analysis (no summaries)
   - Identify 2-3 things other agents will miss
6. Output: ADR (10 key decisions), Risk Register (top 5), 90-Day Execution Summary
7. File results to `docs/vault/wiki/council/` for cross-session persistence

## Usage

```
/council-architect
```

Then paste or fill in your product brief when prompted.
