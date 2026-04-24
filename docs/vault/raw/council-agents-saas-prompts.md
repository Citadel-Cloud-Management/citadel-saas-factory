# THE COUNCIL FRAMEWORK
## Multi-Agent SaaS Prompt System — Architecture, Implementation & Validation

> **How to use this document:**
> Each prompt below activates a Council of specialized agents. You assign roles, then each agent speaks in sequence before the Orchestrator synthesizes a final verdict. Copy the prompt block, fill the bracketed fields, and paste into Claude or Codex. The Council structure forces the model to hold multiple adversarial perspectives simultaneously — producing outputs that are richer, more stress-tested, and significantly harder to break in production.

---

## THE COUNCIL — AGENT ROSTER

| Agent | Symbol | Primary Function | What They Catch |
|---|---|---|---|
| Researcher | 🔍 | Surfaces context, facts, precedents | Missing domain knowledge, wrong assumptions |
| Strategist | 🗺️ | Structures plans and sequencing | Unclear priorities, wrong build order |
| Creative | 💡 | Generates novel approaches | Over-engineering, tunnel vision |
| Critic | 🔎 | Challenges every assumption | Fragile logic, hidden dependencies |
| Devil's Advocate | 😈 | Argues hardest against the consensus | Groupthink, false confidence |
| Ethicist | ⚖️ | Evaluates moral and unintended consequences | Privacy violations, unfair outcomes |
| Implementer | 🔧 | Translates ideas into executable steps | Vague plans, missing concrete details |
| Fact-Checker | ✅ | Verifies accuracy, flags overconfidence | Outdated patterns, wrong library versions |
| Orchestrator | 🧠 | Synthesizes all agents into a final recommendation | Contradiction, lack of closure |

---
---

# PROMPT A — COUNCIL ARCHITECTURE SESSION
## System Design, Infrastructure & Strategic Foundation

---

