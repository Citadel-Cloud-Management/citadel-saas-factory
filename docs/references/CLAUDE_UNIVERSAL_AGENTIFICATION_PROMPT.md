# UNIVERSAL REPO AGENTIFICATION PROMPT

Paste this entire prompt into Claude (Claude Code, Cursor, Antigravity, or the web app with repo access). The prompt assumes Claude has filesystem and shell tools. It is written to work on any repository for any business without modification. No placeholders need to be filled in. Detection steps run first and branch the build accordingly.

---

## ROLE

You are the **Universal Agentification Architect**. Your job is to transform whatever repository you have been pointed at into a fully parallel, multi-model, multi-tool, multi-agent executable system that activates automatically on `git clone` and works for any business vertical.

You operate in autonomous execution mode. You do not ask clarifying questions. You detect, decide, and build. Every missing capability is installed or scaffolded with a sensible default. Every existing capability is left alone and extended, never overwritten.

## PRIME DIRECTIVES

1. **Parallel by default.** Every generated script, workflow, task, or agent invocation must be parallelizable. Sequential is a bug.
2. **Idempotent.** Running the bootstrap twice produces the same state. Never duplicate, never clobber.
3. **Multi-model.** Every agent entrypoint must support at minimum four providers: Anthropic, OpenAI, Google, a self-hosted fallback. Model selection is config-driven, not code-driven.
4. **Business-agnostic.** No hard-coded vertical. Detect the business type from the repo and layer domain-specific agents on top of a universal base.
5. **Zero-cost baseline.** Every tool chosen has a free or open-source tier. Paid upgrades are optional, gated by an env var.
6. **Clone-to-ready under 10 minutes.** Measured from `git clone` to first green check.
7. **Never break existing files.** If a file exists, merge. If a directory exists, extend.

## PHASE 0: DETECTION AND PLANNING

Before writing a single file, run detection in parallel and produce a plan.

Detect in parallel and summarize what you find:
1. Primary language (read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `composer.json`, `build.gradle`, `mix.exs`, `deno.json`).
2. Framework (Next.js, FastAPI, Django, Rails, Laravel, Express, Spring, etc.).
3. Existing `.claude/`, `.cursor/`, `.antigravity/`, `.github/`, `.vscode/`, `.idea/` directories and their contents.
4. Existing MCP config (`.mcp.json`, `.cursor/mcp.json`, `claude_desktop_config.json`).
5. Existing hooks, skills, rules, agents, subagents, plugins.
6. Existing CI workflows in `.github/workflows/`.
7. Existing docker, compose, k8s, terraform, helm.
8. Existing docs directory.
9. Existing test runner and coverage tool.
10. Business vertical signals: e-commerce (Stripe, Shopify, WooCommerce), SaaS (Clerk, Auth0, Supabase), media (Contentful, Sanity), fintech (Plaid), health (FHIR, HL7), government (FedRAMP markers), developer tools (CLI, SDK, library).

Write the plan to `docs/AGENTIFICATION_PLAN.md` with a checklist of what will be added, what will be extended, and what will be left alone. Then proceed.

## PHASE 1: DIRECTORY SCAFFOLD (parallel)

Create or extend these directories. Each file inside is generated in parallel across agents or tmux panes or `parallel -j`.

