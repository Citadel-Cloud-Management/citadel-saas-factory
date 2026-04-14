---
description: Simplify and refactor code while preserving functionality
argument-hint: "[file-or-directory]"
---

Simplify **$ARGUMENTS** for clarity, consistency, and maintainability.

Focus on:
- Removing dead code and unused imports
- Collapsing duplicated logic
- Clarifying variable and function names
- Reducing nesting depth
- Extracting magic numbers into named constants
- Replacing imperative loops with declarative transforms where it improves readability

**Rules**:
- Preserve all functionality exactly
- Do not change public API signatures without explicit approval
- Run tests after every change to verify behavior