```
You are convening a Council of nine specialized AI agents to design
a production-grade SaaS system. Each agent must speak from their
distinct cognitive role. Do not collapse into consensus prematurely.
Let the tension between agents produce a better answer than any single
perspective could.

This is not a brainstorm. This is a structured adversarial review
that ends in a synthesized, actionable, opinionated recommendation.

════════════════════════════════════════════════════════════
PRODUCT BRIEF — FILL THIS IN COMPLETELY BEFORE SUBMITTING
════════════════════════════════════════════════════════════

PRODUCT IDENTITY:
  Name:                   [e.g., "Meridian" — workforce analytics platform]
  Core problem solved:    [one sentence — what pain exists without this]
  Primary user persona:   [job title, context, frustration they have today]
  Secondary persona:      [if applicable]
  Business model:         [e.g., per-seat SaaS, usage-based, freemium → paid]

CUSTOMER PROFILE:
  Target segment:         [SMB / Mid-Market / Enterprise / PLG → Enterprise]
  Deal size expectation:  [e.g., $200/month self-serve or $50K ACV enterprise]
  Compliance exposure:    [HIPAA / SOC2 / GDPR / PCI-DSS / FedRAMP / none]
  Expected data sensitivity: [PII / PHI / financial / proprietary / public]

TECHNICAL CONTEXT:
  Cloud:                  [AWS / Azure / GCP / multi-cloud]
  Preferred regions:      [e.g., us-east-1, eu-west-1 for GDPR]
  Team size:              [e.g., 2 BE, 1 FE, 1 DevOps, 1 founding engineer]
  Existing stack:         [languages, frameworks, infra already in place]
  Existing data:          [greenfield / migrating from legacy / hybrid]

SCALE REQUIREMENTS:
  Launch day users:       [e.g., 200 beta users]
  Month 6 target:         [e.g., 2,000 users across 40 tenants]
  Month 18 target:        [e.g., 50,000 users across 800 tenants]
  Peak load pattern:      [e.g., business hours only / 24-7 / batch spikes]
  Data volume:            [e.g., 5GB at launch, ~2TB at 18 months]

CORE FEATURE MODULES:
  (List each module — e.g., Auth, Billing, Reporting, Notifications, API)
  Module 1:               [name + one-line description]
  Module 2:               [name + one-line description]
  Module 3:               [name + one-line description]
  ...

INTEGRATION SURFACE:
  SSO providers:          [Okta / Azure AD / Google Workspace / custom SAML]
  Third-party APIs:       [Stripe, Salesforce, Slack, etc. — list them]
  Webhooks required:      [yes/no — describe direction: inbound/outbound]
  Data export needs:      [CSV / API / Parquet / real-time stream]

BUSINESS CONSTRAINTS:
  Timeline to MVP:        [e.g., 10 weeks]
  Budget sensitivity:     [cost-optimize hard / balanced / performance-first]
  Must-have at launch:    [3–5 non-negotiable features]
  Deliberately deferred:  [what you are explicitly NOT building in MVP]

════════════════════════════════════════════════════════════
COUNCIL SESSION — BEGIN
════════════════════════════════════════════════════════════

Now speak as each agent in sequence. Each agent must:
  1. State their role and lens
  2. Deliver their full analysis (no summaries — full depth)
  3. Identify the 2–3 things OTHER agents will likely miss or get wrong

─────────────────────────────────────────────────────────────
🔍 RESEARCHER — Context, Precedent & Domain Intelligence
─────────────────────────────────────────────────────────────
Surface:
  • Industry-specific architectural patterns that have succeeded or failed
    for this product type at this scale
  • Regulatory and compliance facts that will constrain architecture choices
    (cite specific requirements — HIPAA §164.312, SOC2 CC6, GDPR Art. 17, etc.)
  • Known failure modes in similar SaaS products (with root cause if known)
  • The current best-in-class reference architectures in this space
  • Technology choices that appear valid but have known hidden costs at scale
  • Competitor infrastructure decisions visible via public postmortems,
    engineering blogs, or job descriptions

Do NOT summarize. Surface specific, actionable intelligence.

─────────────────────────────────────────────────────────────
🗺️ STRATEGIST — Structure, Sequencing & Phased Execution
─────────────────────────────────────────────────────────────
Produce:

  PHASE 1 — Foundation (Weeks 1–4):
    What must exist before anything else can be built.
    Define: infrastructure primitives, auth skeleton, data model core,
    local dev environment, CI pipeline baseline.

  PHASE 2 — Core Product (Weeks 5–10):
    What constitutes a usable, shippable product.
    Define: which modules to build in order, integration order,
    feature flags strategy, observability baseline.

  PHASE 3 — Hardening (Post-MVP):
    What gets deferred without compromising MVP viability.
    Define: compliance certifications, performance optimization,
    advanced billing logic, enterprise SSO, disaster recovery.

  DECISION FRAMEWORK:
    For every major architectural fork (monolith vs. micro,
    REST vs. GraphQL, schema-per-tenant vs. row-level isolation, etc.):
    — State the options
    — State the decision point (when does each become right/wrong)
    — Give a concrete recommendation for THIS product at THIS stage

  SEQUENCING RISKS:
    What happens if a team builds module B before module A is stable?
    Identify the 3 highest-risk sequencing mistakes.

─────────────────────────────────────────────────────────────
💡 CREATIVE — Novel Approaches & Contrarian Architecture
─────────────────────────────────────────────────────────────
Challenge the default assumptions. Propose:

  • Alternative architectural patterns the team has probably NOT considered
    (e.g., event-sourced core instead of CRUD, embedded analytics instead
    of third-party, local-first sync instead of server-side state)
  • One genuinely unconventional technology choice that could give this
    product a real competitive moat if it worked — and what would need to
    be true for it to work
  • Which "standard" SaaS patterns are actually unnecessary for this
    specific product at MVP and could be dropped without consequence
  • A DX (developer experience) innovation that would make the codebase
    dramatically easier to maintain at 18 months vs. the default approach
  • If you had to build this product in half the time with half the people,
    what would you sacrifice and what would you protect? Why?

─────────────────────────────────────────────────────────────
🔎 CRITIC — Assumption Audit & Structural Weaknesses
─────────────────────────────────────────────────────────────
Challenge everything stated in the product brief. Specifically:

  ASSUMPTION AUDIT:
    List every implicit assumption embedded in the brief (even if unstated).
    For each: is it verified, unverified, or likely wrong?

  ARCHITECTURAL FRAGILITIES:
    Where will this design break first under real-world conditions?
    (Not hypothetical — what actually breaks in systems like this)

  DEPENDENCY RISKS:
    Which third-party dependencies create existential risk if they change
    pricing, API, or terms of service? What is the mitigation?

  SCALING CLIFF:
    At what user/data/tenant count does the proposed architecture require
    a painful migration or rewrite? Is that cliff before or after PMF?

  TEAM RISK:
    Given the team size and composition in the brief, which parts of this
    architecture require expertise the team likely does not have?
    What does that failure look like in production?

─────────────────────────────────────────────────────────────
😈 DEVIL'S ADVOCATE — The Strongest Case Against This
─────────────────────────────────────────────────────────────
Argue, with full conviction, the strongest possible case that:

  1. The chosen cloud provider / architecture is WRONG for this product
     (even if it seems obvious). What would a senior architect at a
     competing infrastructure company say to convince this team to switch?

  2. Multi-tenancy at MVP is a mistake. Build single-tenant first.
     Make the most compelling possible argument for this position,
     then state what evidence would change your mind.

  3. The team is about to over-engineer something that should be a
     monolith. Name the thing. Explain the cost of the complexity tax.

  4. There is a simpler, cheaper, faster path to the same outcome that
     the team is ignoring because it feels "not serious enough."
     Describe it in full. Why is the team reluctant to take it?

Note: The Devil's Advocate is not trying to be correct. They are trying
to force the team to have answers to the hardest objections before
they encounter them in the field.

─────────────────────────────────────────────────────────────
⚖️ ETHICIST — Moral Exposure & Unintended Consequences
─────────────────────────────────────────────────────────────
Evaluate:

  DATA ETHICS:
    • What data will this system collect that users may not expect?
    • Is the consent model honest and legible, or buried in ToS?
    • What is the harm model if this data is breached, subpoenaed,
      or sold? Who are the most vulnerable affected parties?
    • Does the data collection serve the user or only the business?

  ALGORITHMIC RISK:
    If this product uses ranking, scoring, filtering, or recommendations:
    • Who gets systematically deprioritized and why?
    • Does the system encode historical bias into future decisions?
    • Is there a feedback loop that will amplify inequality over time?

  POWER DYNAMICS:
    • Does this product create a data lock-in that harms customers
      if they want to leave? Is that lock-in by design?
    • Who controls the data — the user, the tenant admin, or the platform?
    • What happens to user data when a tenant stops paying?

  REGULATORY EXPOSURE BEYOND COMPLIANCE:
    • What is the product liability if this system makes a wrong decision
      with real-world consequences (e.g., healthcare, HR, finance)?
    • What is the reputational risk if the worst-case use of this product
      was published on the front page of a major newspaper?

  MINIMUM ETHICAL ARCHITECTURE:
    • What 3 design decisions would make this product meaningfully more
      ethical without compromising its business model?

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — Concrete Execution Blueprint
─────────────────────────────────────────────────────────────
Translate the above into an executable engineering plan:

  REPOSITORY STRUCTURE:
    Propose the exact monorepo or polyrepo layout with folder names
    and the purpose of each. Be specific — do not say "services folder."

  DAY 1 CHECKLIST:
    What does a new engineer do in their first 8 hours to have a
    running local environment with seeded data and passing tests?

  INFRASTRUCTURE AS CODE:
    Which IaC tool (Terraform / Pulumi / CDK / Bicep) and why.
    What gets provisioned in the first sprint — exact resource list.

  DATABASE MIGRATION STRATEGY:
    How are schema changes managed from day 1?
    What tool (Flyway / Alembic / Prisma Migrate / Liquibase)?
    What is the branching + migration conflict resolution strategy?

  LOCAL DEVELOPMENT CONTRACT:
    Define the developer experience: docker-compose services,
    seed scripts, environment variable management, hot reload,
    local SSL if required.

  DEPLOYMENT PIPELINE — EXACT STAGES:
    Stage 1 (commit): lint, type-check, unit test
    Stage 2 (PR): integration test, security scan, preview deploy
    Stage 3 (merge to main): staging deploy, smoke test, migration run
    Stage 4 (release): canary → production, rollback trigger definition

  FIRST 10 API ENDPOINTS:
    List the first 10 endpoints that must exist before any frontend
    can function. For each: method, path, auth requirement, purpose.

─────────────────────────────────────────────────────────────
✅ FACT-CHECKER — Accuracy Audit & Confidence Calibration
─────────────────────────────────────────────────────────────
Review every recommendation made by all preceding agents and:

  FLAG any:
    • Technology recommendations that are outdated (deprecated, EOL,
      superseded by better alternatives in the last 18 months)
    • Performance or scale claims made without supporting evidence
    • Compliance claims that oversimplify or misstate a regulation
    • "Best practice" statements that are actually contested in the field
    • Library or tool recommendations with known security vulnerabilities
    • Cost estimates that are likely to be materially wrong at scale

  VERIFY:
    • That the proposed stack components are mutually compatible
    • That the compliance framework cited actually applies to this product
    • That the scale numbers given in the brief are internally consistent
      (e.g., "50K users across 800 tenants" = ~62 users/tenant average —
      does the architecture reflect the right distribution model?)

  CONFIDENCE MAP:
    Rate each major recommendation:
    HIGH confidence — well-established, widely validated
    MEDIUM confidence — reasonable but context-dependent
    LOW confidence — speculative, verify before committing

─────────────────────────────────────────────────────────────
🧠 ORCHESTRATOR — Synthesis, Final Recommendation & Decision Log
─────────────────────────────────────────────────────────────
You have heard all eight agents. Now synthesize:

  COUNCIL VERDICT:
    Produce the definitive architectural recommendation for this product.
    This is not a "consider both sides" summary. This is a decision.
    State it with authority.

  WHERE THE COUNCIL AGREED:
    List the points of genuine consensus and why that consensus is
    well-founded.

  WHERE THE COUNCIL DISAGREED:
    List the genuine tensions that remain unresolved. For each:
    — What information would resolve this disagreement?
    — What is the cost of getting this decision wrong?
    — What is the recommended default until that information exists?

  ARCHITECTURE DECISION RECORD (ADR) — 10 KEY DECISIONS:
    For each major architectural decision:
    Decision:         [e.g., Row-level tenant isolation over schema-per-tenant]
    Rationale:        [2–3 sentences]
    Alternatives:     [what was considered and rejected]
    Reversal cost:    [low / medium / high — how painful to undo at 12 months]
    Owner:            [who is accountable for this decision]

  RISK REGISTER — TOP 5 RISKS:
    Risk:             [name it precisely]
    Probability:      [low / medium / high]
    Impact:           [low / medium / high / catastrophic]
    Trigger:          [what event would confirm this risk is materializing]
    Mitigation:       [concrete action, not a category]

  90-DAY EXECUTION SUMMARY:
    Week 1–2:   [infrastructure foundation — exact outputs]
    Week 3–4:   [auth + data model + CI/CD — exact outputs]
    Week 5–7:   [core module 1 + 2 — exact outputs]
    Week 8–10:  [integrations + observability + staging hardening]
    Post-MVP:   [compliance, advanced billing, enterprise features]

  FIRST DECISION THE TEAM MUST MAKE (before writing a line of code):
    [State it. Give the recommended answer. Give the deadline.]
```

---
---

# PROMPT B — COUNCIL IMPLEMENTATION SESSION
## Module-Level Code Generation, Testing & Security

---

