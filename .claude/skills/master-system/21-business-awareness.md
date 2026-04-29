---
name: ms-business-awareness
description: Business awareness for technical decisions — ROI, operational cost, vendor lock-in, scalability cost, licensing, maintenance burden, staffing complexity, support implications, monetization, analytics, onboarding.
type: framework
priority: 21
---

# Business Awareness

## Core Rule

Every technical decision has business implications. Consider ROI, total cost of ownership, and organizational impact alongside technical merit.

## Decision Dimensions

### Return on Investment (ROI)
- What is the expected revenue/savings from this investment?
- What is the time-to-value?
- What is the payback period?
- Are there compounding benefits over time?

### Operational Cost
- Monthly/annual infrastructure cost
- Third-party service fees
- Data transfer and storage costs
- Support and maintenance labor

### Vendor Lock-in Assessment
```
LOW RISK:    Open standards, portable data, commodity services
MEDIUM RISK: Proprietary APIs with alternatives, data export available
HIGH RISK:   Proprietary formats, no export, deep integration dependency
```

### Scalability Cost Model
| Scale | Users | Monthly Cost | Cost/User |
|-------|-------|-------------|-----------|
| Seed | 100 | $50 | $0.50 |
| Growth | 10K | $500 | $0.05 |
| Scale | 100K | $5,000 | $0.05 |
| Enterprise | 1M | $30,000 | $0.03 |

### Licensing Considerations
- MIT/Apache: Safe for commercial use
- GPL/AGPL: Copyleft obligations — evaluate carefully
- BSL/SSPL: Source-available, not open source — vendor lock-in risk
- Proprietary: Total cost of ownership includes renewal risk

### Maintenance Burden
- How many engineers needed to maintain?
- Is the technology well-staffed in the job market?
- Complexity of upgrades and version migrations?
- Quality of documentation and community support?

### Staffing Complexity
- Can current team maintain this?
- Does it require specialized hiring?
- Training cost for existing team?
- On-call burden?

### Support Implications
- What's the support SLA requirement?
- Self-hosted vs managed (support ownership)?
- Incident response complexity?
- Customer-facing documentation needed?

## Monetization Awareness

When building features, consider:
- **Free tier limits** — what drives upgrades?
- **Usage metering** — what to charge for?
- **Feature gating** — starter vs pro vs enterprise
- **Seat-based pricing** — per-user costs and scaling
- **Value metrics** — align pricing with customer value

## Analytics Requirements

Every feature should answer:
- How many users use this?
- What's the conversion funnel?
- Where do users drop off?
- What's the feature's impact on retention?
- What's the revenue attribution?

## Build vs Buy Decision Matrix

| Factor | Build | Buy |
|--------|-------|-----|
| Core differentiator | YES | Probably not |
| Commodity capability | Rarely | YES |
| Team has expertise | Consider | — |
| Time-to-market critical | — | YES |
| Long-term cost lower | Consider | — |
| Customization needed | YES | Depends on API |

## Cost-Aware Architecture Patterns

- Use serverless for spiky, unpredictable workloads
- Use reserved instances for steady-state workloads
- Implement caching to reduce compute and DB costs
- Use CDNs to reduce bandwidth costs
- Archive cold data to cheaper storage tiers
- Right-size containers (don't over-provision)
- Use spot/preemptible instances for fault-tolerant workloads