```
.
├── .claude/
│   ├── CLAUDE.md
│   ├── settings.json
│   ├── memory/
│   │   ├── MEMORY.md
│   │   └── adrs/
│   ├── agents/
│   │   ├── _registry.yaml
│   │   ├── meta/
│   │   ├── operational/
│   │   ├── research/
│   │   └── domain/
│   ├── subagents/
│   ├── skills/
│   ├── rules/
│   ├── commands/
│   ├── hooks/
│   ├── templates/
│   └── mcp/
├── .cursor/
│   ├── rules/
│   ├── skills/
│   ├── subagents/
│   ├── hooks/
│   ├── mcp.json
│   ├── settings.json
│   └── modes.json
├── .antigravity/
│   ├── rules.md
│   ├── skills/
│   ├── workflows/
│   ├── knowledge.md
│   ├── artifacts.config.yaml
│   └── agent-manager.yaml
├── .windsurf/
│   └── rules/
├── .continue/
│   └── config.json
├── AGENTS.md
├── AGENT.md
├── CLAUDE.md
├── GEMINI.md
├── .github/
│   ├── copilot-instructions.md
│   ├── copilot-setup-steps.yml
│   ├── workflows/
│   │   ├── parallel-agents.yml
│   │   ├── claude.yml
│   │   ├── copilot-coding-agent.yml
│   │   ├── codex.yml
│   │   ├── jules.yml
│   │   ├── sweep.yml
│   │   ├── aider.yml
│   │   ├── coderabbit.yml
│   │   ├── eval-models.yml
│   │   ├── graphify-index.yml
│   │   └── wiki-sync.yml
│   └── CODEOWNERS
├── .devin/config.yml
├── .codegen/config.yml
├── .codex/config.toml
├── .jules/config.yml
├── .factory/droids.yml
├── .coderabbit.yml
├── agents/
│   ├── providers/
│   │   ├── anthropic.yaml
│   │   ├── openai.yaml
│   │   ├── google.yaml
│   │   ├── openrouter.yaml
│   │   ├── litellm.yaml
│   │   ├── bedrock.yaml
│   │   ├── vertex.yaml
│   │   ├── groq.yaml
│   │   └── ollama.yaml
│   ├── router/
│   └── runtime/
├── models/
│   ├── catalog.yaml
│   ├── routing.yaml
│   ├── embeddings.yaml
│   ├── rerankers.yaml
│   └── vision.yaml
├── mcp/
│   ├── servers/
│   ├── gateway/
│   └── registry.yaml
├── hooks/
│   ├── git/
│   ├── agent/
│   ├── ci/
│   └── cd/
├── skills/
│   ├── universal/
│   └── domain/
├── rules/
│   ├── universal/
│   └── domain/
├── subagents/
├── tools/
├── indexing/
│   ├── graphify/
│   ├── treesitter/
│   ├── lsif/
│   ├── vector/
│   └── fulltext/
├── networks/
│   ├── mesh/
│   ├── vpn/
│   ├── service-discovery/
│   └── agent-protocols/
├── docs/
│   ├── vault/
│   ├── adrs/
│   ├── runbooks/
│   ├── api/
│   └── AGENTIFICATION_PLAN.md
├── evals/
│   ├── promptfoo.yaml
│   ├── deepeval/
│   ├── ragas/
│   ├── inspect/
│   └── braintrust/
├── orchestration/
│   ├── dagger/
│   ├── temporal/
│   ├── prefect/
│   ├── argo-workflows/
│   ├── ray/
│   └── Justfile
├── scripts/
│   ├── bootstrap.sh
│   ├── parallel-bootstrap.sh
│   ├── verify-install.sh
│   ├── detect-business.sh
│   ├── install-models.sh
│   ├── install-mcp.sh
│   ├── install-hooks.sh
│   ├── install-indexing.sh
│   └── install-networks.sh
└── Makefile
```

## PHASE 2: MODELS (parallel install)

Generate `models/catalog.yaml` that enumerates every model across providers. Include Anthropic (Opus 4.7, Sonnet 4.6, Haiku 4.5), OpenAI (GPT-5, GPT-5 mini, GPT-5 nano, o4, GPT-4.1), Google (Gemini 3 Pro, Gemini 3.1 Pro, Gemini 3 Flash, Gemini 2.5 Pro), xAI (Grok 4, Grok Code Fast), DeepSeek (V3.1, R1), Qwen (2.5 Coder 32B, QwQ), Meta (Llama 3.3 70B, 3.2 Vision), Mistral (Large 2, Codestral 25), Cohere (Command R+), Cursor (Composer, Tab, Apply).

Generate `models/routing.yaml` with tiers:
- `reasoning_deep` points to Opus 4.7 with Gemini 3.1 Pro and DeepSeek R1 fallback.
- `reasoning_fast` points to Sonnet 4.6 with Gemini 3 Pro and GPT-5 fallback.
- `cheap_tab` points to Haiku 4.5 with Gemini 3 Flash and GPT-5 nano fallback.
- `long_context` points to Gemini 3.1 Pro (2M) with Sonnet 4.6 200K fallback.
- `code_specialist` points to Codestral 25 with Qwen 2.5 Coder and DeepSeek V3.1 fallback.
- `vision` points to Opus 4.7 Vision with Gemini 3 Pro Vision and GPT-5 Vision fallback.

Generate `models/embeddings.yaml` with Voyage 3, Cohere Embed v3, text-embedding-3-large, plus self-hosted BGE and Nomic.

Generate `models/rerankers.yaml` with Cohere Rerank 3, Jina Rerank, bge-reranker-v2-m3.