```
You are convening a Council of nine specialized agents to implement
a specific module of a production SaaS system. The architecture has
already been decided (paste it below). Your job is to produce
working, tested, secure, observable code — not a sketch of it.

No placeholders. No TODOs. No "implement error handling here."
Every function must be complete. Every edge case must be handled.
Every test must run.

════════════════════════════════════════════════════════════
MODULE BRIEF — FILL THIS IN COMPLETELY
════════════════════════════════════════════════════════════

MODULE IDENTITY:
  Module name:              [e.g., "Tenant Provisioning Service"]
  System role:              [what breaks if this module fails]
  Owner team / persona:     [who wrote the spec, who will maintain it]

TECHNICAL CONTRACT:
  Language + version:       [e.g., Python 3.12 / TypeScript 5.3 / Go 1.22]
  Framework + version:      [e.g., FastAPI 0.110 / NestJS 10 / Gin 1.9]
  Database + ORM:           [e.g., PostgreSQL 16 + SQLAlchemy 2.0]
  Message queue:            [e.g., SQS / RabbitMQ / Redis Streams / none]
  Auth mechanism:           [e.g., JWT RS256 / OAuth2 access token / mTLS]
  Deployment target:        [e.g., Kubernetes (EKS) / AWS Lambda / App Service]
  Environment:              [prod account isolated / shared staging]

FUNCTIONAL SPECIFICATION:
  Purpose (one sentence):   [what this module does]
  Triggers:                 [HTTP request / event / cron / queue message]
  Inputs:                   [exact request schema or event payload structure]
  Outputs:                  [exact response schema or side effects emitted]
  State changes:            [what gets written to what storage]
  Events emitted:           [what downstream systems will consume]

BUSINESS RULES (list every one — this becomes the test matrix):
  Rule 1:  [e.g., "A tenant name must be globally unique, case-insensitive"]
  Rule 2:  [e.g., "Provisioning must be idempotent — same request twice = same result"]
  Rule 3:  [e.g., "Free tier tenants cannot exceed 5 users"]
  Rule 4:  [e.g., "Admin users cannot be deleted, only deactivated"]
  Rule 5:  [continue for all rules...]

DEPENDENCIES (services this module calls):
  Internal:   [list other internal services + what operations are called]
  External:   [third-party APIs — Stripe, SendGrid, etc. — exact operations]
  Database:   [which tables/collections this module reads and writes]
  Cache:      [Redis keys this module reads/writes + TTL expectations]

SECURITY INVARIANTS (these are non-negotiable):
  [e.g., "tenantId must always be derived from the JWT claims, NEVER from request body"]
  [e.g., "All DB queries must include tenant_id = auth.tenant_id in WHERE clause"]
  [e.g., "Secrets loaded from environment — never hardcoded, never logged"]

ARCHITECTURE CONTEXT:
  [Paste the relevant section of the Claude architecture output here]

════════════════════════════════════════════════════════════
COUNCIL SESSION — BEGIN
════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
🔍 RESEARCHER — Prior Art, Library Intelligence & Pattern Audit
─────────────────────────────────────────────────────────────
Before a line of code is written, surface:

  • The canonical implementation pattern for this module type in the
    specified language/framework ecosystem (with source references)
  • Known pitfalls specific to the libraries being used in this version
    (e.g., SQLAlchemy 2.0 async session management gotchas, NestJS
    circular dependency patterns, FastAPI background task memory leaks)
  • The most common production bug introduced in this type of module
    (tenant isolation violations, race conditions in provisioning flows,
    silent failures in async operations, etc.)
  • Any relevant CVEs or security advisories in the specified dependency
    versions that must be addressed in the implementation
  • Reference implementations from high-quality open-source SaaS
    codebases that handle this problem well (name the repo + pattern)

─────────────────────────────────────────────────────────────
🗺️ STRATEGIST — File Structure, Layer Design & Implementation Order
─────────────────────────────────────────────────────────────
Produce:

  EXACT FILE STRUCTURE:
    (Every file that will be created. Every folder. No ambiguity.)

    /modules/[module-name]/
    ├── __init__.py / index.ts          [exports]
    ├── router.py / controller.ts       [HTTP layer — routing only]
    ├── service.py / service.ts         [business logic — pure functions where possible]
    ├── repository.py / repository.ts  [data access — all DB calls here]
    ├── schemas.py / dto.ts             [input/output validation models]
    ├── models.py / entity.ts          [ORM models / DB entities]
    ├── events.py / events.ts          [event definitions + emitters]
    ├── exceptions.py / errors.ts      [typed error classes]
    ├── dependencies.py / guards.ts    [DI factories, auth guards]
    └── tests/
        ├── test_service.py / service.spec.ts
        ├── test_router.py / controller.spec.ts
        └── test_repository.py / repository.spec.ts

  SHARED UTILITIES TO USE (not re-implement):
    [List which shared utilities from the broader codebase this module
    consumes — auth middleware, logger, DB session factory, event bus, etc.]

  IMPLEMENTATION ORDER:
    1. Models + migration
    2. Repository layer (no business logic)
    3. Service layer (no HTTP concerns)
    4. Exception classes
    5. Schemas / DTOs
    6. Router / Controller
    7. Unit tests (service layer first)
    8. Integration tests (router layer)
    9. Event emitters
    10. Documentation

  WHY THIS ORDER:
    [Explain the dependency chain — why each step must precede the next]

─────────────────────────────────────────────────────────────
💡 CREATIVE — Implementation Innovations & DX Improvements
─────────────────────────────────────────────────────────────
Propose:

  • One non-obvious implementation technique that would make this module
    significantly more robust or maintainable than the standard approach
    (e.g., using PostgreSQL advisory locks for idempotent provisioning
    instead of application-level mutex, using a state machine library
    instead of conditional logic for multi-step workflows)
  • A testing strategy that would make regressions on this module
    nearly impossible to introduce undetected
  • A developer ergonomics improvement: how could this module's interface
    be designed so that it's nearly impossible for other developers to
    misuse it? (Pit of success design)
  • If this module will be touched by 5+ engineers over 2 years, what
    is the single most important structural decision to make now that
    will prevent it from becoming a legacy mess?

─────────────────────────────────────────────────────────────
🔎 CRITIC — Interface Audit & Hidden Complexity
─────────────────────────────────────────────────────────────
Before implementation begins, challenge:

  CONTRACT COMPLETENESS:
    Is the functional spec complete enough to implement without
    asking questions? List every ambiguity that would force an
    engineer to make a silent assumption.

  MISSING BUSINESS RULES:
    What business rules are implied by the spec but not explicitly
    stated? (e.g., "The spec says create a tenant but doesn't say
    what happens if the provisioning database write succeeds but the
    Stripe customer creation fails. That's a rule.")

  EDGE CASES NOT COVERED:
    List the 10 most likely production edge cases this spec does not
    address, with the likely failure mode if each goes unhandled.

  DEPENDENCY REVIEW:
    For each external dependency this module calls:
    — What is the failure mode if it returns 500?
    — What is the failure mode if it times out?
    — What is the failure mode if it returns a partial success?
    — Is the calling code resilient to all three?

─────────────────────────────────────────────────────────────
😈 DEVIL'S ADVOCATE — Why This Module Will Fail in Production
─────────────────────────────────────────────────────────────
Argue with conviction:

  1. This module as specified will become the biggest source of
     on-call pages within 6 months. Here is exactly why and how
     it will fail at 3am for a reason no one thought of.

  2. The data model implied by this spec will require a painful
     migration within 12 months when [specific business requirement]
     changes. Name the field or relationship that is about to be wrong.

  3. The test suite implied by this spec will give false confidence.
     Here is the specific class of bug that will pass all tests
     and still corrupt production data.

  4. There is a simpler version of this module that handles 90% of
     the use cases with 30% of the code. The team is over-engineering
     because [specific reason]. Here is the simpler version.

─────────────────────────────────────────────────────────────
⚖️ ETHICIST — Data Handling, Consent & Fairness Audit
─────────────────────────────────────────────────────────────
For this specific module:

  DATA MINIMIZATION AUDIT:
    Is this module collecting or storing data it doesn't actually need?
    For each data field: what is the business justification for storing it?

  RETENTION & DELETION:
    When a tenant is deleted, is all their data actually deleted?
    From: primary DB, replicas, backups, audit logs, caches,
    third-party systems (Stripe customer, email lists, analytics)?
    Is there a documented and tested data deletion procedure?

  CONSENT SURFACE:
    Does this module trigger any action that a user consented to
    at one point but may have since revoked? Is revocation honored?

  AUDIT TRAIL COMPLETENESS:
    For regulated operations (user deletion, data export, privilege
    escalation, payment processing): is there an immutable audit log
    entry that could satisfy a regulator in an investigation?

  BIAS / FAIRNESS:
    If this module makes any automated decision about a user or tenant
    (e.g., rate limiting, fraud scoring, feature gating), is the
    decision logic transparent, documented, and contestable?

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — Complete Working Code
─────────────────────────────────────────────────────────────
Write the full implementation. Requirements:

  CODE STANDARDS:
    □ Clean architecture strictly enforced — no business logic in router,
      no DB calls in service, no HTTP concerns in repository
    □ Every function has a single responsibility
    □ Every public function has a docstring / JSDoc with: purpose,
      params, return, raises / throws
    □ No function longer than 40 lines — extract if necessary
    □ All strings that appear in API responses are constants, not literals
    □ No magic numbers — named constants only

  ERROR HANDLING:
    □ Typed exception hierarchy (Base → Domain → Specific)
    □ All exceptions caught at router layer, never leaked to caller
    □ Error response format: { code, message, details, traceId }
    □ HTTP status codes semantically correct (422 for validation,
      409 for conflicts, 404 for not found, 403 for authz failure)
    □ All external API failures caught with explicit error classification:
      transient (retry) vs. permanent (fail fast)

  SECURITY IMPLEMENTATION:
    □ Auth guard applied — token validated before any handler executes
    □ tenantId extracted from JWT claims — NEVER from request body or path
    □ Every repository method includes tenant_id filter as first WHERE clause
    □ All SQL uses parameterized queries — zero string interpolation
    □ Input validation on every public endpoint (reject unknown fields)
    □ Rate limiting middleware referenced (not reimplemented here)
    □ Sensitive fields (passwords, tokens, secrets) never logged

  OBSERVABILITY:
    □ Structured JSON logging at every operation entry/exit
    □ Log fields: timestamp, level, traceId, tenantId, userId,
      operation, durationMs, success, errorCode (if applicable)
    □ External API calls: log request (sanitized), response status,
      latency, retry count
    □ Emit metrics for: request count, error rate, latency p95,
      external API call latency, queue depth (if applicable)

  IDEMPOTENCY:
    □ Identify every operation that must be idempotent
    □ Implement idempotency key handling (DB unique constraint +
      application-level deduplication)
    □ Document idempotency window (how long is a duplicate request
      recognized as a duplicate?)

  ASYNC / CONCURRENCY:
    □ All I/O operations are async
    □ No blocking calls in async context
    □ Database connection pool properly configured and documented
    □ Queue consumers handle partial failures without losing messages

  OUTPUT REQUIRED:
    Deliver every file in the structure defined by the Strategist.
    Each file: complete, runnable, no placeholders.
    End each file with: # END OF FILE — [filename]

─────────────────────────────────────────────────────────────
✅ FACT-CHECKER — Code Review & Accuracy Audit
─────────────────────────────────────────────────────────────
After the Implementer delivers code:

  VERIFY:
    □ All import statements reference real, compatible library versions
    □ All ORM patterns match the specified ORM version's actual API
      (flag any patterns that changed between major versions)
    □ All async/await patterns are correct for the runtime (e.g., no
      asyncio.run() inside a running event loop in FastAPI)
    □ JWT validation uses the correct algorithm (RS256 not HS256 for
      asymmetric keys — common mistake)
    □ All environment variable names match the .env.example
    □ Migration SQL is valid for the specified DB version
    □ Test assertions are actually testing what they claim to test
      (check for tests that always pass regardless of behavior)

  FLAG:
    □ Any deprecated API usage in the specified framework version
    □ Any pattern that works in unit tests but fails under concurrent load
    □ Any missing index implied by the query patterns in the repository
    □ Any N+1 query pattern in relationship loading
    □ Any unclosed database connection or resource leak

  CONFIDENCE RATING:
    For each major implementation decision, rate:
    HIGH / MEDIUM / LOW confidence — with justification

─────────────────────────────────────────────────────────────
🧠 ORCHESTRATOR — Final Delivery Package & Handoff
─────────────────────────────────────────────────────────────
Synthesize the Council's work into a final delivery:

  IMPLEMENTATION VERDICT:
    Is this module ready to merge? If not, what are the blocking items?

  OPEN ISSUES LOG:
    (Issues raised by the Council that require human decision before
    or after merge)
    Issue:        [description]
    Raised by:    [agent]
    Blocking:     [yes/no]
    Owner:        [who resolves this]
    Deadline:     [before merge / before production / next sprint]

  TEST MATRIX SIGN-OFF:
    Confirm that the following test categories are covered:
    □ Happy path — all inputs valid, all dependencies succeed
    □ Validation failure — each invalid input field individually
    □ Authentication failure — missing token, expired token, wrong tenant
    □ Authorization failure — valid token, insufficient role
    □ Tenant isolation — attempt to access another tenant's resource
    □ Idempotency — duplicate request with same idempotency key
    □ External dependency failure — 500, timeout, partial success
    □ Concurrent request — same operation executed simultaneously
    □ Data boundary — max field lengths, empty strings, null values
    □ Business rule violation — each rule listed in the brief

  FOLLOW-ON MODULE PROMPT:
    Generate the exact Module Brief (top section of this prompt)
    pre-filled for the NEXT module that should be built, based on
    the dependency chain established in the architecture session.

  DEPLOYMENT CHECKLIST:
    □ Environment variables documented in .env.example
    □ DB migration tested on a copy of staging data
    □ Rollback plan documented (what to do if this deploy fails)
    □ Feature flag in place if module has user-facing changes
    □ Monitoring dashboard updated with new metrics
    □ On-call runbook updated with new failure modes and remediation
```

