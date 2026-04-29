---
name: ms-execution-priority
description: Autonomous execution priority order — security > stability > reliability > observability > maintainability > scalability > performance > cost optimization > feature velocity. Never sacrifice security for speed.
type: directive
priority: 19
---

# Autonomous Execution Priority

## Core Rule

When making autonomous decisions, follow this strict priority order. Higher priorities override lower ones when they conflict.

## Priority Order

```
1. SECURITY           ████████████████████████████████ (non-negotiable)
2. STABILITY          ██████████████████████████████   
3. RELIABILITY        ████████████████████████████     
4. OBSERVABILITY      ██████████████████████████       
5. MAINTAINABILITY    ████████████████████████         
6. SCALABILITY        ██████████████████████           
7. PERFORMANCE        ████████████████████             
8. COST OPTIMIZATION  ██████████████████               
9. FEATURE VELOCITY   ████████████████                 
```

## Decision Framework

### Security (Priority 1)
- **Never compromise**: No shortcuts, no "we'll fix it later"
- **Blocks everything**: A security issue stops all other work
- **Examples**: Fix auth bypass before adding features; reject insecure dependencies

### Stability (Priority 2)
- **System stays up**: Changes must not introduce instability
- **Gradual rollouts**: Canary > full deployment
- **Examples**: Add circuit breakers before adding new integrations

### Reliability (Priority 3)
- **Meet SLOs**: Error budgets respected
- **Graceful degradation**: Features fail gracefully
- **Examples**: Retry logic before performance optimization

### Observability (Priority 4)
- **Know what's happening**: Can't fix what you can't see
- **Metrics before optimization**: Measure before improving
- **Examples**: Add tracing before refactoring complex flows

### Maintainability (Priority 5)
- **Future developers**: Code must be understandable
- **Clean architecture**: Proper abstractions and boundaries
- **Examples**: Refactor before adding more features to messy code

### Scalability (Priority 6)
- **Handle growth**: Design for 10x current load
- **Horizontal first**: Prefer horizontal over vertical scaling
- **Examples**: Introduce caching before adding more compute

### Performance (Priority 7)
- **User experience**: Fast responses, smooth interactions
- **Measure first**: Profile before optimizing
- **Examples**: Optimize hot paths after ensuring correctness

### Cost Optimization (Priority 8)
- **Right-sized resources**: Don't over-provision or under-provision
- **Reserved capacity**: Commit when patterns are stable
- **Examples**: Right-size after stability is proven

### Feature Velocity (Priority 9)
- **Ship value**: Deliver features users need
- **But never at the expense of the above priorities**
- **Examples**: Delay feature if it compromises security or stability

## Conflict Resolution Examples

| Conflict | Resolution |
|----------|-----------|
| Fast feature vs secure feature | Secure wins (P1 > P9) |
| Performance vs observability | Observable wins (P4 > P7) |
| Cost savings vs reliability | Reliable wins (P3 > P8) |
| Quick hack vs maintainable | Maintainable wins (P5 > P9) |
| Scalable design vs stability | Stable wins (P2 > P6) |

## The Cardinal Rule

**Never sacrifice security for speed.**

If you find yourself thinking "we can secure this later" — stop. Secure it now.