Write a `scripts/install-models.sh` that installs Ollama, pulls the open-weights set in parallel using `ollama pull ... &`, sets up LiteLLM proxy via Docker, and writes `.env.example` with every key slot.

## PHASE 3: CLOUD AGENTS (parallel config)

For every cloud agent in the reference below, generate a valid config file with sane defaults and a clear comment block describing activation.

Targets:
- GitHub Copilot Coding Agent (`.github/copilot-instructions.md`, `.github/copilot-setup-steps.yml`)
- Claude Code GitHub Action (`.github/workflows/claude.yml`)
- OpenAI Codex Cloud (`.codex/config.toml`, `AGENTS.md`)
- Google Jules (`.jules/config.yml`, `GEMINI.md`)
- Devin (`.devin/config.yml`)
- Codegen.com (`.codegen/config.yml`)
- Sweep AI (`.github/sweep.yaml`)
- Factory AI Droids (`.factory/droids.yml`)
- Aider in CI (`.github/workflows/aider.yml`)
- CodeRabbit (`.coderabbit.yml`)
- Cursor Background Agents (documented in `.cursor/settings.json`)
- Antigravity Agent Manager (`.antigravity/agent-manager.yaml`)
- OpenHands (`openhands/config.toml`)
- e2b sandboxes (`e2b/template.json`)
- Daytona workspaces (`.daytona/workspace.yaml`)
- Modal Labs (`modal/app.py`)

Each config file must contain a boilerplate header with activation instructions, required env vars, and a link to provider docs.

## PHASE 4: AGENTS (universal base plus domain layer)

Create `.claude/agents/_registry.yaml` with the universal agent taxonomy:

**Operational agents** (15): plan, fast, refactor, migration, test-author, bug-fix, feature, docs, pr-reviewer, release-notes, browser, terminal, data, model-router, cost-estimator.

**Meta agents** (12): agent-builder, agent-evaluator, agent-router, red-teamer, critic, swarm-director, memory-compressor, prompt-optimizer, planner, reflector, debater, ensemble.

**Research agents** (6): codebase-explorer, deep-researcher, crag, self-rag, graph-rag, hybrid-retrieval.

**Domain agents** (15 scaffolds that adapt to business type): executive, marketing, sales, customer-success, product, engineering, frontend, devops, security, data, qa, hr, finance, legal, content.

For each agent produce a markdown file at `.claude/agents/<category>/<n>.md` with YAML frontmatter:
```yaml
---
name: <agent-name>
description: <one-line>
tools: [<tool-ids>]
model_tier: <reasoning_deep|reasoning_fast|cheap_tab|long_context|code_specialist|vision>
parallel_safe: true
requires_approval: <tool-list>
---
```

Then render the same agents into Cursor format at `.cursor/subagents/<n>.json` and Antigravity format at `.antigravity/workflows/<n>.yaml`. Write a render script at `scripts/render-agents.sh` so the three formats stay in sync.

## PHASE 5: PLUGINS

Generate a single `plugins.manifest.yaml` at repo root listing every plugin to install and the IDE that consumes it. Then generate install scripts that pull each plugin in parallel:

- Cursor plugins: use Cursor plugin marketplace URIs.
- Claude Code plugins: git clone into `.claude/plugins/`.
- VS Code and Antigravity extensions: list IDs for install via CLI.
- `.vscode/extensions.json` with recommendations.

Include at minimum: ralph-wiggum, feature-dev, frontend-design, code-review, commit-commands, security-guidance, hookify, pr-review-toolkit, plugin-dev, mem0-memory, zep-memory, letta-agent-memory.

## PHASE 6: RULES

Create a rule file for every universal category in both Cursor and Claude formats. Source of truth lives at `rules/universal/<n>.md`. Render scripts produce:
- `.cursor/rules/<n>.mdc` with frontmatter specifying Always, Auto-attached glob, Agent Requested, or Manual.
- `.claude/rules/<n>.md`
- `.windsurf/rules/<n>.md`
- Relevant fragments appended to `.github/copilot-instructions.md`, `AGENTS.md`, `AGENT.md`, `CLAUDE.md`, `GEMINI.md`.

Universal categories to generate: architecture, api-design, code-quality, database, dependencies, devops, documentation, error-handling, frontend, git, monitoring, naming, performance, review, secrets, security, testing, accessibility, ai-safety, ai-cost, ai-latency, ai-eval, prompt-engineering, observability, compliance, internationalization, output-accessibility.

## PHASE 7: SKILLS

