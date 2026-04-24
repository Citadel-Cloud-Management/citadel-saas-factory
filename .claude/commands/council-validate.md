# Council Validation Session

Convene a Council of 9 specialized agents for security review, compliance audit, and production readiness.

## Instructions

1. Load the Council skill: `.claude/skills/council/SKILL.md`
2. Load the full Prompt C template from: `docs/vault/raw/council-agents-saas-prompts.md` (lines 720-1003)
3. If the user has not provided a review brief, prompt them to fill in:
   - System under review (module name + context)
   - Review trigger (pre-launch / post-incident / compliance audit / etc.)
   - Compliance requirements (HIPAA / SOC2 / GDPR / PCI-DSS / none)
   - Highest risk area
   - Previous known issues
   - Full code (all files in the module)
4. Run each agent in sequence: Researcher -> Strategist -> Creative -> Critic -> Devil's Advocate -> Ethicist -> Implementer -> Fact-Checker -> Orchestrator
5. Critic performs exhaustive line-level security audit across: injection, auth, tenant isolation, crypto, input validation, error handling, logging, dependencies
6. Devil's Advocate constructs 3 breach scenarios (external attacker, malicious tenant, compromised internal service)
7. Implementer provides complete remediation code for every CRITICAL and HIGH finding
8. Output: Ship verdict (SHIP IT / SHIP WITH CONDITIONS / DO NOT SHIP), findings table, compliance readiness, monitoring gaps
9. File results to `docs/vault/wiki/council/` for cross-session persistence

## Usage

```
/council-validate
```

Then paste your review brief and complete module code when prompted.
