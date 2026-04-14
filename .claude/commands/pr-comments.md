---
description: Fetch and respond to GitHub PR comments
argument-hint: "[pr-number]"
---

Fetch comments on PR **#$ARGUMENTS**:

```
!gh pr view $ARGUMENTS --comments
```

Review each comment, draft responses, and apply code changes where requested. Follow the project's code review conventions.