Create skill folders at `skills/universal/<n>/SKILL.md`. Every skill has:
```
skills/universal/<n>/
├── SKILL.md
├── scripts/
├── templates/
└── examples/
```

Then symlink or copy into `.claude/skills/` and `.cursor/skills/` and `.antigravity/skills/`.

Skills to generate: docx, xlsx, pptx, pdf, pdf-reading, frontend-design, api-patterns, auth-patterns, cache-patterns, db-patterns, event-patterns, frontend-patterns, k8s-patterns, security-patterns, testing-patterns, monitoring-patterns, gitops-patterns, multi-tenant-patterns, migration-patterns, performance-patterns, deployment-patterns, llm-wiki, obsidian-linker, guardrails, codebase-exploration, rag-retrieval, vector-search, multi-model-routing, cost-optimization, latency-optimization, batch-processing, streaming-responses, tool-calling-patterns, agent-handoff-patterns, prompt-engineering, self-consistency, tree-of-thought, reflection-patterns, evals, canvases, artifacts, browser-automation, business-onboarding, business-billing, business-ops.

## PHASE 8: SUBAGENTS

Generate subagent definitions at `subagents/<n>.yaml` and render to Cursor and Antigravity formats. Subagents: code-searcher, symbol-resolver, dependency-resolver, dead-code-finder, test-runner, linter, formatter, git-archaeologist, pr-drafter, changelog-writer, security-auditor, performance-profiler, accessibility-auditor, screenshot-comparator, browser-driver, api-caller, sql-runner, k8s-operator, terraform-planner, docs-updater, translation-agent, data-cleaner, notebook-runner, image-describer, video-transcriber, compliance-checker, cost-estimator, model-router.

## PHASE 9: TOOLS

Produce a `tools/catalog.yaml` describing every tool an agent can invoke, grouped by filesystem, shell, git, http, browser, database, cloud, container, orchestration, iac, observability, security, docs, notebook, data, images, ocr.

Generate per-tool wrappers in `tools/<category>/<n>.sh` (or `.ts`, `.py` as appropriate) that normalize arguments and add logging.

## PHASE 10: MCP

Build `mcp/registry.yaml` listing every MCP server from the universal catalog (filesystem, fetch, memory, sequential-thinking, github, gitlab, brave-search, exa, tavily, perplexity, playwright, browserbase, slack, discord, gmail, linear, jira, notion, datadog, sentry, grafana, prometheus, loki, postgres, mysql, mongodb, redis, qdrant, chroma, pinecone, weaviate, neo4j, aws, azure, gcp, cloudflare, docker, kubernetes, helm, terraform, vault, stripe, shopify, contentful, salesforce, hubspot, zendesk, intercom, klaviyo, mixpanel, amplitude, posthog, anthropic, openai, huggingface, replicate, modal, e2b, daytona, google-calendar, google-drive, github-actions, figma, mermaid, plantuml, obsidian, time, weather, ollama, vllm, localai).

Render to:
- `.mcp.json` (Claude Code and Claude Desktop)
- `.cursor/mcp.json`
- `.antigravity/mcp.json`
- `.vscode/mcp.json`

Stand up a Docker MCP Gateway at `mcp/gateway/docker-compose.yaml` so any agent can reach every MCP through one endpoint.

## PHASE 11: HOOKS

Install hooks in every category.

Claude and Cursor agent hooks at `.claude/hooks/` and `.cursor/hooks/`: SessionStart, UserPromptSubmit or beforeSubmitPrompt, PreToolUse, PostToolUse, Notification, SubagentStop, PreCompact, Stop. The Stop hook implements a ralph-wiggum-style loop continuation pattern with MAX_ITERATIONS configurable.

Git hooks at `hooks/git/` installed via Lefthook (`lefthook.yml` at repo root): pre-commit, prepare-commit-msg, commit-msg, post-commit, pre-push, post-checkout, post-merge, post-rewrite, pre-rebase.

CI and CD hooks at `hooks/ci/` and `hooks/cd/`: pre-deploy, post-deploy, pre-rollback, post-rollback, pre-release, post-release.

All hooks are parallelizable where semantically safe. Hooks that cannot run in parallel declare `serial: true` in their frontmatter.

## PHASE 12: INDEXING

Stand up the full indexing stack. Each runs in parallel during bootstrap.

