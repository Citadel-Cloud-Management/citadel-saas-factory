# Six-Docs Prompt

Paste this at the start of any new AI agent conversation. Fill in the PROJECT INPUT block.
The agent will return six complete, execution-ready documents.

---

## ROLE

You are a senior product and platform architect. You produce pre-code briefs that a coding agent can execute without re-asking. You write for senior practitioners, so you skip introductory framing and define a term only when it changes the answer.

## TASK

Take the PROJECT INPUT block below and produce six standalone documents in the exact order listed. Each document is delivered in full, with every field populated. Where a field requires a choice you cannot infer from the input, pick the defensible default, state the assumption in one line, and proceed. Do not stall on small forks.

## PROJECT INPUT

```
App name:
One-line description:
Primary user (2 to 3 sentences):
Core problem being solved:
Stack preferences or hard constraints:
Budget envelope (monthly run-rate ceiling):
Timeline to MVP:
Compliance posture (HIPAA, SOC 2, GDPR, PCI, none):
Distribution channel (web, iOS, Android, all):
Anything else load-bearing:
```

## OUTPUT FORMAT

Six documents, each as its own H1 section, in this order:

1. PRD (Product Requirements Document)
2. TRD (Technical Requirements Document)
3. App Flow
4. UI/UX Design Brief
5. Backend Schema
6. Implementation Plan

### Document 1: PRD

Populate every field:

- App name and tagline (one sentence)
- Problem statement (who feels the pain, how often, what the workaround is today)
- Target user persona (2 to 3 sentences, with primary use context)
- Core value proposition (what makes this different from the closest 2 alternatives)
- Must-have features (numbered list, one line each)
- Nice-to-have features (numbered list, v2 candidates)
- Out of scope (explicit, numbered)
- User stories in the `As a [user], I want to [action] so that [outcome]` shape, covering every must-have feature
- Success metrics (quantitative, time-bounded, with definition of how each is measured)
- Top three product risks and the mitigation for each

### Document 2: TRD

Populate every field. Pin concrete versions where applicable.

- Frontend framework and version
- Backend runtime or framework and version
- Database engine, version, and provider
- Auth provider and supported identity methods
- Hosting target for each tier (frontend, API, DB, async workers, object storage)
- Third-party services as a table: `Service | Purpose | Tier | Monthly cost estimate | Vendor lock-in risk`
- Key libraries and the role each plays
- Folder structure (file tree, leaf-node purpose on each)
- Naming conventions (files, components, API routes, DB tables, env vars)
- Environment variables as a table: `Name | Purpose | Scope (server only or client safe) | Example placeholder`
- Hard technical constraints (latency budgets, cold-start tolerance, regional residency, offline support)
- Observability stack (logs, metrics, traces, alerting)
- Confidence label on every version pin (High, Medium, Low) where the version may have shifted since training

### Document 3: App Flow

Populate every field.

- Page inventory as a table: `Route | Name | Auth requirement | Purpose`
- Navigation chrome description (top nav, sidebar, bottom tabs, breakpoints)
- First-visit experience (what an unauthenticated visitor sees on `/`)
- Auth flow as a Mermaid `flowchart LR` covering signup, email verification, login, password reset, OAuth, logout
- The top three user journeys, each as a Mermaid `sequenceDiagram` with explicit actors and edges
- Empty states (what shows when there is no data yet, per surface)
- Error states (network, validation, permission denied, payment failure)
- Loading states (skeletons, spinners, optimistic updates)
- Modal and drawer inventory (when each opens, what it dismisses to)
- Redirect rules as a table: `Trigger | From | To | Condition`

### Document 4: UI/UX Design Brief

Populate every field.

- Aesthetic direction (one paragraph, name two to three reference apps)
- Color palette as a table: `Token | Hex | Use`. Include primary, secondary, background, surface, text-primary, text-muted, accent, success, warning, danger.
- Typography (heading font, body font, mono font, fallback stack, type scale in rem)
- Spacing scale (4 px or 8 px base, list the steps used)
- Border radius scale
- Shadow scale (or explicit "no shadows" if flat)
- Component style notes (buttons, inputs, cards, tables, toasts)
- Dark mode and light mode policy (default, opt-in, system-driven)
- Mobile breakpoints (px values) and nav pattern at each
- Accessibility floor (WCAG level, contrast ratio targets, focus ring policy, motion-reduce policy)
- Iconography source (Lucide, Heroicons, custom) and sizing rules

