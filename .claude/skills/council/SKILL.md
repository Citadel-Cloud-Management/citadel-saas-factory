---
name: council
description: Multi-agent Council framework for adversarial SaaS system design, implementation, validation, and parallel remediation. Convenes 9 specialized agents (Researcher, Strategist, Creative, Critic, Devil's Advocate, Ethicist, Implementer, Fact-Checker, Orchestrator) for structured adversarial review.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Agent, WebFetch, WebSearch]
---

# Council Framework — Multi-Agent SaaS Prompt System

> Structured adversarial review that ends in synthesized, actionable, opinionated recommendations.
> Inspired by Hermes Agent (NousResearch) delegation patterns and skill-based procedural memory.

## When to Invoke

- `/council-architect` — System design, infrastructure, strategic foundation (Prompt A)
- `/council-implement` — Module-level code generation, testing, security (Prompt B)
- `/council-validate` — Security review, compliance audit, production readiness (Prompt C)
- `/council-fix` — Parallel multi-front remediation across all findings (Prompt D)
- When user says "run the council", "council session", "adversarial review"
- When designing a new SaaS module or service from scratch
- When reviewing code for production readiness
- When remediating multiple security/quality findings simultaneously

## Agent Roster

| Agent | Symbol | Primary Function | What They Catch |
|---|---|---|---|
| Researcher | R | Surfaces context, facts, precedents | Missing domain knowledge, wrong assumptions |
| Strategist | S | Structures plans and sequencing | Unclear priorities, wrong build order |
| Creative | C | Generates novel approaches | Over-engineering, tunnel vision |
| Critic | X | Challenges every assumption | Fragile logic, hidden dependencies |
| Devil's Advocate | D | Argues hardest against consensus | Groupthink, false confidence |
| Ethicist | E | Evaluates moral and unintended consequences | Privacy violations, unfair outcomes |
| Implementer | I | Translates ideas into executable steps | Vague plans, missing concrete details |
| Fact-Checker | F | Verifies accuracy, flags overconfidence | Outdated patterns, wrong library versions |
| Orchestrator | O | Synthesizes all agents into final recommendation | Contradiction, lack of closure |

## Session Pipeline

```
Architecture Session (Prompt A)
  -> Produces: ADR, phased roadmap, component map, risk register

Implementation Session (Prompt B) x N modules
  -> Input: paste relevant ADR sections + module spec
  -> Produces: complete code, test suite, deployment checklist

Validation Session (Prompt C)
  -> Input: paste complete module code
  -> Produces: security findings, remediation code, ship verdict

Parallel Fix Session (Prompt D)
  -> Input: paste findings table from Validation Session
  -> Produces: coordinated parallel workstream fixes, merge sequence
```

## Integration with Citadel Agent Fleet

The Council framework integrates with the existing 500+ agent system:

- **Researcher agent** maps to `data-analytics/` domain agents
- **Strategist agent** maps to `executive/` domain agents (CEO Strategist, CTO)
- **Critic + Devil's Advocate** map to `security/` and `qa-testing/` agents
- **Implementer** maps to `engineering/` and `frontend/` agents
- **Ethicist** maps to `legal/` and `compliance/` agents
- **Fact-Checker** maps to `qa-testing/` agents
- **Orchestrator** maps to backbone orchestrator

## Hermes Agent Patterns Used

Reference: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)

- **Skill-based procedural memory**: Council sessions produce skills that compound across sessions
- **Delegation pattern**: Spawn isolated subagents for parallel workstreams (Prompt D)
- **Cross-session recall**: Findings, ADRs, and verdicts persist in LLM Wiki
- **Interface contracts**: Pre-agreed function signatures before parallel execution
- **Self-improving loop**: Each Council session refines patterns for the next

## Three Laws of Parallel Fixes (Prompt D)

1. **Contracts Before Code** — No workstream writes implementation until all interface contracts are specified
2. **Own Your Files. Borrow Nothing.** — Each workstream has defined files it may modify; no cross-ownership
3. **Devil's Advocate Is Always Right Until Proven Wrong** — Burden of proof is on the fix author

## Escalation Protocol

- If Devil's Advocate raises an unrefuted concern: **STOP. Treat as blocker.**
- If Ethicist raises a harm under business pressure: **Document in ADR. Make trade-off visible.**
- If Fact-Checker rates a recommendation LOW confidence: **Do not build on it. Spike separately.**

## Output Format

Each Council session produces:
1. **Per-agent analysis** — Full depth, not summaries
2. **Orchestrator synthesis** — Definitive decision with authority
3. **ADR** — Architecture Decision Records for key decisions
4. **Risk Register** — Top 5 risks with probability, impact, trigger, mitigation
5. **Execution Summary** — Week-by-week deliverables

## Raw Source

Full prompt templates: `docs/vault/raw/council-agents-saas-prompts.md`

## Vault Links

- [[../../docs/vault/raw/council-agents-saas-prompts|Council Prompts Source]]
- [[../agent-workflow-designer/SKILL|Agent Workflow Designer]]
- [[../code-review/SKILL|Code Review Skill]]
- [[../security-audit/SKILL|Security Audit Skill]]
- [[../guardrails/SKILL|Guardrails Skill]]
- [[../llm-wiki/SKILL|LLM Wiki Skill]]
- [[../../.claude/agents/engineering/_index|Engineering Agents]]
- [[../../.claude/agents/security/_index|Security Agents]]