---
---

# PROMPT C — COUNCIL VALIDATION SESSION
## Security Review, Compliance Audit & Production Readiness

---

```
You are convening a Council of nine specialized agents to perform a
comprehensive pre-production review of a SaaS module or system.
This is not a code style review. This is a production readiness
assessment. Every finding must be actionable, located precisely in
the code, and rated by severity and blast radius.

════════════════════════════════════════════════════════════
REVIEW BRIEF
════════════════════════════════════════════════════════════

System under review:      [module name + system context]
Review trigger:           [pre-launch / post-incident / compliance audit /
                           new engineer review / major refactor]
Compliance requirements:  [HIPAA / SOC2 / GDPR / PCI-DSS / none]
Highest risk area:        [what is the team most worried about]
Previous known issues:    [any prior bugs, incidents, or concerns to probe]

[PASTE FULL CODE HERE — include all files in the module]

════════════════════════════════════════════════════════════
COUNCIL SESSION — BEGIN
════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
🔍 RESEARCHER — Threat Intelligence & Vulnerability Context
─────────────────────────────────────────────────────────────
Before the review begins:

  • Surface the OWASP Top 10 categories most relevant to this module type
  • Identify any known CVEs in the specific library versions used
  • Research recent real-world incidents in similar SaaS systems
    (publicly disclosed breaches or postmortems) that involved this
    class of component — what was the attack vector?
  • What are the CISA Known Exploited Vulnerabilities (KEV) that are
    relevant to this technology stack?
  • What compliance controls specifically apply to this module's
    data handling behavior?

─────────────────────────────────────────────────────────────
🗺️ STRATEGIST — Review Scope & Prioritization Framework
─────────────────────────────────────────────────────────────
Structure the review:

  REVIEW TAXONOMY:
    Tier 1 — Launch Blockers (must fix before any production traffic)
    Tier 2 — Pre-Scale Fixes (must fix before 1,000 users)
    Tier 3 — Compliance Debt (must fix before SOC2 / HIPAA audit)
    Tier 4 — Engineering Debt (fix within 90 days post-launch)
    Tier 5 — Observations (log, monitor, revisit at 6 months)

  ATTACK SURFACE MAP:
    List every external entry point to this module:
    — Public API endpoints (authenticated / unauthenticated)
    — Internal API endpoints (service-to-service)
    — Queue consumers
    — Cron jobs
    — Webhook receivers
    — Admin interfaces

  TRUST BOUNDARY MAP:
    Where does untrusted input enter the system?
    Where does it get validated?
    Where could it still cause harm after validation?

─────────────────────────────────────────────────────────────
💡 CREATIVE — Unconventional Attack Vectors
─────────────────────────────────────────────────────────────
Think like an attacker who has read the code:

  • What is the most creative, non-obvious attack against this system
    that would not be caught by a standard OWASP review?
  • What happens if an attacker controls a tenant that is a legitimate
    paying customer — what can they do to affect other tenants?
  • What happens if an internal microservice is compromised —
    how far can the blast radius spread through this module?
  • Is there a logic vulnerability (not a SQL injection, not an XSS —
    but a business logic flaw) that could be exploited at scale?
  • What would a "slow" attack look like — one that extracts value
    or data over months without triggering any alerts?

─────────────────────────────────────────────────────────────
🔎 CRITIC — Line-Level Security Audit
─────────────────────────────────────────────────────────────
Perform exhaustive review across:

  INJECTION:
    □ SQL injection — parameterized queries used everywhere?
    □ Command injection — any subprocess / shell calls?
    □ Template injection — any user input rendered in templates?
    □ SSRF — any URL constructed from user input?
    □ Path traversal — any file paths constructed from user input?

  AUTHENTICATION & AUTHORIZATION:
    □ All endpoints require authentication — no accidental public route?
    □ JWT validation: signature verified, expiry checked, audience verified?
    □ Role checks: every operation has an explicit authz check?
    □ Privilege escalation path: can a user grant themselves higher role?
    □ Horizontal privilege escalation: can user A access user B's resources?

  TENANT ISOLATION:
    □ Every DB query includes tenant_id in WHERE clause?
    □ tenantId is ALWAYS derived from auth context, never request body?
    □ Cross-tenant operations (admin only) require explicit elevated role?
    □ Batch operations scope correctly to single tenant?
    □ Exports / reports scope correctly — no cross-tenant data leakage?

  CRYPTOGRAPHY:
    □ Passwords hashed with bcrypt / argon2 / scrypt (not MD5/SHA1)?
    □ Tokens generated with cryptographically secure random (not Math.random)?
    □ TLS enforced on all external calls — no HTTP fallback?
    □ Secrets stored in environment / vault — not in code or DB plaintext?
    □ Encryption at rest for sensitive fields — implemented correctly?

  INPUT VALIDATION:
    □ All inputs validated on entry (schema validation, not just type check)?
    □ Max length enforced on all string fields?
    □ File uploads: type validated, size limited, content scanned?
    □ Numeric inputs: overflow/underflow protected?
    □ Dates: timezone-aware, reasonable range validated?

  ERROR HANDLING & INFORMATION DISCLOSURE:
    □ Stack traces never returned to API consumers?
    □ Error messages don't reveal system internals (DB schema, file paths)?
    □404 vs 403 responses consistent (don't reveal resource existence to unauth)?
    □ Timing attacks on auth endpoints mitigated (constant-time comparison)?

  LOGGING & AUDIT:
    □ PII never logged (names, emails, SSN, health data)?
    □ Secrets never logged (tokens, passwords, API keys)?
    □ Audit events emitted for all regulated operations?
    □ Logs tamper-evident (append-only store, signed, or SIEM-forwarded)?
    □ Log injection prevented (newlines, ANSI codes sanitized)?

  DEPENDENCY SECURITY:
    □ All dependencies pinned to exact versions?
    □ Lock file committed and used in CI?
    □ Automated CVE scanning in CI pipeline?
    □ No abandoned or unmaintained libraries (last commit > 2 years)?

─────────────────────────────────────────────────────────────
😈 DEVIL'S ADVOCATE — The Breach Scenario
─────────────────────────────────────────────────────────────
Construct three complete breach scenarios:

  SCENARIO 1 — EXTERNAL ATTACKER:
    Starting point: anonymous internet access
    Goal: exfiltrate tenant data
    Step-by-step attack path using only vulnerabilities in this code
    What alert (if any) would fire? When?
    What is the maximum data exposed before detection?

  SCENARIO 2 — MALICIOUS TENANT:
    Starting point: legitimate paid tenant account
    Goal: access competitor tenant's data
    Step-by-step attack path
    Why the current tenant isolation would or would not stop them

  SCENARIO 3 — COMPROMISED INTERNAL SERVICE:
    Starting point: attacker has compromised a service-to-service
    call (e.g., via stolen mTLS cert or internal API key)
    Goal: escalate to full data access
    Step-by-step lateral movement path through this module

  For each scenario:
    Likelihood:           [low / medium / high for a funded attacker]
    Detection capability: [would current monitoring catch this?]
    Remediation:          [what code change closes this path?]

─────────────────────────────────────────────────────────────
⚖️ ETHICIST — Compliance & Harm Assessment
─────────────────────────────────────────────────────────────
Evaluate against stated compliance requirements:

  GDPR (if applicable):
    □ Right to access — can user export all their data from this module?
    □ Right to erasure — is deletion complete, including backups?
    □ Data minimization — is each field stored actually necessary?
    □ Lawful basis — is the legal basis for processing documented in code?
    □ Data breach notification — can the system detect and report
      a breach in the 72-hour GDPR window?

  HIPAA (if applicable):
    □ PHI identified and mapped — do the PHI fields match the data model?
    □ Access controls on PHI — minimum necessary principle enforced?
    □ Audit log of all PHI access — immutable, 6-year retention?
    □ Encryption in transit and at rest — documented and verified?
    □ BAA implications — which third parties receive PHI from this module?

  SOC2 (if applicable):
    □ CC6 (Logical Access) — access provisioning and de-provisioning auditable?
    □ CC7 (System Operations) — monitoring and alerting in place?
    □ CC9 (Risk Mitigation) — vendor risk assessed for all third parties?
    □ A1 (Availability) — SLA measurable from this module's observability?

  HARM BEYOND COMPLIANCE:
    • If this module malfunctions silently (no errors thrown, wrong data
      returned), what is the worst-case real-world harm to an end user?
    • Who is most vulnerable if this system fails or is misused?
    • Is there a documented incident response plan that covers
      this module's failure modes?

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — Remediation Code
─────────────────────────────────────────────────────────────
For every CRITICAL and HIGH finding:

  Provide:
    FINDING:          [precise description]
    LOCATION:         [file:line or function name]
    VULNERABLE CODE:  [exact code snippet]
    FIXED CODE:       [complete replacement — no placeholders]
    TEST TO VERIFY:   [unit or integration test that proves the fix works
                       and will prevent regression]
    MIGRATION NEEDED: [yes/no — if yes, provide the migration script]

  For MEDIUM findings:
    Provide the fixed code and a brief explanation.
    No migration script required unless data is affected.

─────────────────────────────────────────────────────────────
✅ FACT-CHECKER — Finding Validation & False Positive Review
─────────────────────────────────────────────────────────────
Review all findings from the Critic and Devil's Advocate:

  For each finding:
    □ Is this actually exploitable in the current configuration?
      (Some SQL injection patterns are blocked by the ORM layer —
       confirm this is a real finding, not a false positive)
    □ Is the severity rating accurate given the actual blast radius?
    □ Does the proposed fix actually close the vulnerability, or does
      it introduce a new one?
    □ Is the finding specific to this code, or is it a framework-level
      control that's already mitigated elsewhere?

  RATE each finding:
    CONFIRMED — real vulnerability, accurate severity
    DOWNGRADED — real issue but severity overstated
    FALSE POSITIVE — not actually exploitable in context
    NEEDS MORE INFO — cannot confirm without [specific additional context]

─────────────────────────────────────────────────────────────
🧠 ORCHESTRATOR — Production Readiness Verdict
─────────────────────────────────────────────────────────────
Synthesize the Council's full review:

  VERDICT:
    □ SHIP IT — no blockers, risks accepted and documented
    □ SHIP WITH CONDITIONS — [list conditions, owner, deadline]
    □ DO NOT SHIP — [list blocking issues]

  FINDINGS SUMMARY TABLE:
    | ID | Severity | Category | Location | Fix Owner | Deadline |
    |----|----------|----------|----------|-----------|----------|
    | C1 | CRITICAL | Tenant isolation | service.py:47 | @engineer | Before deploy |
    | H1 | HIGH     | Missing auth check | router.py:23 | @engineer | Before deploy |
    | M1 | MEDIUM   | N+1 query | repository.py:89 | @engineer | Sprint 2 |
    ...

  COMPLIANCE READINESS:
    GDPR:   [READY / GAPS IDENTIFIED — list gaps]
    HIPAA:  [READY / GAPS IDENTIFIED — list gaps]
    SOC2:   [READY / GAPS IDENTIFIED — list gaps]

  MONITORING GAPS:
    List what is not currently being monitored that should be,
    with the specific alert rule to create.

  POST-LAUNCH REVIEW TRIGGER:
    Define the specific metric thresholds or events that should
    trigger a re-review of this module:
    [e.g., "Re-review if error rate exceeds 1% sustained for 10 minutes,
     or if any tenant isolation violation is detected in logs"]

  HANDOFF TO NEXT COUNCIL SESSION:
    What is the most important unresolved architectural question
    surfaced during this review that should be addressed in the
    next Architecture Council Session?
```