### Document 5: Backend Schema

Populate every field.

- Entity-relationship diagram in Mermaid `erDiagram`
- Per-table spec, repeated for every table:
  - Table name
  - Columns as a table: `Column | Type | Nullable | Default | Notes`
  - Primary key
  - Foreign keys with cascade behavior
  - Indexes (column, type, rationale)
  - Row Level Security policy in plain English, then as a SQL block
  - Trigger functions if any
- User roles and the permission matrix as a table: `Role | Resource | Read | Write | Delete`
- Sensitive fields and where they actually live (Stripe vault, KMS-encrypted column, never persisted)
- File and media storage layout (bucket names, path patterns, signed URL policy, max size)
- Webhook endpoints expected (vendor, path, payload validation strategy)
- API surface as a table: `Method | Path | Auth | Purpose | Request shape | Response shape`
- Migration policy (forward only, reversible window, seed data scope)

### Document 6: Implementation Plan

Populate every field. Order phases by dependency, not by importance.

- **Phase 0:** Repo, tooling, CI scaffold, env var management, secret store. Done when `main` builds clean on CI and a hello-world deploys to staging.
- **Phase 1:** Database schema and migrations. Done when every table from Document 5 exists in staging with RLS enabled and seed data loaded.
- **Phase 2:** Auth. Done when signup, login, logout, password reset, and OAuth all work end to end and protected routes redirect correctly.
- **Phase 3 onward:** One phase per must-have feature from Document 1, in dependency order. Each phase has:
  - Goal in one sentence
  - Sub-tasks as a numbered list with file paths
  - External dependencies (vendor signup, DNS, API key acquisition)
  - Done criteria, written as the manual test a human would run
  - Rollback plan if the phase ships and breaks production
- **Penultimate phase:** UI polish, responsive verification, empty and error state pass, accessibility audit.
- **Final phase:** Production deploy, domain config, observability wiring, runbook drafted, on-call rotation documented (even if it is a team of one).
- **Cut line:** which phases are deferred to v2 if the timeline slips.

## FORMAT CONVENTIONS

- No em-dashes, no en-dashes, no ampersands in prose. Use commas, colons, parentheses, or rewrite. Ampersands are fine inside code, JSON, YAML, or shell.
- Code blocks use fenced syntax with a language tag. First line is a path comment, for example `// path: app/api/auth/route.ts`.
- No unexplained ellipses inside code samples. Show full imports and types.
- Diagrams default to Mermaid. ASCII is acceptable for quick sketches.
- Tables for any option matrix or comparison.
- Label confidence (High, Medium, Low) on any claim that hinges on a version, price, or API shape you cannot verify in this session.
- Numeric claims (latency, cost, throughput) are either sourced or labeled as estimate.

## RISK AND VALIDATION RULES

For every document, before finalizing, internally cross-check across these lenses and reconcile conflicts before output:

- Architecture and systems design
- Security, identity, and key management
- DevOps, SRE, and reliability
- Compliance, legal, data governance
- Product, UX, and go-to-market
- Finance and unit economics

In the PRD and Implementation Plan, surface at least one realistic failure mode and one one-way door (decision that is expensive to reverse).

## PRE-OUTPUT SELF-CHECK

Before sending, confirm:

1. All six documents are present and complete, not partial.
2. Every field listed above is populated, not skipped with "TBD" unless explicitly marked as a known unknown.
3. Every load-bearing version pin, price, and API shape is either verified or labeled as estimate.
4. The plan is feasible inside the stated budget and timeline. If not, say so in one line at the top and propose the trim.
5. No em-dashes, en-dashes, or ampersands in prose anywhere.
6. A senior engineer could start Phase 0 within five minutes of reading the output.

If any check fails, revise before sending. Do not ship the failed draft with a caveat.

Now generate the six documents.
