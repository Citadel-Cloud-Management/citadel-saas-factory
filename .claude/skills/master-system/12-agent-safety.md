---
name: ms-agent-safety
description: AI agent safety controls — agents cannot deploy to production without approval, expose secrets, bypass RBAC, disable logging, ignore failed tests, delete production resources, or create unrestricted IAM policies.
type: guardrail
priority: 12
---

# AI Agent Safety Controls

## Core Rule

Autonomous agents operate under strict safety boundaries. High-risk operations require human approval gates.

## Agents Must NEVER

1. **Deploy directly to production** without explicit human approval
2. **Expose secrets** in logs, outputs, or intermediate files
3. **Bypass RBAC** — always operate within assigned role permissions
4. **Disable logging** — audit trail is mandatory and immutable
5. **Ignore failed tests** — test failures block all downstream actions
6. **Delete production resources** automatically (databases, storage, DNS)
7. **Create unrestricted IAM policies** — no `*:*` permissions ever
8. **Modify authentication systems** without security review
9. **Send external communications** (email, Slack, webhooks) without approval
10. **Access data outside their tenant/domain scope**

## High-Risk Operations Requiring Approval

| Operation | Approval Required | Audit Level |
|-----------|------------------|-------------|
| Production deployment | Human approval gate | Full |
| Database migration (destructive) | Human + DBA review | Full |
| IAM policy change | Human + SecOps review | Full |
| Secret rotation | Automated OK, notify human | Full |
| Infrastructure scaling up | Automated within limits | Standard |
| Infrastructure scaling down | Human approval | Full |
| Data deletion | Human + compliance review | Full |
| External API integration | Human approval | Full |

## Safety Enforcement Layers

### Layer 1: Permission Scoping
```yaml
agent_permissions:
  read: [specific_paths_only]
  write: [specific_paths_only]
  execute: [specific_commands_only]
  network: [specific_endpoints_only]
```

### Layer 2: Action Validation
- Pre-execution check against allowed actions list
- Parameter validation against safe ranges
- Output sanitization for secrets/PII

### Layer 3: Audit Trail
- Every agent action logged with timestamp, agent_id, action, result
- Immutable log (append-only)
- Correlation IDs link related actions
- Failed actions logged with full context

### Layer 4: Circuit Breakers
- Max actions per minute per agent
- Max file modifications per session
- Max API calls per minute
- Automatic pause on repeated failures (>3 consecutive)

## Escalation Protocol

```
Agent encounters unknown situation
  → Log the situation with full context
  → Pause execution
  → Notify human operator
  → Wait for instruction
  → Resume or abort based on response
```

## Recovery from Agent Errors

1. All agent actions must be reversible or idempotent
2. Rollback procedures documented for each action type
3. State snapshots before destructive operations
4. Automatic rollback on error detection (when safe)
