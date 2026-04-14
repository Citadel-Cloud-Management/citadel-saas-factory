---
description: Run guardrails validation against LLM outputs or files
argument-hint: "[file-or-directory]"
---

Run the Guardrails AI validation layer against **$ARGUMENTS**.

## Validation Pipeline
1. **Schema check** — Structured output enforcement
2. **Hallucination score** — Threshold 0.85
3. **Factuality check** — Against source data / RAG context
4. **Provenance verification** — RAG grounding validators
5. **PII / toxicity filters**

## Hub Validators
- `hub://guardrails/hallucination_free`
- `hub://guardrails/provenance_llm`
- `hub://guardrails/toxic_language`
- `hub://guardrails/detect_pii`

Report pass/fail status with scores and failed validators. Log every result to the immutable audit trail.
