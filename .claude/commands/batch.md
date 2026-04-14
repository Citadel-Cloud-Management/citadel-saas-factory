---
description: Run a task across multiple files in parallel
argument-hint: "[glob-pattern] [task-description]"
---

Run a task across multiple files matching **$ARGUMENTS**.

For each matching file:
1. Read the file
2. Apply the requested transformation
3. Verify the result
4. Report progress

Use parallel sub-agents when files are independent to maximize throughput.