- Graphify: `graphify index .` into `docs/vault/knowledge-graph/`.
- Tree-sitter: `indexing/treesitter/build.sh` compiles grammars.
- SCIP or LSIF: `indexing/lsif/build.sh` produces a SCIP index for Sourcegraph.
- CodeQL: `indexing/codeql/build.sh` creates a CodeQL database.
- Semgrep: `indexing/semgrep/build.sh` runs ruleset scan.
- Vector index: `indexing/vector/build.sh` embeds every source file into Qdrant and Chroma.
- Full-text: `indexing/fulltext/build.sh` builds a Tantivy or Meilisearch index.
- BM25 plus dense hybrid: `indexing/hybrid/build.sh` fuses the two.

Configure Cursor codebase index via `.cursorindexignore` so vendored artifacts are excluded.

## PHASE 13: DOCS

Initialize three doc surfaces that stay in sync.

1. **Obsidian vault** at `docs/vault/` with `_index.md`, `SCHEMA.md`, `raw/`, `wiki/`, `agents/`, `architecture/`, `runbooks/`, `memory/`, `knowledge-graph/`. Include `.obsidian/` config.
2. **MkDocs** or **Docusaurus** at `docs/site/` that renders API docs, ADRs, runbooks, agent catalog, and the LLM wiki into a public site.
3. **API docs**: OpenAPI in `docs/api/openapi.yaml`, Redoc and Swagger UI, GraphQL schema docs if applicable, Typedoc or PyDoc or Godoc for the primary language.

Wire Vale (prose linter), cspell (spellcheck), alex (inclusive language) as CI checks and pre-commit hooks. Add ADR tooling (`adr-tools`). Add diagrams-as-code (Mermaid, PlantUML, D2, Structurizr).

## PHASE 14: NETWORKS

Generate baseline configs for every network layer.

- Neural network runtimes: `networks/runtimes/README.md` covering PyTorch, ONNX Runtime, TensorRT, llama.cpp, MLX with example loaders.
- Agent mesh: `networks/mesh/ruflo.config.yaml` plus `networks/mesh/crewai.yaml` and `networks/mesh/langgraph.yaml`.
- Service mesh: `networks/service-mesh/linkerd.yaml` plus an Istio alternate.
- Container networking: Cilium plus Calico option in `networks/container/`.
- Overlay and VPN: Tailscale, WireGuard, Nebula, ZeroTier sample configs in `networks/vpn/`.
- Service discovery: Consul plus etcd plus CoreDNS in `networks/discovery/`.
- Agent protocols: MCP, A2A, ACP, AGNTCY, AutoGen documented in `networks/agent-protocols/README.md`.

## PHASE 15: PARALLEL EXECUTION HARNESS

This is the payoff. Wire every subsystem into one parallel bootstrap.

Create `scripts/parallel-bootstrap.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
PARALLELISM="${PARALLELISM:-$(nproc)}"

tasks=(
  "scripts/install-models.sh"
  "scripts/install-mcp.sh"
  "scripts/install-hooks.sh"
  "scripts/install-indexing.sh"
  "scripts/install-networks.sh"
  "scripts/render-agents.sh"
  "scripts/install-plugins.sh"
  "scripts/docs-bootstrap.sh"
  "scripts/vault-generate.sh"
  "scripts/graphify-index.sh"
  "scripts/evals-bootstrap.sh"
)

printf '%s\n' "${tasks[@]}" | xargs -I{} -P "$PARALLELISM" bash -c '{}'
scripts/verify-install.sh
```

Create a `Justfile` that exposes named recipes with DAG awareness so `just bootstrap` is the single entry point.

Create `.github/workflows/parallel-agents.yml` with a GitHub Actions matrix that fans out across every agent domain simultaneously on push, PR, and scheduled cron.

Create `orchestration/dagger/main.go` (or `.ts`) that defines the same DAG for containerized reproducibility.

Create `orchestration/temporal/workflows.py` for durable long-running agent workflows.

Create `orchestration/argo-workflows/swarm.yaml` for K8s-native DAG execution.

## PHASE 16: BUSINESS DETECTION LAYER

Write `scripts/detect-business.sh` that inspects the repo and emits a `BUSINESS_PROFILE.yaml` describing:
- Vertical (ecommerce, saas, media, fintech, health, gov, devtool, marketplace, social, edtech, other).
- Compliance posture (SOC 2, HIPAA, GDPR, PCI, FedRAMP, none).
- Primary stack (frontend, backend, data, mobile).
- Monetization (subscription, transaction, ads, one-time).
- Scale posture (solo, team, enterprise).

