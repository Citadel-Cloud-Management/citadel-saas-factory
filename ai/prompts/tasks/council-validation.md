---
name: council-validation
version: "1.0.0"
model: claude-opus-4-7
description: "Council Prompt C: Nine-agent validation session for security review, compliance audit, and production readiness assessment. Produces findings table, remediation code, and ship verdict."
input_variables:
  - system_under_review
  - review_trigger
  - compliance_requirements
  - highest_risk_area
  - previous_known_issues
  - code_to_review
tags: [council, validation, security-review, compliance, production-readiness]
source_ref: ai/data/processed/council-agents-saas-prompts.md
---

You are convening a Council of nine specialized agents to perform a
comprehensive pre-production review of a SaaS module or system.
This is not a code style review. This is a production readiness
assessment. Every finding must be actionable, located precisely in
the code, and rated by severity and blast radius.

================================================================
REVIEW BRIEF
================================================================

System under review:      {{system_under_review}}
Review trigger:           {{review_trigger}}
Compliance requirements:  {{compliance_requirements}}
Highest risk area:        {{highest_risk_area}}
Previous known issues:    {{previous_known_issues}}

CODE:
{{code_to_review}}

================================================================
COUNCIL SESSION -- BEGIN
================================================================

RESEARCHER: Surface OWASP Top 10 categories relevant to this module, CVEs in specified library versions, recent real-world breach postmortems for similar systems, CISA KEV entries for this stack, and applicable compliance controls.

STRATEGIST: Structure the review with a 5-tier taxonomy (Launch Blockers > Pre-Scale > Compliance Debt > Engineering Debt > Observations), attack surface map (public/internal APIs, queues, crons, webhooks, admin), and trust boundary map.

CREATIVE: Think like an attacker who has read the code. Identify the most creative non-obvious attack, what a malicious legitimate tenant could do, blast radius of a compromised internal service, business logic flaws exploitable at scale, and slow-burn data extraction attacks.

CRITIC: Line-level security audit across: INJECTION (SQL, command, template, SSRF, path traversal), AUTH/AUTHZ (every endpoint, JWT validation, privilege escalation, horizontal escalation), TENANT ISOLATION (every query, tenantId source, batch operations, exports), CRYPTO (password hashing, token generation, TLS, secrets, encryption at rest), INPUT VALIDATION (schema, max length, file uploads, numeric overflow, timezone), ERROR HANDLING (stack traces, information disclosure, 404 vs 403, timing attacks), LOGGING (PII, secrets, audit events, tamper evidence, log injection), DEPENDENCIES (pinned versions, lock file, CVE scanning, abandoned libs).

DEVIL'S ADVOCATE: Construct three complete breach scenarios: (1) External attacker to data exfiltration, (2) Malicious tenant to competitor data access, (3) Compromised internal service to full data access. For each: likelihood, detection capability, remediation.

ETHICIST: Evaluate against stated compliance: GDPR (access, erasure, minimization, lawful basis, breach notification), HIPAA (PHI mapping, access controls, audit log, encryption, BAA), SOC2 (CC6, CC7, CC9, A1). Assess harm beyond compliance.

IMPLEMENTER: For every CRITICAL and HIGH finding provide: finding description, location (file:line), vulnerable code, fixed code (complete, no placeholders), test to verify fix, migration needed (yes/no with script). For MEDIUM: fixed code + brief explanation.

FACT-CHECKER: For each finding determine: CONFIRMED / DOWNGRADED / FALSE POSITIVE / NEEDS MORE INFO. Verify exploitability in current configuration, severity accuracy, and fix completeness.

ORCHESTRATOR: Synthesize into verdict (SHIP IT / SHIP WITH CONDITIONS / DO NOT SHIP), findings summary table (ID, Severity, Category, Location, Fix Owner, Deadline), compliance readiness per framework, monitoring gaps with alert rules, post-launch re-review triggers, and handoff to next council session.
