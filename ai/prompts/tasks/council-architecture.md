---
name: council-architecture
version: "1.0.0"
model: claude-opus-4-7
description: "Council Prompt A: Nine-agent adversarial architecture session for production SaaS system design. Produces ADR, phased roadmap, component map, and risk register."
input_variables:
  - product_name
  - core_problem
  - primary_persona
  - secondary_persona
  - business_model
  - target_segment
  - deal_size
  - compliance_exposure
  - data_sensitivity
  - cloud_provider
  - preferred_regions
  - team_size
  - existing_stack
  - existing_data
  - launch_users
  - month_6_target
  - month_18_target
  - peak_load_pattern
  - data_volume
  - core_modules
  - sso_providers
  - third_party_apis
  - webhooks_required
  - data_export_needs
  - timeline_to_mvp
  - budget_sensitivity
  - must_have_at_launch
  - deliberately_deferred
tags: [council, architecture, system-design, adversarial-review]
source_ref: ai/data/processed/council-agents-saas-prompts.md
---

You are convening a Council of nine specialized AI agents to design
a production-grade SaaS system. Each agent must speak from their
distinct cognitive role. Do not collapse into consensus prematurely.
Let the tension between agents produce a better answer than any single
perspective could.

This is not a brainstorm. This is a structured adversarial review
that ends in a synthesized, actionable, opinionated recommendation.

================================================================
PRODUCT BRIEF
================================================================

PRODUCT IDENTITY:
  Name:                   {{product_name}}
  Core problem solved:    {{core_problem}}
  Primary user persona:   {{primary_persona}}
  Secondary persona:      {{secondary_persona}}
  Business model:         {{business_model}}

CUSTOMER PROFILE:
  Target segment:         {{target_segment}}
  Deal size expectation:  {{deal_size}}
  Compliance exposure:    {{compliance_exposure}}
  Expected data sensitivity: {{data_sensitivity}}

TECHNICAL CONTEXT:
  Cloud:                  {{cloud_provider}}
  Preferred regions:      {{preferred_regions}}
  Team size:              {{team_size}}
  Existing stack:         {{existing_stack}}
  Existing data:          {{existing_data}}

SCALE REQUIREMENTS:
  Launch day users:       {{launch_users}}
  Month 6 target:         {{month_6_target}}
  Month 18 target:        {{month_18_target}}
  Peak load pattern:      {{peak_load_pattern}}
  Data volume:            {{data_volume}}

CORE FEATURE MODULES:
{{core_modules}}

INTEGRATION SURFACE:
  SSO providers:          {{sso_providers}}
  Third-party APIs:       {{third_party_apis}}
  Webhooks required:      {{webhooks_required}}
  Data export needs:      {{data_export_needs}}

BUSINESS CONSTRAINTS:
  Timeline to MVP:        {{timeline_to_mvp}}
  Budget sensitivity:     {{budget_sensitivity}}
  Must-have at launch:    {{must_have_at_launch}}
  Deliberately deferred:  {{deliberately_deferred}}

================================================================
COUNCIL SESSION -- BEGIN
================================================================

Now speak as each agent in sequence. Each agent must:
  1. State their role and lens
  2. Deliver their full analysis (no summaries -- full depth)
  3. Identify the 2-3 things OTHER agents will likely miss or get wrong

-----------------------------------------------------------------
RESEARCHER -- Context, Precedent & Domain Intelligence
-----------------------------------------------------------------
Surface:
  - Industry-specific architectural patterns that have succeeded or failed
    for this product type at this scale
  - Regulatory and compliance facts that will constrain architecture choices
    (cite specific requirements -- HIPAA 164.312, SOC2 CC6, GDPR Art. 17, etc.)
  - Known failure modes in similar SaaS products (with root cause if known)
  - The current best-in-class reference architectures in this space
  - Technology choices that appear valid but have known hidden costs at scale
  - Competitor infrastructure decisions visible via public postmortems,
    engineering blogs, or job descriptions

Do NOT summarize. Surface specific, actionable intelligence.

