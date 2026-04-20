# Citadel SaaS Factory — .claude/ Intelligence Layer

> This file extends the root [CLAUDE.md](../CLAUDE.md) with .claude/-specific context.
> The root CLAUDE.md is the project constitution. This file covers the intelligence layer only.

## Intelligence Layer Structure

```
.claude/
├── agents/                    ← 500+ agent definitions across 30 domains
│   ├── _registry.yaml         ← master registry (id, domain, model, enabled, entrypoint)
│   ├── executive/             ← 18 agents (CEO Strategist, CTO, CFO, OKR, Board, M&A, etc.)
│   ├── marketing/             ← 28 agents (SEO, Content, Social, Email, PPC, PLG, ABM, etc.)
│   ├── sales/                 ← 24 agents (Lead Qualifier, Proposals, CRM, Deal Desk, etc.)
│   ├── customer-success/      ← 20 agents
│   ├── product-design/        ← 26 agents
│   ├── engineering/           ← 35 agents
│   ├── frontend/              ← 24 agents
│   ├── devops/                ← 34 agents
│   ├── security/              ← 28 agents
│   ├── data-analytics/        ← 24 agents
│   ├── qa-testing/            ← 28 agents
│   ├── hr-people/             ← 16 agents
│   ├── finance/               ← 20 agents
│   ├── legal/                 ← 14 agents
│   ├── content/               ← 16 agents
│   └── (standalone agents)    ← api-tester, code-reviewer, deploy-agent, etc.
├── commands/                  ← slash commands (34 total)
│   ├── deploy.md, review.md, test.md, plan.md, debug.md
│   ├── security-review.md, guardrails.md, simplify.md
│   ├── wiki-ingest.md, wiki-query.md, wiki-lint.md, vault-link.md
│   └── *.yaml (audit, backup, build, cert, lint, logs, migrate, etc.)
├── hooks/                     ← lifecycle scripts (11 total)
│   ├── pre-commit.sh, pre-push.sh
│   ├── pre-agent.sh, post-agent.sh
│   ├── pre-deploy.sh, post-deploy.sh
│   ├── on-file-change.sh, on-error.sh, on-test-fail.sh
│   ├── on-deploy-fail.sh, on-security-alert.sh
│   └── vault-autolink.sh
├── rules/                     ← 23 coding standards
│   ├── code-quality.md, architecture.md, api-design.md
│   ├── testing.md, security.md, secrets.md
│   ├── database.md, frontend.md, devops.md
│   ├── naming.md, error-handling.md, performance.md
│   ├── monitoring.md, documentation.md, dependencies.md
│   ├── accessibility.md, review.md, git.md
│   ├── guardrails.md, llm-wiki.md, obsidian-backlinks.md
│   └── (each rule is self-contained with enforcement details)
├── skills/                    ← specialist capabilities
│   ├── code-review/SKILL.md, testing/SKILL.md
│   ├── guardrails/SKILL.md, llm-wiki/SKILL.md
│   ├── obsidian-linker/SKILL.md, graphify/SKILL.md
│   ├── deploy/SKILL.md, onboard/SKILL.md
│   ├── database-migration/SKILL.md, security-audit/SKILL.md
│   └── (14 standalone .md skills: api-design, debugging, etc.)
├── memory/                    ← persistent project memory
│   ├── project-context.md, architecture-decisions.md
│   ├── agent-learnings.md, error-patterns.md
│   ├── deployment-history.md, team-preferences.md
│   └── (append-only, survives across sessions)
├── mcp/                       ← 8 MCP server configs
│   ├── github.json, postgres.json, docker.json
│   ├── kubernetes.json, filesystem.json, redis.json
│   ├── vault.json, prometheus.json
│   └── (enable by adding to .mcp.json at root)
├── templates/                 ← 20 code generation templates
│   ├── api-endpoint.py.tmpl, model.py.tmpl, service.py.tmpl
│   ├── component.tsx.tmpl, page.tsx.tmpl, hook.ts.tmpl
│   ├── test-unit.py.tmpl, test-e2e.ts.tmpl
│   ├── dockerfile.yml.tmpl, github-action.yml.tmpl
│   ├── terraform-module.tf.tmpl, helm-values.yaml.tmpl
│   └── migration.py.tmpl, worker.py.tmpl, schema.py.tmpl
└── settings.json              ← hooks, permissions, model routing
```

## Agent Registry Schema

Each agent in `_registry.yaml` follows:

```yaml
- id: <domain-role>
  domain: <one of 30 domains>
  role: "<short description>"
  model: claude-sonnet-4-6 | claude-haiku-4-5 | claude-opus-4-7
  enabled: true | false
  entrypoint: .claude/agents/<domain>/<id>.md
  skills_required: [...]
  mcp_required: [...]
```

## Hook Execution Order

1. `pre-agent.sh` → before any agent spawns
2. `pre-commit.sh` → before git commit (secret scan, lint, test)
3. `pre-push.sh` → before git push
4. `pre-deploy.sh` → before deployment
5. `post-deploy.sh` → after deployment
6. `post-agent.sh` → after agent completes
7. `on-error.sh` → on any error
8. `on-test-fail.sh` → on test failure
9. `on-deploy-fail.sh` → on deploy failure
10. `on-security-alert.sh` → on security finding
11. `vault-autolink.sh` → after writing to docs/vault/

## Settings (settings.json)

- PreToolUse hooks: lint Python (ruff), lint TypeScript (eslint), LLM Wiki reminder
- PostToolUse hooks: format Python (ruff), format TypeScript (prettier), vault autolink
- Permissions: allow standard tools, deny reading .env files and writing production configs