---
---

# HOW TO RUN THE COUNCIL — OPERATING INSTRUCTIONS

## Starting a Session

1. Choose the appropriate prompt (A = Architecture, B = Implementation, C = Validation)
2. Fill every bracketed field completely — incomplete briefs produce shallow output
3. Paste the full prompt into Claude (use Projects for persistent context)
4. Do not interrupt the Council mid-session — let all nine agents speak

## Connecting Sessions

```
Architecture Session (Prompt A)
  → Produces: ADR, phased roadmap, component map, risk register

Implementation Session (Prompt B) × N modules
  → Input: paste relevant ADR sections + module spec
  → Produces: complete code, test suite, deployment checklist

Validation Session (Prompt C)
  → Input: paste complete module code
  → Produces: security findings, remediation code, ship verdict
```

## The Iteration Loop

```
Implementer delivers code
  → Validation Council reviews
  → Implementer fixes CRITICAL + HIGH
  → Fact-Checker confirms fixes
  → Orchestrator issues ship verdict
  → Next module begins
```

## Escalation Protocol

If the Devil's Advocate raises a concern that no other agent can refute:
**Stop. Treat it as a blocker. Do not rationalize past it.**

If the Ethicist raises a harm that the business pressure is pushing to defer:
**Document it explicitly in the ADR. Make the trade-off visible and owned.**

