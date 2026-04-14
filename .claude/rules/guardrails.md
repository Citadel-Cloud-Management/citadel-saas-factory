# Guardrails Rules (MANDATORY)

**No LLM output reaches users or downstream agents without passing through the Guardrails validation layer.** This is non-negotiable.

## Core Rules

1. **Mandatory validation** — Every LLM call in `backend/` MUST use `guard_llm_call()` from `app.middleware.guardrails`. Direct LLM client calls are prohibited.

2. **Source grounding required** — All agent responses must be validated against source data or RAG context. Ungrounded responses are rejected.

3. **Hallucination threshold** — Outputs with hallucination confidence scores below **0.85** trigger automatic retry with grounding context injected. After 3 retries, the output is rejected.

4. **Schema enforcement** — All structured outputs must specify a JSON schema. The Guard.from_rail_string() wrapper enforces the schema and rejects malformed responses.

5. **Audit everything** — Every validation — pass, fail, retry, reject — is logged to the immutable audit trail with timestamp, correlation ID, scores, and failed validators.

6. **Fail-closed** — In production, if the guardrails library is unavailable, the system rejects LLM outputs by default. Never silently bypass validation.

## Validators Required

Every LLM call must run through at least:

- `hub://guardrails/hallucination_free` — fabricated fact detection
- `hub://guardrails/provenance_llm` — RAG grounding verification
- `hub://guardrails/toxic_language` — toxic content filter
- `hub://guardrails/detect_pii` — PII masking

## Problem → Solution Matrix

| Problem | Solution |
|---------|----------|
| Model makes things up | Validate against rules and source data |
| No grounding | RAG provenance validators |
| Inconsistent answers | Schema enforcement with deterministic outputs |
| Unsafe agent behavior | Pre/post execution guardrails |

## Enforcement

- **Pre-commit hook** — rejects code that calls LLM clients directly without `guard_llm_call()`
- **Code review** — reviewers must verify guardrails are wired for any LLM integration
- **Runtime** — the guardrails middleware intercepts all LLM traffic; bypass attempts are logged as security events
