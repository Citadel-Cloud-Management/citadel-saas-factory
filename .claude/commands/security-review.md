---
description: Scan branch diff for security vulnerabilities
---

Run a security review on the current branch diff.

```
!git diff main...HEAD
```

Analyze the diff for:
- Hardcoded secrets, API keys, credentials
- SQL injection via string concatenation
- XSS vectors (unsanitized user input)
- CSRF gaps, missing auth checks
- Unsafe deserialization
- Container security (runAsRoot, privileged)
- Dependency CVEs

Report findings by severity (CRITICAL/HIGH/MEDIUM/LOW) with remediation steps.
