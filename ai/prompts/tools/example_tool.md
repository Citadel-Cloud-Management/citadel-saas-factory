---
name: web-search-tool
version: "1.0.0"
model: claude-sonnet-4-6
description: Prompt template for invoking the web search tool with structured query parameters.
tool_ref: exa_search
tags: [tool, search, retrieval]
---

## Tool: Web Search

You have access to a web search tool. Use it when the user's question requires information beyond your training data or the knowledge vault.

### Tool Schema

```json
{
  "name": "exa_search",
  "description": "Search the web for current information",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query"
      },
      "num_results": {
        "type": "integer",
        "description": "Number of results to return (1-10)",
        "default": 5
      },
      "type": {
        "type": "string",
        "enum": ["keyword", "neural", "auto"],
        "default": "auto"
      }
    },
    "required": ["query"]
  }
}
```

### When to Use

- The user asks about events, data, or changes after your knowledge cutoff.
- The knowledge vault (`docs/vault/wiki/index.md`) does not contain a relevant answer.
- The user explicitly requests a web search.

### When NOT to Use

- The answer is available in the project codebase or vault.
- The question is about internal architecture or project conventions.
- The answer requires no external data.

### Response Format

After receiving search results, synthesize them into a direct answer. Cite each source with a numbered reference. Do not dump raw search results.
