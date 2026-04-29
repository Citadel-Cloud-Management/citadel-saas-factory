---
name: ms-failure-handling
description: Failure handling patterns — retry with exponential backoff, timeout handling, circuit breakers, graceful degradation, fallback logic, dead-letter queues, rollback procedures.
type: standard
priority: 20
---

# Failure Handling

## Core Rule

Always include comprehensive failure handling. Systems must degrade gracefully, recover automatically where possible, and provide clear visibility into failures.

## Required Patterns

### 1. Retry Strategy
```yaml
retry:
  max_attempts: 3
  backoff: exponential
  base_delay: 100ms
  max_delay: 10s
  jitter: true  # Prevents thundering herd
  retryable_errors:
    - 429  # Rate limited
    - 500  # Server error
    - 502  # Bad gateway
    - 503  # Service unavailable
    - 504  # Gateway timeout
  non_retryable_errors:
    - 400  # Bad request (fix the request)
    - 401  # Unauthorized (re-auth needed)
    - 403  # Forbidden (permission issue)
    - 404  # Not found (resource doesn't exist)
```

### 2. Timeout Handling
```yaml
timeouts:
  connect: 5s        # TCP connection establishment
  read: 30s          # Response read timeout
  write: 30s         # Request write timeout
  idle: 60s          # Keep-alive idle timeout
  total: 60s         # Total request timeout

rules:
  - Always set timeouts (never infinite)
  - Timeout < caller's timeout (cascade protection)
  - Log timeout events with context
  - Track timeout rates as metrics
```

### 3. Circuit Breakers
```yaml
circuit_breaker:
  failure_threshold: 5        # Failures to open
  success_threshold: 3        # Successes to close
  timeout: 30s                # Time in open state before half-open
  half_open_max_calls: 3      # Calls allowed in half-open

states:
  closed: Normal operation, failures counted
  open: Requests fail immediately (fast-fail)
  half_open: Limited requests to test recovery
```

### 4. Graceful Degradation
```yaml
degradation_levels:
  L0_full_service: All features operational
  L1_non_critical_disabled: Recommendations, analytics disabled
  L2_reduced_functionality: Read-only mode, cached responses
  L3_emergency: Static fallback page, queue writes for later

triggers:
  - Error rate > 5% → L1
  - Error rate > 20% → L2
  - Critical dependency down → L2 or L3
  - Database unreachable → L3
```

### 5. Fallback Logic
```yaml
fallback_chain:
  primary: Live database query
  secondary: Redis cache (stale OK)
  tertiary: Local cache / static default
  final: Informative error message

rules:
  - Fallback data must be clearly marked (stale, cached, default)
  - Log when fallback is activated
  - Alert on sustained fallback usage
  - Never silently serve stale data as fresh
```

### 6. Dead-Letter Queues
```yaml
dlq:
  retention: 14_days
  max_retries_before_dlq: 3
  alert_threshold: 100_messages
  
  handling:
    - Automatic retry after fix deployed
    - Manual inspection dashboard
    - Replay capability (idempotent consumers)
    - Poison message isolation
```

### 7. Rollback Procedures
```yaml
rollback:
  automated_triggers:
    - Error rate > 5% for > 2 minutes
    - p95 latency > 2x baseline for > 5 minutes
    - Health check failures > 3 consecutive

  manual_procedure:
    1. Identify the failing deployment
    2. Trigger rollback (ArgoCD/kubectl)
    3. Verify rollback health
    4. Notify team
    5. Create incident if needed

  database_rollback:
    - Forward-only migrations preferred
    - Backward-compatible schema changes
    - Feature flags to disable new code paths
    - Data backfill scripts for emergency revert
```

## Implementation Checklist

```
[ ] All HTTP clients have timeouts configured
[ ] All external calls have retry logic
[ ] Circuit breakers on all external dependencies
[ ] Graceful degradation levels defined
[ ] Fallback responses for critical paths
[ ] Dead-letter queues for async processing
[ ] Automated rollback triggers configured
[ ] Failure scenarios documented in runbooks
```
