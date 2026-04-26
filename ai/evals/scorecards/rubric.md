---
name: citadel-eval-rubric
version: "1.0.0"
description: Scoring rubric for evaluating AI agent outputs across accuracy, format, tool usage, and latency.
---

# Evaluation Rubric

## Scoring Dimensions

### 1. Accuracy (0-10)

| Score | Criteria |
|-------|----------|
| 10 | All claims correct, fully grounded in source data, no hallucinations |
| 7-9 | Minor omissions but no factual errors |
| 4-6 | Some correct claims mixed with unsupported statements |
| 1-3 | Majority of claims unsupported or incorrect |
| 0 | Completely fabricated or irrelevant output |

**Pass threshold:** >= 7

### 2. Format Compliance (0-10)

| Score | Criteria |
|-------|----------|
| 10 | Output matches schema exactly, valid JSON/markdown, all fields present |
| 7-9 | Valid structure with minor formatting issues (extra whitespace, optional fields missing) |
| 4-6 | Parseable but deviates from schema (wrong field names, missing required fields) |
| 1-3 | Partially structured but not machine-parseable |
| 0 | Unstructured text when structured output was required |

**Pass threshold:** >= 8

### 3. Tool Usage (0-10)

| Score | Criteria |
|-------|----------|
| 10 | Correct tool selected, valid parameters, results properly synthesized |
| 7-9 | Correct tool with minor parameter issues, results adequately used |
| 4-6 | Right tool but wrong parameters, or results poorly integrated |
| 1-3 | Wrong tool selected, or tool called unnecessarily |
| 0 | Tool not called when required, or hallucinated tool call |

**Pass threshold:** >= 7

### 4. Latency Budget (0-10)

| Score | Criteria |
|-------|----------|
| 10 | Response within 50% of budget |
| 7-9 | Response within 75% of budget |
| 4-6 | Response within budget but close to limit |
| 1-3 | Response exceeds budget by up to 2x |
| 0 | Response exceeds budget by more than 2x or times out |

**Pass threshold:** >= 6

## Composite Score

```
composite = (accuracy * 0.40) + (format * 0.25) + (tool_use * 0.20) + (latency * 0.15)
```

**Overall pass threshold:** >= 7.0 (maps to `eval_threshold: 0.85` when normalized to 0-1 via score/8.24)

## Failure Actions

| Composite | Action |
|-----------|--------|
| >= 7.0 | PASS — log and proceed |
| 5.0-6.9 | WARN — log, flag for review, allow with caveat |
| < 5.0 | FAIL — reject output, retry with grounding context, escalate after 3 failures |