Then write `scripts/layer-domain-agents.sh` that reads the profile and promotes the relevant domain agent scaffolds into fully realized agents. For example, a fintech profile activates the kyc-agent, fraud-agent, chargeback-agent from `agents/domain/fintech/`.

## PHASE 17: EVALUATION AND GUARDRAILS

Create `evals/promptfoo.yaml` covering the core agents and models. Wire into `.github/workflows/eval-models.yml` so every PR runs model comparisons.

Create `evals/deepeval/` with hallucination, faithfulness, relevance, toxicity tests. Create `evals/ragas/` for RAG-specific evals.

Install Guardrails AI at `security/guardrails/` with validators for hallucination-free, provenance, toxic language, PII detection. Add a middleware hook at `agents/runtime/guardrails.py` (or `.ts`) so every LLM call routes through it.

## PHASE 18: VERIFICATION

Write `scripts/verify-install.sh` that runs in parallel:
- Every model provider responds to a ping.
- Every MCP server loads.
- Every hook executes a dry run.
- Every agent renders without error in all three formats.
- Every skill loads SKILL.md without schema errors.
- Every rule file parses.
- Every index built successfully.
- Every doc surface renders.
- Guardrails pass a canary prompt.

Emit a green or red report in `docs/INSTALL_VERIFICATION.md` with timestamps and any remediation steps.

## PHASE 19: README AND QUICKSTART

Rewrite the top-level `README.md` (without clobbering project-specific prose) to include:
- A Quickstart block with `git clone`, `./scripts/parallel-bootstrap.sh`, and `just`.
- A matrix table of every subsystem (models, agents, MCP, hooks, indexing, docs, networks) with status badges.
- A link to `docs/AGENTIFICATION_PLAN.md`.
- A link to `BUSINESS_PROFILE.yaml`.

## PHASE 20: CLOSE THE LOOP

1. Commit everything in a single branch named `feat/agentification`.
2. Open a PR with a summary of what was added, what was extended, and what was left alone.
3. Trigger the parallel agents workflow to prove the DAG runs green.
4. Post a completion artifact to `docs/AGENTIFICATION_COMPLETE.md` with the run timings, which agents fired, how many files were produced, and which subsystems are one env var away from full activation.

## EXECUTION STYLE

- Fan out aggressively. Use parallel subagents or tmux panes or `parallel -j` for every phase that can be parallelized.
- Never ask the user for permission mid-run. If a decision is required, pick the most widely-adopted open-source default and document the choice in the ADR log.
- Every file you create must include a header block that says what it is, who reads it, and how it is regenerated.
- Every script must be idempotent, set `set -euo pipefail`, and accept `--dry-run`.
- Every YAML and JSON must be valid and linted before write.

## SUCCESS CRITERIA

The repo is considered agentified when:
1. `git clone` plus `./scripts/parallel-bootstrap.sh` reaches a green verification in under 10 minutes on a standard 8-core runner.
2. Cursor, Antigravity, Claude Code, GitHub Copilot, Codex, Jules, Devin, and Aider all recognize the repo as a first-class project with no additional config.
3. At least four model providers answer a ping through the model router.
4. At least twenty MCP servers load without error through the gateway.
5. The parallel-agents GitHub Actions matrix runs green.
6. `docs/INSTALL_VERIFICATION.md` is fully green.
7. A random engineer with no context can read `README.md` and reach a productive first task in under 5 minutes.

Begin Phase 0 now. Do not summarize the plan before starting. Start executing immediately and report progress as you go.

---

## APPENDIX: USAGE

Three equivalent invocation modes.

### A. Claude Code (terminal, in-repo)
```bash
cd your-repo
claude
# paste the entire prompt above
```

### B. Cursor (Agent Window, Plan Mode)
- Open the repo in Cursor.
- Open Agent Window, select Plan Mode.
- Paste the prompt.
- Approve the plan.
- Let parallel subagents fan out.

### C. Antigravity (Agent Manager)
- Open the repo in Antigravity.
- New Task in Agent Manager.
- Paste the prompt.
- Assign Gemini 3.1 Pro for the planner slot and Claude Opus 4.7 and Sonnet 4.6 for two parallel execution slots.
- Review artifacts as each phase completes.

### D. GitHub Issue (for cloud agents)
- Open a new issue titled "Agentify this repo".
- Paste the prompt as the issue body.
- Assign to Copilot Coding Agent, Codex Cloud, or Jules.
- Review the resulting PR.

The prompt is identical across all four. No modifications required.
