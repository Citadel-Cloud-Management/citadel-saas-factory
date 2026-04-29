---
name: ms-saas-factory
description: Full SaaS factory mode — ideation through deployment for multi-tenant SaaS, AI-native apps, B2B/B2C platforms, marketplaces, enterprise systems, healthcare, and fintech. Covers entire lifecycle.
type: framework
priority: 9
---

# Full Stack SaaS Factory Mode

## Core Rule

Operate as an autonomous SaaS factory capable of end-to-end product development from ideation to production.

## Factory Capabilities

### Product Lifecycle
1. **Ideation** — market research, competitive analysis, value proposition
2. **Architecture** — system design, tech stack selection, data modeling
3. **Coding** — full-stack implementation, API design, UI/UX
4. **Testing** — unit, integration, E2E, load, security testing
5. **Deployment** — containerization, orchestration, GitOps
6. **Observability** — monitoring, alerting, dashboards, SLOs
7. **Incident Response** — runbooks, escalation, postmortems
8. **Customer Support** — ticketing, knowledge base, chatbots
9. **Analytics** — product analytics, funnel analysis, cohorts
10. **Growth Automation** — onboarding, engagement, retention
11. **Marketing Automation** — email sequences, campaigns, nurture
12. **SEO Optimization** — technical SEO, content, schema markup
13. **Billing Integration** — subscriptions, usage-based, trials
14. **Onboarding Systems** — progressive disclosure, guided tours

## Supported Platform Types

| Type | Key Requirements |
|------|-----------------|
| Multi-tenant SaaS | Tenant isolation, RLS, customization, billing |
| AI-native applications | Model routing, guardrails, embeddings, fine-tuning |
| B2B platforms | Workspaces, SSO, RBAC, audit logs, API access |
| B2C platforms | Social auth, profiles, feeds, notifications |
| Marketplaces | Two-sided, payments, escrow, reviews, search |
| Enterprise systems | SSO, compliance, SLAs, data residency |
| Internal tools | Admin panels, workflows, approvals, dashboards |
| Healthcare systems | HIPAA, HL7/FHIR, consent, audit trails |
| Fintech platforms | PCI-DSS, KYC/AML, ledger, reconciliation |

## Standard SaaS Architecture

```
┌─────────────────────────────────────────────┐
│                 CDN / WAF                     │
├─────────────────────────────────────────────┤
│              Load Balancer                    │
├──────────┬──────────┬───────────────────────┤
│ Frontend │ API      │ Background Workers     │
│ (Next.js)│ (FastAPI)│ (Celery/Bull)          │
├──────────┴──────────┴───────────────────────┤
│           Service Layer                      │
├──────────┬──────────┬───────────────────────┤
│PostgreSQL│ Redis    │ Object Storage (S3)    │
├──────────┴──────────┴───────────────────────┤
│     Monitoring │ Logging │ Tracing           │
└─────────────────────────────────────────────┘
```

## Multi-Tenancy Patterns

| Pattern | When to Use | Implementation |
|---------|-------------|---------------|
| Shared DB, shared schema | Cost-sensitive, <100 tenants | RLS policies, tenant_id column |
| Shared DB, separate schemas | Moderate isolation needs | Schema per tenant, connection routing |
| Separate databases | Strict isolation, enterprise | DB per tenant, connection pool per tenant |

## SaaS Feature Checklist

```
Core:
[ ] Authentication (email, social, SSO)
[ ] Authorization (RBAC, permissions)
[ ] Multi-tenancy (isolation, customization)
[ ] Billing (subscriptions, trials, usage)
[ ] Onboarding (guided setup, templates)

Growth:
[ ] Analytics (product, business, funnel)
[ ] Email automation (transactional, marketing)
[ ] Notifications (in-app, email, push)
[ ] Feature flags (rollout, A/B testing)
[ ] Referral system (codes, rewards)

Enterprise:
[ ] SSO/SAML (Okta, Azure AD)
[ ] Audit logs (who, what, when)
[ ] Data export (GDPR, portability)
[ ] API access (keys, rate limits, docs)
[ ] SLA monitoring (uptime, performance)
```
