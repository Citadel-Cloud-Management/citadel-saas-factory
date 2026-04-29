---
name: ms-saas-business
description: Autonomous SaaS business mode — onboarding flows, CRM, subscriptions, analytics, email automation, support, admin dashboards, feature flags, A/B testing, affiliates, referrals, SEO, AI agents, knowledge bases.
type: framework
priority: 24
---

# Autonomous SaaS Business Mode

## Core Rule

When building SaaS businesses, automatically include all business-critical systems. No SaaS launches without these capabilities.

## Required Business Systems

### 1. Onboarding Flows
```
- Progressive disclosure (don't overwhelm new users)
- Guided setup wizard (3-5 steps max)
- Template selection (get to value fast)
- Welcome email sequence (3-5 emails over 7 days)
- In-app tooltips and tours (Intercom/Chameleon pattern)
- Activation metric tracking (time-to-first-value)
```

### 2. CRM Integration
```
- Contact lifecycle tracking (lead → trial → customer → churned)
- Activity logging (page views, feature usage, support tickets)
- Lead scoring (engagement-based)
- Pipeline management (trial → paid conversion)
- Integration: HubSpot, Salesforce, or custom
```

### 3. Subscription Billing
```
- Plan tiers (free, starter, pro, enterprise)
- Usage-based pricing support
- Trial management (14-day default)
- Proration on plan changes
- Dunning management (failed payment recovery)
- Invoice generation
- Integration: Stripe, Paddle, or Chargebee
```

### 4. Customer Analytics
```
- Event tracking (signup, activation, feature use, churn)
- Cohort analysis (by signup date, plan, source)
- Funnel visualization (signup → activation → retention)
- Feature adoption metrics
- Revenue analytics (MRR, ARR, churn rate, LTV, CAC)
- Integration: PostHog, Mixpanel, or Amplitude
```

### 5. Email Automation
```
- Transactional (welcome, receipt, password reset)
- Marketing (product updates, promotions)
- Behavioral triggers (abandoned onboarding, inactive user)
- Drip campaigns (onboarding, re-engagement)
- Integration: Resend, SendGrid, or Mailgun
```

### 6. Support Systems
```
- Help center / knowledge base
- In-app chat widget
- Ticket management
- Canned responses
- SLA tracking
- Customer satisfaction (CSAT) surveys
- Integration: Intercom, Zendesk, or custom
```

### 7. Admin Dashboard
```
- User management (CRUD, impersonation)
- Subscription management (override, credit)
- Feature flag management
- System health overview
- Revenue metrics dashboard
- Support ticket overview
```

### 8. Feature Flags
```
- Boolean flags (on/off)
- Percentage rollouts (1% → 10% → 50% → 100%)
- User segment targeting
- A/B test integration
- Kill switches for emergency
- Integration: LaunchDarkly, PostHog, or Unleash
```

### 9. A/B Testing
```
- Landing page variants
- Pricing page experiments
- Onboarding flow optimization
- Feature UX variants
- Statistical significance calculation
- Revenue impact measurement
```

### 10. Affiliate & Referral Systems
```
- Referral codes with tracking
- Reward tiers (credits, discounts, cash)
- Attribution tracking (first-touch, last-touch)
- Payout management
- Fraud detection (self-referral, abuse)
```

### 11. SEO Optimization
```
- Technical SEO (sitemap, robots.txt, meta tags)
- Schema markup (JSON-LD)
- Performance optimization (Core Web Vitals)
- Content strategy (blog, guides, docs)
- Internal linking structure
- Programmatic SEO (template pages)
```

### 12. AI Support Agent
```
- Knowledge base RAG (answers from docs)
- Conversation history
- Escalation to human
- Guardrails (hallucination prevention)
- Feedback loop (thumbs up/down)
- Analytics (resolution rate, CSAT)
```

## SaaS Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| MRR | Sum of all monthly subscriptions | Growing |
| ARR | MRR × 12 | Growing |
| Churn Rate | Lost customers / Total customers | < 5% monthly |
| Net Revenue Retention | (Start MRR + Expansion - Churn) / Start MRR | > 100% |
| CAC | Total acquisition cost / New customers | < LTV/3 |
| LTV | ARPU × Average lifetime months | > 3× CAC |
| Activation Rate | Activated users / Signups | > 40% |
| Trial-to-Paid | Paid conversions / Trial starts | > 15% |

## Launch Checklist

```
[ ] Landing page live with clear value prop
[ ] Signup flow working (< 30 seconds)
[ ] Onboarding guides user to activation
[ ] Billing integration tested (trial, upgrade, cancel)
[ ] Transactional emails configured
[ ] Analytics tracking all key events
[ ] Support channel available (chat or email)
[ ] Admin dashboard accessible
[ ] Error monitoring active (Sentry)
[ ] Performance baseline established
[ ] SEO basics (meta tags, sitemap, robots.txt)
[ ] Legal pages (privacy, terms, cookie policy)
```
