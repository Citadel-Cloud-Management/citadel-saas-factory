---
name: summarize-document
version: "1.0.0"
model: claude-sonnet-4-6
description: Summarize a document into structured key points with citations.
input_variables:
  - document_text
  - max_points
  - output_format
tags: [task, summarization, content]
---

## Task: Document Summarization

Summarize the following document into a structured list of key points.

### Input

**Document:**
{{document_text}}

**Max Points:** {{max_points}}

**Output Format:** {{output_format}}

### Instructions

1. Read the full document carefully.
2. Identify the {{max_points}} most important claims, decisions, or facts.
3. For each point:
   - State the claim in one sentence.
   - Cite the source section or paragraph number.
   - Rate confidence: HIGH / MEDIUM / LOW.
4. Return the result in {{output_format}} format (json | markdown | plain).

### Output Schema (if json)

```json
{
  "summary": [
    {
      "point": "string",
      "source_ref": "string",
      "confidence": "HIGH | MEDIUM | LOW"
    }
  ],
  "total_points": "number",
  "document_length_chars": "number"
}
```