-----------------------------------------------------------------
STRATEGIST -- Structure, Sequencing & Phased Execution
-----------------------------------------------------------------
Produce:

  PHASE 1 -- Foundation (Weeks 1-4):
    What must exist before anything else can be built.
    Define: infrastructure primitives, auth skeleton, data model core,
    local dev environment, CI pipeline baseline.

  PHASE 2 -- Core Product (Weeks 5-10):
    What constitutes a usable, shippable product.
    Define: which modules to build in order, integration order,
    feature flags strategy, observability baseline.

  PHASE 3 -- Hardening (Post-MVP):
    What gets deferred without compromising MVP viability.
    Define: compliance certifications, performance optimization,
    advanced billing logic, enterprise SSO, disaster recovery.

  DECISION FRAMEWORK:
    For every major architectural fork (monolith vs. micro,
    REST vs. GraphQL, schema-per-tenant vs. row-level isolation, etc.):
    -- State the options
    -- State the decision point (when does each become right/wrong)
    -- Give a concrete recommendation for THIS product at THIS stage

  SEQUENCING RISKS:
    What happens if a team builds module B before module A is stable?
    Identify the 3 highest-risk sequencing mistakes.

-----------------------------------------------------------------
CREATIVE -- Novel Approaches & Contrarian Architecture
-----------------------------------------------------------------
Challenge the default assumptions. Propose:

  - Alternative architectural patterns the team has probably NOT considered
  - One genuinely unconventional technology choice that could give this
    product a real competitive moat if it worked -- and what would need to
    be true for it to work
  - Which "standard" SaaS patterns are actually unnecessary for this
    specific product at MVP and could be dropped without consequence
  - A DX (developer experience) innovation that would make the codebase
    dramatically easier to maintain at 18 months vs. the default approach
  - If you had to build this product in half the time with half the people,
    what would you sacrifice and what would you protect? Why?

-----------------------------------------------------------------
CRITIC -- Assumption Audit & Structural Weaknesses
-----------------------------------------------------------------
Challenge everything stated in the product brief. Specifically:

  ASSUMPTION AUDIT:
    List every implicit assumption embedded in the brief (even if unstated).
    For each: is it verified, unverified, or likely wrong?

  ARCHITECTURAL FRAGILITIES:
    Where will this design break first under real-world conditions?

  DEPENDENCY RISKS:
    Which third-party dependencies create existential risk if they change
    pricing, API, or terms of service? What is the mitigation?

  SCALING CLIFF:
    At what user/data/tenant count does the proposed architecture require
    a painful migration or rewrite? Is that cliff before or after PMF?

  TEAM RISK:
    Given the team size and composition in the brief, which parts of this
    architecture require expertise the team likely does not have?

-----------------------------------------------------------------
DEVIL'S ADVOCATE -- The Strongest Case Against This
-----------------------------------------------------------------
Argue, with full conviction, the strongest possible case that:

  1. The chosen cloud provider / architecture is WRONG for this product
  2. Multi-tenancy at MVP is a mistake. Build single-tenant first.
  3. The team is about to over-engineer something that should be a monolith.
  4. There is a simpler, cheaper, faster path to the same outcome.

Note: The Devil's Advocate is not trying to be correct. They are trying
to force the team to have answers to the hardest objections.

-----------------------------------------------------------------
ETHICIST -- Moral Exposure & Unintended Consequences
-----------------------------------------------------------------
Evaluate: DATA ETHICS, ALGORITHMIC RISK, POWER DYNAMICS,
REGULATORY EXPOSURE BEYOND COMPLIANCE, MINIMUM ETHICAL ARCHITECTURE.

-----------------------------------------------------------------
IMPLEMENTER -- Concrete Execution Blueprint
-----------------------------------------------------------------
Translate the above into an executable engineering plan:
  REPOSITORY STRUCTURE, DAY 1 CHECKLIST, INFRASTRUCTURE AS CODE,
  DATABASE MIGRATION STRATEGY, LOCAL DEVELOPMENT CONTRACT,
  DEPLOYMENT PIPELINE (exact stages), FIRST 10 API ENDPOINTS.

-----------------------------------------------------------------
FACT-CHECKER -- Accuracy Audit & Confidence Calibration
-----------------------------------------------------------------
Review every recommendation made by all preceding agents and:
  FLAG outdated tech, unverified scale claims, oversimplified compliance.
  VERIFY stack compatibility, compliance applicability, scale consistency.
  CONFIDENCE MAP: rate each recommendation HIGH / MEDIUM / LOW.

-----------------------------------------------------------------
ORCHESTRATOR -- Synthesis, Final Recommendation & Decision Log
-----------------------------------------------------------------
Synthesize: COUNCIL VERDICT, WHERE THE COUNCIL AGREED,
WHERE THE COUNCIL DISAGREED, ARCHITECTURE DECISION RECORD (10 ADRs),
RISK REGISTER (TOP 5), 90-DAY EXECUTION SUMMARY,
FIRST DECISION THE TEAM MUST MAKE.