If the Fact-Checker rates a Council recommendation as LOW confidence:
**Do not build on it. Spike the question separately before committing.**

---
---

# PROMPT D — COUNCIL PARALLEL FIX SESSION
## Simultaneous Multi-Front Remediation Across All Findings

---

> **When to use this prompt:**
> You have completed a Validation Session (Prompt C) and hold a findings list
> with CRITICAL, HIGH, and MEDIUM items across multiple files, layers, and
> domains. Rather than assigning one engineer to fix issues serially — which
> creates merge conflicts, re-introduces bugs, and produces inconsistent
> remediation quality — this session assigns every finding to a parallel
> workstream with a dedicated Council agent as owner, a defined interface
> contract between streams, and an Orchestrator-managed merge and verification
> protocol. The entire Council fixes everything at once, without stepping on
> each other.

---

```
You are convening a Council of nine specialized agents to execute a
parallel remediation operation across all outstanding findings from
a prior Validation Session. Every CRITICAL and HIGH finding is fixed
simultaneously in isolated workstreams. Every fix is tested in
isolation before integration. The Orchestrator manages sequencing,
merge order, and the final verification gate.

This is not a queue of tasks. This is coordinated simultaneous
execution. Each agent owns a defined workstream. No agent waits
for another to finish before beginning. Conflicts are resolved by
explicit interface contracts agreed before work starts.

════════════════════════════════════════════════════════════
PARALLEL FIX BRIEF — FILL THIS IN COMPLETELY
════════════════════════════════════════════════════════════

SYSTEM UNDER REMEDIATION:
  System name:              [e.g., "Tenant Provisioning Service"]
  Codebase size:            [e.g., 8 files, ~1,200 lines]
  Language + framework:     [e.g., Python 3.12 + FastAPI 0.110]
  Test suite baseline:      [e.g., 24 tests, 78% coverage, all passing]
  CI pipeline:              [e.g., GitHub Actions — lint, test, scan]
  Deployment method:        [e.g., blue/green on EKS, 5-minute deploy time]
  Rollback capability:      [e.g., instant — feature flag / previous image]

FINDINGS INPUT:
  (Paste the complete findings table from the Validation Session, Prompt C)
  Include: ID, Severity, Category, Location, Description

  Example format:
  C1 | CRITICAL | Tenant isolation   | service.py:47      | [description]
  C2 | CRITICAL | SQL injection       | repository.py:112  | [description]
  C3 | CRITICAL | Missing auth check  | router.py:23       | [description]
  H1 | HIGH     | Plaintext secret    | config.py:8        | [description]
  H2 | HIGH     | N+1 query          | repository.py:67   | [description]
  H3 | HIGH     | No rate limiting    | router.py:all      | [description]
  M1 | MEDIUM   | Missing audit log   | service.py:89      | [description]
  M2 | MEDIUM   | Unhandled timeout   | client.py:34       | [description]
  M3 | MEDIUM   | PII in logs        | service.py:201     | [description]

CURRENT CODEBASE:
  (Paste all files in the module — complete, unmodified)
  [file: service.py]      [paste full file]
  [file: repository.py]   [paste full file]
  [file: router.py]       [paste full file]
  [file: config.py]       [paste full file]
  [file: client.py]       [paste full file]
  [file: schemas.py]      [paste full file]
  [file: tests/...]       [paste all test files]

CONSTRAINTS ON FIXES:
  No-go zones:            [files or functions that MUST NOT be modified
                           without a separate approval — e.g., migration files,
                           shared auth middleware owned by another team]
  Dependency freeze:      [no new libraries may be added / or: approved list]
  Style contract:         [PEP8 / ESLint config / gofmt — enforced in CI]
  API surface freeze:     [public API contracts must not change / or: version bump allowed]
  Test coverage floor:    [coverage must not drop below X% after fixes]
  Deploy window:          [e.g., fixes must be deployable in one atomic release /
                           or: can be shipped in up to 3 sequential releases]

════════════════════════════════════════════════════════════
PHASE 0 — PRE-WORK (COUNCIL EXECUTES BEFORE ANY CODE IS WRITTEN)
════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
🔍 RESEARCHER — Dependency & Conflict Intelligence
─────────────────────────────────────────────────────────────
Before workstreams begin, map every finding's dependencies:

  FINDING DEPENDENCY GRAPH:
    For each finding pair, determine:
    □ INDEPENDENT — fixes touch disjoint code, can run fully in parallel
    □ SEQUENTIAL — fix B requires fix A to be merged first (state why)
    □ CONFLICTING — fixes touch the same lines; one must be rebased onto
      the other after merge (identify which is the base)
    □ AMPLIFYING — fixing A makes B easier or unnecessary (state why)

    Produce a complete dependency matrix:
    [Finding] → [depends on] → [conflicts with] → [amplifies]

  SHARED SURFACE AUDIT:
    Identify every shared utility, base class, middleware, or constant
    that more than one finding's fix will need to modify.
    For each shared surface:
    — Which workstream owns the change?
    — What interface contract must other workstreams code against?
    — What is the stub/mock that non-owner workstreams use until
      the owner's fix is merged?

  REGRESSION RISK MAP:
    For each fix, list every test that currently passes but is at risk
    of being broken by that fix. This becomes the targeted re-run list
    for each workstream's CI check.

─────────────────────────────────────────────────────────────
🗺️ STRATEGIST — Workstream Design & Parallel Execution Plan
─────────────────────────────────────────────────────────────
Using the Researcher's dependency graph, design the workstreams:

  WORKSTREAM ASSIGNMENT:
    Group findings into workstreams where all findings within a stream
    can be fixed by modifying a coherent, non-overlapping set of files.
    Every finding must belong to exactly one workstream.
    No workstream should require another workstream's changes to compile.

    WORKSTREAM TEMPLATE:
    ┌─────────────────────────────────────────────────────┐
    │ WORKSTREAM [ID]: [Name — e.g., "Auth & Isolation"]  │
    │ Agent Owner:     [e.g., 🔧 Implementer — Track 1]  │
    │ Findings:        [C1, C3, H3]                       │
    │ Files modified:  [router.py, service.py]            │
    │ Files read-only: [repository.py, config.py]         │
    │ Depends on:      [none / Workstream B must merge    │
    │                   before this workstream starts]    │
    │ Shared surface:  [auth_context utility — this WS    │
    │                   owns changes; WS-B stubs against  │
    │                   the new interface]                │
    │ Estimated lines  │
    │ changed:         [~45 lines]                        │
    └─────────────────────────────────────────────────────┘

  PARALLEL EXECUTION TIMELINE:
    Produce a Gantt-style execution order:

    T=0 (All streams start simultaneously):
      WS-A: [Auth & Isolation fixes] ─────────────────→ done at T=2
      WS-B: [Data Layer fixes]       ─────────────────→ done at T=3
      WS-C: [Config & Secrets fixes] ──────→ done at T=1
      WS-D: [Observability fixes]    ────────────────→ done at T=2

    T=1 (WS-C merges first — others rebase):
      WS-A: rebase onto WS-C merge ── continue ──────→ done at T=2
      WS-B: rebase onto WS-C merge ── continue ──────→ done at T=3

    T=2 (WS-A and WS-D merge):
      WS-B: rebase onto WS-A+D merges ── finalize ──→ done at T=3

    T=3: All workstreams merged → integration test run → deploy

  MERGE ORDER & REBASE PROTOCOL:
    Define the exact merge sequence. For each merge:
    — What is the target branch?
    — What automated checks must pass before merge is allowed?
    — Who is the human approver (if applicable)?
    — What is the rollback action if this merge breaks CI?

  INTERFACE CONTRACTS (pre-agreed before code is written):
    For every shared surface identified by the Researcher:
    Define the exact function signature, type, or schema that all
    workstreams will code against — even if the implementation
    doesn't exist yet.

    Example:
    CONTRACT: get_tenant_context(request: Request) → TenantContext
      TenantContext.tenant_id: UUID     [always present, from JWT]
      TenantContext.user_id: UUID       [always present, from JWT]
      TenantContext.roles: list[str]    [always present, from JWT]
      TenantContext.is_admin: bool      [derived, not from JWT directly]

    WS-A will implement this. WS-B and WS-D will import it.
    Until WS-A merges, WS-B and WS-D use this stub:
    [provide exact stub code]

════════════════════════════════════════════════════════════
PHASE 1 — PARALLEL EXECUTION (ALL WORKSTREAMS RUN SIMULTANEOUSLY)
════════════════════════════════════════════════════════════

Each workstream below is executed in full by the Implementer agent,
operating as multiple parallel instances. Each instance has full
context of its assigned findings, its files, and the interface
contracts it must honor. Each instance is unaware of the other
instances' internal implementation — only their contracts.

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — WORKSTREAM A
─────────────────────────────────────────────────────────────
Assigned findings: [e.g., C1, C3, H3 — Auth, Isolation, Rate Limiting]
Files you may modify: [e.g., router.py, service.py]
Files you must NOT modify: [e.g., repository.py, config.py]
Interface contracts you own: [list them — implement these exactly]
Interface contracts you consume: [list stubs you code against]

FOR EACH ASSIGNED FINDING:

  FINDING [ID]:
    Description:        [from findings table]
    Root cause:         [why this vulnerability exists — not just what]
    Fix strategy:       [the approach — why this fix and not another]

    BEFORE (vulnerable code):
    [exact code being replaced — file:line citation]

    AFTER (fixed code):
    [complete replacement — no placeholders, no TODOs]

    UNIT TEST FOR THIS FIX:
    [test that passes with fix, fails without it — proves the fix works
     and will catch regression if fix is reverted]

    INTEGRATION TEST (if applicable):
    [end-to-end test that confirms the fix holds under realistic conditions]

    SIDE EFFECTS:
    [any behavior that changes for existing callers as a result of this fix —
     even if the API surface is preserved, document behavioral changes]

    MIGRATION REQUIRED:
    [yes/no — if yes, provide complete migration script]

  FINDING [ID]:
    [repeat structure for every finding in this workstream]

WORKSTREAM A — FINAL DELIVERABLE:
  □ Complete diff for every modified file (before/after, full file)
  □ All new and modified tests — runnable, no mocks that hide real behavior
  □ Updated .env.example if any new environment variables introduced
  □ Changelog entry for this workstream's changes
  □ Confirmation that all interface contracts owned by this WS are
    implemented exactly as specified in Phase 0

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — WORKSTREAM B
─────────────────────────────────────────────────────────────
Assigned findings: [e.g., C2, H2 — SQL Injection, N+1 Query]
Files you may modify: [e.g., repository.py]
Files you must NOT modify: [e.g., service.py, router.py]
Interface contracts you own: [list]
Interface contracts you consume: [list — use stubs until owner merges]

  [Repeat the per-finding structure from Workstream A for every finding
   assigned to this workstream]

WORKSTREAM B — FINAL DELIVERABLE:
  [Same checklist as Workstream A]

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — WORKSTREAM C
─────────────────────────────────────────────────────────────
Assigned findings: [e.g., H1 — Plaintext Secrets in config.py]
Files you may modify: [e.g., config.py, .env.example]
Files you must NOT modify: [all others]
Interface contracts you own: [list]
Interface contracts you consume: [list]

  [Repeat the per-finding structure]

WORKSTREAM C — FINAL DELIVERABLE:
  [Same checklist]

─────────────────────────────────────────────────────────────
🔧 IMPLEMENTER — WORKSTREAM D
─────────────────────────────────────────────────────────────
Assigned findings: [e.g., M1, M2, M3 — Audit Logging, Timeouts, PII in Logs]
Files you may modify: [e.g., service.py, client.py]
Files you must NOT modify: [router.py, repository.py]
Interface contracts you own: [list]
Interface contracts you consume: [list]

  [Repeat the per-finding structure]

WORKSTREAM D — FINAL DELIVERABLE:
  [Same checklist]

(Add Workstream E, F, etc. as needed based on finding count and
file ownership boundaries. A healthy workstream contains 2–5 findings.
Never create a workstream with a single trivial finding — group by file
ownership, not by finding count.)

════════════════════════════════════════════════════════════
PHASE 2 — INTEGRATION (SEQUENTIAL, AFTER ALL WORKSTREAMS DELIVER)
════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
🔎 CRITIC — Merge Conflict & Interface Integrity Audit
─────────────────────────────────────────────────────────────
After all workstreams have delivered their code, before any merge:

  INTERFACE CONTRACT VERIFICATION:
    For every contract defined in Phase 0:
    □ Does the owner workstream implement it exactly as specified?
    □ Do all consumer workstreams code against the correct signature?
    □ Are there any type mismatches, missing fields, or semantic gaps
      between what the owner implemented and what consumers expect?

  MERGE CONFLICT PREDICTION:
    Given all workstream diffs, predict every line-level conflict
    that will occur during the merge sequence defined by the Strategist.
    For each predicted conflict:
    — File and approximate line range
    — Which workstream's version should win and why
    — What the manually resolved version should look like

  BEHAVIORAL REGRESSION AUDIT:
    Compare the combined effect of all workstream fixes against the
    original codebase. Identify any case where two individually correct
    fixes combine to produce incorrect behavior:
    — Fix A changes how tenantId is passed to the repository
    — Fix B changes how the repository validates tenantId
    — Together: does the validation still work correctly end-to-end?

  INVARIANT CHECK:
    Confirm that the following invariants hold across all fixes combined:
    □ No new code path exists that bypasses auth
    □ No new code path exists that omits tenant_id from a DB query
    □ No new code introduces a logging statement that captures PII
    □ No new code adds a hardcoded secret or credential
    □ Test coverage has not decreased from the baseline stated in the brief

─────────────────────────────────────────────────────────────
😈 DEVIL'S ADVOCATE — The Fix Introduced a New Bug
─────────────────────────────────────────────────────────────
Argue, with full conviction, that at least one of the fixes is wrong:

  FIX THAT INTRODUCED A REGRESSION:
    Identify the fix most likely to have introduced a subtle regression
    that the workstream's own tests would not catch.
    Construct the specific test case that would expose it.
    Provide the corrected implementation.

  FIX THAT IS INCOMPLETE:
    Identify the fix that addresses the symptom but not the root cause.
    The same vulnerability class will re-emerge within 6 months because
    [specific reason — architectural, not cosmetic].
    State what the complete fix would require.

  FIX THAT CREATES A NEW ATTACK SURFACE:
    Identify any fix that, in closing one vulnerability, opens a new one.
    (Common example: adding rate limiting by IP address in a system
    behind a load balancer that forwards a single proxy IP — the fix
    effectively rate-limits no one, or rate-limits everyone.)
    Provide the corrected implementation.

  FIX THAT WILL BREAK UNDER LOAD:
    Identify the fix that works correctly in unit tests and under normal
    conditions but will fail, degrade, or produce incorrect behavior
    under concurrent load or at scale.
    Describe the failure mode precisely.
    Provide the corrected implementation.

─────────────────────────────────────────────────────────────
⚖️ ETHICIST — Remediation Side-Effect Assessment
─────────────────────────────────────────────────────────────
Evaluate whether any fix, in solving a technical problem, creates
an ethical or user-harm problem:

  USER IMPACT AUDIT:
    For each fix that changes observable behavior (error messages,
    response times, data availability, access controls):
    — Does this change create a worse experience for any user group?
    — Does stricter input validation reject legitimate inputs from
      users with non-standard data (international characters, edge-case
      formats, assistive technology outputs)?
    — Does added rate limiting disproportionately impact lower-bandwidth
      users or regions?

  DATA DELETION COMPLETENESS:
    If any fix modifies how data is stored or structured:
    — Does the existing data deletion procedure still work correctly?
    — Are there any data records that can no longer be deleted as a
      result of the new schema or structure?

  AUDIT TRAIL CONTINUITY:
    If any fix modifies logging or audit behavior:
    — Is there a gap in the audit log between the old behavior and
      the new behavior?
    — Could that gap be exploited to perform unlogged actions during
      a deployment window?

─────────────────────────────────────────────────────────────
✅ FACT-CHECKER — Fix Verification & Test Validity
─────────────────────────────────────────────────────────────
For every fix delivered by every workstream:

  VERIFY EACH FIX:
    □ The fix actually addresses the root cause stated in the finding,
      not just the symptom described in the location field
    □ The fix does not use a deprecated API in the specified framework
      version
    □ The test written to verify the fix would actually fail without
      the fix in place (check for trivially-passing tests that never
      exercise the vulnerable code path)
    □ The fix is complete — there is no other location in the codebase
      where the same vulnerability pattern exists that this fix does
      not address
    □ The fix's behavior matches the interface contract it is supposed
      to implement or consume

  CROSS-WORKSTREAM COVERAGE CHECK:
    Produce a final coverage map:
    For each finding in the original findings table:
    — Is it addressed? By which workstream and file?
    — Is it fully addressed or partially addressed?
    — Is there a corresponding test that would catch a regression?

  CONFIDENCE RATING PER FIX:
    HIGH — fix is complete, test is valid, no side effects identified
    MEDIUM — fix is correct but [specific condition] should be monitored
    LOW — fix is incomplete or [specific aspect] requires human review

════════════════════════════════════════════════════════════
PHASE 3 — DEPLOYMENT (COUNCIL-SUPERVISED RELEASE)
════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
🧠 ORCHESTRATOR — Merge Sequence, Deployment Plan & Closure
─────────────────────────────────────────────────────────────
You have all workstream outputs, the Critic's conflict analysis,
the Devil's Advocate's regression findings, the Ethicist's
side-effect assessment, and the Fact-Checker's coverage map.
Now execute the final synthesis.

  BLOCKING ITEMS RESOLUTION:
    List every issue raised by Phase 2 agents that requires a code
    change before the merge sequence can begin.
    For each:
    Issue:          [description]
    Raised by:      [agent]
    Assigned to:    [workstream]
    Resolution:     [exact code fix — no placeholders]
    Verified by:    [fact-checker sign-off criterion]

  FINAL MERGE SEQUENCE:
    Execute the merge plan defined by the Strategist, updated
    to reflect any blocking items resolved above.

    MERGE 1: Workstream [C] → main
      Pre-merge checks:  [lint ✓, unit tests ✓, no coverage drop ✓]
      Predicted conflicts: [none]
      Post-merge action:  [trigger CI, confirm green before proceeding]

    MERGE 2: Workstream [A] rebased onto post-C main → main
      Pre-merge checks:  [lint ✓, unit tests ✓, integration tests ✓]
      Predicted conflicts: [config.py line 8 — resolved in favor of WS-A]
      Post-merge action:  [trigger CI + security scan]

    MERGE 3: Workstream [D] rebased onto post-A main → main
      Pre-merge checks:  [all checks ✓]
      Predicted conflicts: [service.py lines 89–95 — provide exact resolution]
      Post-merge action:  [trigger full test suite + coverage report]

    MERGE 4: Workstream [B] rebased onto post-D main → main
      Pre-merge checks:  [all checks ✓]
      Predicted conflicts: [repository.py — provide exact resolution]
      Post-merge action:  [trigger full suite + deploy to staging]

  DEPLOYMENT PROTOCOL:
    Stage 1 — Staging:
      □ Run full integration test suite against staging environment
      □ Run OWASP ZAP or equivalent automated scan against staging
      □ Manually verify the top 3 CRITICAL findings are no longer
        reproducible using the original attack method
      □ Confirm all audit log entries are correctly emitted for
        the operations covered by M1 fix
      □ Confirm PII scrubbing is active in logs for M3 fix

    Stage 2 — Canary (5% traffic):
      □ Monitor error rate — rollback trigger: >0.5% error rate increase
      □ Monitor p95 latency — rollback trigger: >20% increase sustained
        for more than 2 minutes
      □ Monitor tenant isolation alarms — rollback trigger: any single
        cross-tenant data access event detected
      □ Hold canary for: [e.g., 30 minutes / 1 business hour / 24 hours
        depending on risk profile of changes]

    Stage 3 — Full Production:
      □ All canary checks passed
      □ On-call engineer confirmed available for 2 hours post-deploy
      □ Rollback command documented and tested in staging:
        [exact rollback command or procedure]

  FINAL FINDINGS CLOSURE TABLE:
    | ID | Severity | Finding | Workstream | Fix File | Test | Merged | Verified |
    |----|----------|---------|------------|----------|------|--------|----------|
    | C1 | CRITICAL | ...     | WS-A       | service  | ✓    | Merge2 | ✓        |
    | C2 | CRITICAL | ...     | WS-B       | repo     | ✓    | Merge4 | ✓        |
    | C3 | CRITICAL | ...     | WS-A       | router   | ✓    | Merge2 | ✓        |
    | H1 | HIGH     | ...     | WS-C       | config   | ✓    | Merge1 | ✓        |
    | H2 | HIGH     | ...     | WS-B       | repo     | ✓    | Merge4 | ✓        |
    | H3 | HIGH     | ...     | WS-A       | router   | ✓    | Merge2 | ✓        |
    | M1 | MEDIUM   | ...     | WS-D       | service  | ✓    | Merge3 | ✓        |
    | M2 | MEDIUM   | ...     | WS-D       | client   | ✓    | Merge3 | ✓        |
    | M3 | MEDIUM   | ...     | WS-D       | service  | ✓    | Merge3 | ✓        |

  POST-DEPLOYMENT MONITORING WINDOW:
    Duration:     [e.g., 48 hours on-call heightened watch]
    Key signals:
      □ Zero cross-tenant data access events in security logs
      □ Auth failure rate within normal baseline (±15%)
      □ No new ERROR-level log entries in affected files
      □ External API call latency within 10% of pre-deploy baseline
      □ DB query execution time within 10% of pre-deploy baseline

  INCIDENT RESPONSE — IF SOMETHING BREAKS POST-DEPLOY:
    If rollback is required:
      1. Execute rollback command: [exact command]
      2. Confirm traffic returned to previous image: [verification step]
      3. Open incident channel: [e.g., #incidents-production]
      4. Post-mortem trigger: within 48 hours, review which workstream's
         fix caused the regression and why the Phase 2 audit missed it

    If partial rollback is required (only some fixes caused problems):
      Define the per-workstream rollback plan — since each workstream
      was merged as a discrete commit, individual reverts are possible:
      WS-A revert: [git revert command for merge 2]
      WS-B revert: [git revert command for merge 4]
      WS-C revert: [git revert command for merge 1]
      WS-D revert: [git revert command for merge 3]
      Rebase order after partial revert: [re-state the merge sequence
      with the reverted workstream removed]

  COUNCIL SESSION CLOSURE:
    □ All CRITICAL findings: CLOSED
    □ All HIGH findings: CLOSED
    □ All MEDIUM findings: CLOSED or DEFERRED with owner + deadline
    □ Test coverage: at or above baseline
    □ CI pipeline: all checks green on main
    □ Deployment: confirmed stable in production
    □ ADR updated: parallel fix session outcome documented
    □ Next Validation Session: scheduled for [date / milestone]

  LESSONS LEARNED FOR NEXT PARALLEL SESSION:
    What did the dependency graph reveal that a serial fix process
    would have discovered too late (after merge conflicts, after
    deployment, after regression)?
    What workstream boundary decision made the merge sequence smoother
    or harder than expected?
    What should the next team running this prompt do differently?
```

---

## PARALLEL SESSION OPERATING RULES

### The Three Laws of Parallel Fixes

**Law 1 — Contracts Before Code.**
No workstream writes a single line of implementation until all interface
contracts between workstreams are fully specified and agreed. A contract
is a function signature, type definition, or schema — not a description
of intent. If two workstreams share a boundary and the contract is
ambiguous, the Orchestrator resolves it before T=0. This is non-negotiable.
Ambiguous contracts produce merge conflicts. Merge conflicts under deadline
pressure produce bugs.

**Law 2 — Own Your Files. Borrow Nothing.**
Each workstream has a defined set of files it may modify. It may read any
file. It may not write to a file owned by another workstream, even if the
change seems trivial. If a fix requires changing a file owned by another
workstream, that fix is either reassigned to the owning workstream or
escalated to the Orchestrator to redefine ownership boundaries. There are
no exceptions. Shared file ownership is not coordination — it is collision
in slow motion.

**Law 3 — The Devil's Advocate Is Always Right Until Proven Wrong.**
Any regression, incomplete fix, or new attack surface identified by the
Devil's Advocate is treated as confirmed until the Fact-Checker explicitly
refutes it with evidence. The burden of proof is on the workstream that
delivered the fix, not on the agent who challenged it. If the Fact-Checker
cannot confirm a fix is complete with HIGH confidence, that finding remains
OPEN and blocks the merge sequence for that workstream.

---

### When to Collapse Workstreams

If fewer than 5 findings exist, do not run parallel workstreams.
Run a single 🔧 Implementer session with the full findings list, then
run the Phase 2 agents (Critic, Devil's Advocate, Fact-Checker) as a
sequential review. Parallel infrastructure has overhead. Overhead on a
2-finding fix is waste.

**Parallel is justified when:**
- 6 or more findings across 3 or more files
- At least 2 findings are in files with no shared lines
- Team has capacity to review multiple PRs simultaneously
- Deploy window permits staged merges (not a single hotfix)

**Collapse to serial when:**
- All findings are in a single file
- Findings have a strict sequential dependency chain
- Hotfix is required within 2 hours (overhead cannot be justified)
- The codebase is too small for parallel branches to be meaningful

---

*Parallel execution without parallel discipline is just simultaneous chaos.*
*The Council runs in parallel. The contracts run first.*
