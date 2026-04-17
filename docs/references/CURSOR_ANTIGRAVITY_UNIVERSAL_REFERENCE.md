# Cursor + Antigravity Universal Reference

Everything that can exist inside Cursor (v3.x) and Google Antigravity (Gemini 3 era) across models, cloud agents, agents, plugins, rules, skills, subagents, tools, MCP, hooks, indexing, docs, and networks. Oriented for multi-model execution and usable as the master catalog for any business deployment.

Scope date: April 17, 2026. This document is intentionally exhaustive. Pick the subset relevant to each project and drop it into the repository structure via the integration prompt.

---

## 1. Models

### 1.1 Models Natively Available in Cursor 3.x
| Provider | Model | Cursor role |
|---|---|---|
| Anthropic | Claude Opus 4.7 | Deep reasoning, architecture, long refactors |
| Anthropic | Claude Sonnet 4.6 | Default agent mode, balanced |
| Anthropic | Claude Haiku 4.5 | Fast tab completion, lightweight edits |
| Anthropic | Claude Sonnet 4.5 | Still available for compat, agent fallback |
| OpenAI | GPT-5 | Complex reasoning alternative |
| OpenAI | GPT-5 mini | Fast agent fallback |
| OpenAI | GPT-5 nano | Autocomplete speed tier |
| OpenAI | GPT-4.1 | Long-context fallback |
| OpenAI | o4 reasoning | Chain-of-thought tasks |
| Google | Gemini 3 Pro | Long-context (2M tokens) codebase reasoning |
| Google | Gemini 3 Flash | Fast autocomplete and boilerplate |
| Google | Gemini 2.5 Pro | Cost-optimized long context |
| xAI | Grok 4 | Alternate large-context reasoning |
| xAI | Grok Code Fast | Code-tuned speed tier |
| DeepSeek | DeepSeek V3.1 | Open-weights reasoning, cost-optimal |
| DeepSeek | DeepSeek R1 | Reasoning-tuned open model |
| Alibaba | Qwen 2.5 Coder 32B | Code specialist |
| Alibaba | QwQ 32B | Open reasoning model |
| Meta | Llama 3.3 70B | Open-weights fallback |
| Meta | Llama 3.2 Vision | Visual reasoning open-weights |
| Mistral | Mistral Large 2 | EU-hosted option |
| Mistral | Codestral 25 | Code-tuned Mistral |
| Cohere | Command R+ | RAG specialist |
| Cursor native | Composer | Cursor-trained fast coding model |
| Cursor native | Cursor Tab | Proprietary tab-completion model |
| Cursor native | Cursor Apply | Inline diff application model |

### 1.2 Models Natively Available in Antigravity
| Provider | Model | Antigravity role |
|---|---|---|
| Google | Gemini 3 Pro | Default Plan Mode and long-context |
| Google | Gemini 3.1 Pro | 2M-token context, primary agent |
| Google | Gemini 3 Flash | Fast Mode and parallel agent tier |
| Google | Gemini 2.5 Pro | Fallback long-context |
| Anthropic | Claude Opus 4.6 | Deep reasoning alternative |
| Anthropic | Claude Sonnet 4.5 | Balanced agent option |
| OpenAI | GPT-OSS 120B | Open-weights OpenAI alternative |
| OpenAI | GPT-OSS 20B | Lightweight OpenAI alternative |

### 1.3 Models Reachable Through OpenAI-Compatible Endpoints
Both Cursor and Antigravity accept custom OpenAI-compatible endpoints, which opens the following integrations.

| Gateway | Models unlocked |
|---|---|
| OpenRouter | 300+ models including Nemotron, Perplexity Sonar, Hermes, WizardLM |
| LiteLLM Proxy | Any of 100+ providers routed through a single endpoint |
| Portkey AI Gateway | Every major provider with caching and fallback |
| Helicone Proxy | Full provider coverage with observability |
| Together AI | Hosted open models (Llama, Qwen, DeepSeek, Mixtral) |
| Fireworks AI | Hosted open models with low-latency inference |
| Groq | LPU-accelerated Llama, Qwen, DeepSeek |
| Cerebras | Wafer-scale Llama inference |
| SambaNova | Fast Llama, Qwen |
| Replicate | Any open model hosted as API |
| HuggingFace Inference | Any HF model |
| Novita AI | Hosted open models |
| Mistral Codestral API | Direct Mistral code endpoint |
| NVIDIA NIM | Enterprise open-model API |
| Azure OpenAI | GPT models with Azure compliance |
| AWS Bedrock | Anthropic, Meta, AI21, Cohere, Amazon Titan |
| GCP Vertex AI | Gemini, Anthropic, Llama, Mistral |
| Databricks Mosaic | DBRX and hosted open models |

### 1.4 Local and Self-Hosted Runtimes
| Runtime | Path |
|---|---|
| Ollama | Local multi-model server with model registry |
| vLLM | Paged-attention inference at scale |
| llama.cpp server | GGUF quantized models |
| text-generation-inference | HuggingFace production server |
| TensorRT-LLM | NVIDIA-optimized inference |
| LocalAI | OpenAI-compatible local multi-modal |
| LM Studio headless | GUI plus headless local |
| GPT4All | CPU-first local |
| MLX (Apple Silicon) | Local Apple runtime |
| ExLlamaV2 | GPTQ quantized local |

### 1.5 Embedding and Reranker Models
| Model | Role |
|---|---|
| text-embedding-3-large | OpenAI default retrieval |
| voyage-3 and voyage-code-3 | Premium retrieval and code retrieval |
| cohere-embed-v3 | Enterprise retrieval |
| nomic-embed-text | Self-hosted retrieval |
| bge-large-en-v1.5 | Open retrieval |
| mxbai-embed-large | Open retrieval |
| jina-embeddings-v3 | Multi-task retrieval |
| Cohere Rerank 3 | Reranking |
| Jina Rerank | Reranking |
| bge-reranker-v2-m3 | Self-hosted reranking |
| mxbai-rerank-large | Self-hosted reranking |

### 1.6 Multi-Modal Models
| Model | Role |
|---|---|
| Gemini 3 Pro Vision | Screenshot to code, UI reasoning |
| Claude Opus 4.7 Vision | Design-to-code |
| GPT-5 Vision | Alternative vision |
| CLIP and SigLIP | Image embeddings |
| LLaVA, CogVLM, InternVL | Local vision-language |
| Whisper large-v3 | Speech to text |
| Distil-Whisper | Fast speech to text |
| Piper, Coqui XTTS, Bark | Text to speech |
| ElevenLabs | Premium TTS |
| Nano Banana Pro (Cursor) | Image generation in agent |
| Imagen 3 and Imagen 4 | Google image generation |
| Stable Diffusion 3.5 and Flux.1 | Open image generation |
| Runway Gen 3 | Video generation |
| Sora 2 | Video generation |
| Veo 3 | Google video generation |

### 1.7 Specialty Models
| Model | Role |
|---|---|
| CodeT5+, CodeBERT, UniXcoder | Code-specific embeddings |
| Granite Code, StarCoder 2, Code Llama | Code-tuned open models |
| Nougat, Marker | PDF to structured text |
| Surya OCR, Tesseract 5 | OCR |
| PaddleOCR | Multi-lingual OCR |
| Table Transformer | Table extraction |
| Donut | Document understanding |
| Detectron2, YOLOv11 | Object detection for screenshots |

---

## 2. Cloud Agents

Cursor and Antigravity both run cloud agents. The full landscape of cloud agents that integrate with either IDE or the repo is below.

### 2.1 Cursor-Native Cloud Agents
| Capability | Description |
|---|---|
| Background Agents | Isolated Ubuntu VMs, clone repo from GitHub, work on branch, open PRs |
| Self-Hosted Cloud Agents | Worker process connects outbound to Cursor cloud, executes tools on customer infra |
| Persistent Agent Handoff | Start locally, hand off to cloud to finish with laptop closed |
| Bugbot | PR review bot, learns from comments, MCP-enabled, Autofix |
| Cursor Cloud Session | claude.ai/code-style parallel sandboxed environments |
| Canvases | Durable side-panel artifacts alongside terminal, browser, source control |

### 2.2 Antigravity-Native Cloud Agents
| Capability | Description |
|---|---|
| Agent Manager | Mission Control dashboard dispatching up to 5 parallel agents |
| Plan Mode Agent | Generates Plan Artifact before coding |
| Fast Mode Agent | Quick inline edits |
| Browser Actuation Agent | Opens built-in Chrome, clicks, fills forms, records, screenshots |
| Artifact-Producing Agent | Every task produces plan, diff, screenshot, browser recording |
| Terminal Agent | Executes shell commands with streaming output |

### 2.3 External Cloud Agents That Integrate via GitHub or Repo Config
| Agent | Config file |
|---|---|
| GitHub Copilot Coding Agent | `.github/copilot-instructions.md`, `.github/copilot-setup-steps.yml` |
| GitHub Copilot Workspace | GitHub-native repo |
| Claude Code GitHub Action | `.github/workflows/claude.yml` |
| Claude Code Cloud | `.claude/cloud.json` |
| Devin (Cognition Labs) | `.devin/config.yml` |
| Codegen.com | `.codegen/config.yml` |
| OpenAI Codex Cloud | `.codex/config.toml`, `AGENTS.md` |
| Google Jules | `.jules/config.yml`, `GEMINI.md` |
| Sweep AI | `.github/sweep.yaml` |
| OpenHands (OpenDevin) | `openhands/config.toml` |
| Factory AI Droids | `.factory/droids.yml` |
| Bolt.new | `.bolt/config.json` |
| Replit Agent | `.replit` |
| Windsurf Cascade Cloud | `.windsurf/cascade.yml` |
| e2b sandboxes | `e2b/template.json` |
| Daytona workspaces | `.daytona/workspace.yaml` |
| Modal Labs | `modal/app.py` |
| Anthropic Claude Agent SDK | `agents/claude-sdk/` |
| Aider in CI | `.github/workflows/aider.yml` |
| CodeRabbit | `.coderabbit.yml` |
| Graphite CI | `.graphite.yml` |
| Lintrule | `.lintrule/` |
| Continue.dev Cloud | `.continue/config.json` |
| Tabnine | `.tabnine/config.json` |
| Zed AI | `.zed/settings.json` |
| JetBrains Junie | `.idea/junie/` |

---

## 3. Agents

Cursor and Antigravity both host agents. At the ecosystem level the following agent categories can exist in the repo.

### 3.1 Operational Agents (drive tasks end to end)
| Agent | Role |
|---|---|
| Plan Agent | Produces plan artifact before code changes |
| Fast Agent | Inline edit with minimal ceremony |
| Refactor Agent | Large-scale cross-file refactor |
| Migration Agent | Framework and version migrations |
| Test Author Agent | Generates unit, integration, E2E tests |
| Bug Fix Agent | Triage and fix from issue description |
| Feature Agent | End-to-end feature delivery |
| Documentation Agent | Generate and update docs |
| PR Reviewer Agent | Review diffs, post comments |
| Release Notes Agent | Generate changelog from commits |
| Browser Agent | Navigate web, fill forms, scrape |
| Terminal Agent | Execute shell workflows |
| Data Agent | SQL, pandas, notebook work |

### 3.2 Meta Agents (operate on other agents)
| Agent | Role |
|---|---|
| Agent Builder | Generates new agent definitions from spec |
| Agent Evaluator | Scores agent output (deepeval, Ragas) |
| Agent Router | Routes task to best agent |
| Red Team Agent | Adversarial prompts and jailbreak tests |
| Critic Agent | Constitutional AI critique loop |
| Swarm Director | Top-level multi-agent coordinator |
| Memory Compressor | Compresses long context into wiki pages |
| Prompt Optimizer | DSPy-style prompt search |
| Planner Agent | Tree-of-Thought planning |
| Reflector Agent | Reflexion self-critique loop |
| Debater Agent | Multi-agent debate for contested decisions |
| Ensemble Agent | Majority vote across model ensemble |

### 3.3 Research and Retrieval Agents
| Agent | Role |
|---|---|
| Codebase Explorer | Maps repo structure for new contributors |
| Deep Researcher | Long-horizon web research with tool loops |
| Corrective RAG (CRAG) | Retrieval with error correction |
| Self-RAG | Retrieval with gating decisions |
| Graph-RAG (Microsoft) | Knowledge-graph retrieval |
| Hybrid Retrieval Agent | Sparse plus dense plus rerank |

### 3.4 Business-Domain Agents (universal starter set)
The 265-agent fleet in `citadel-saas-factory` covers 15 domains. For a universal business starter the following domain templates should exist as scaffolds so any new project gets them: Executive, Marketing, Sales, Customer Success, Product, Engineering, Frontend, DevOps, Security, Data, QA, HR, Finance, Legal, Content. Each domain should ship at least one cross-industry scaffolding agent.

---

## 4. Plugins

### 4.1 Cursor Plugin Ecosystem (from Cursor 3 plugin marketplace)
A Cursor plugin bundles skills, MCPs, subagents, rules, and hooks. Categories:

| Category | Example plugins |
|---|---|
| Framework plugins | Next.js, Remix, Astro, Nuxt, SvelteKit, Laravel, Rails, Django, FastAPI, Spring |
| Cloud plugins | AWS, Azure, GCP, Cloudflare, Vercel, Fly.io, Railway, Render |
| Database plugins | Postgres, MySQL, MongoDB, Redis, SQLite, Supabase, PlanetScale, Neon, Turso |
| Observability plugins | Datadog, Sentry, Grafana, New Relic, Honeycomb, Lightstep, Axiom |
| Messaging plugins | Slack, Discord, Teams, Telegram |
| Project plugins | Linear, Jira, Asana, Notion, GitHub Projects, ClickUp, Monday |
| Payments plugins | Stripe, Paddle, Lemon Squeezy, Flutterwave, Paystack |
| Auth plugins | Auth0, Clerk, Supabase Auth, Keycloak, Okta, Firebase Auth, WorkOS |
| E-commerce plugins | Shopify, WooCommerce, BigCommerce, Medusa |
| CMS plugins | Contentful, Sanity, Strapi, Payload, WordPress |
| AI provider plugins | Anthropic, OpenAI, Google, Replicate, HuggingFace |
| Security plugins | Snyk, GitGuardian, Semgrep, Trivy, Wiz, Orca |

### 4.2 Claude Code Plugins Compatible With Cursor and Antigravity
Cursor can load Claude Code resources from `~/.claude/{skills,agents}`. Relevant plugins:

| Plugin | Role |
|---|---|
| ralph-wiggum | Auto-loop pattern (Grace Engine equivalent) |
| feature-dev | 7-phase feature workflow |
| frontend-design | Design tokens and mockup standards |
| code-review | 5-agent parallel review |
| commit-commands | Conventional-commit slash commands |
| security-guidance | Security patterns |
| hookify | Hook generator |
| pr-review-toolkit | PR review automation |
| plugin-dev | Plugin authoring helpers |
| mem0-memory | Long-term memory layer |
| zep-memory | Graph-based memory |
| letta-agent-memory | Letta or MemGPT memory |

### 4.3 Antigravity Extensions
Antigravity imports VS Code extensions at install and supports the VS Code Marketplace alongside its own agent plugin model. Anything listed in sections 4.1 and 4.2 that ships as a VS Code extension plus an MCP or rule file works in both.

---

## 5. Rules

Rules are always-on context attached to the agent. They live in these canonical locations.

### 5.1 Rule File Locations Across Tools
| File | Owner |
|---|---|
| `.cursor/rules/*.mdc` | Cursor modern rules |
| `.cursorrules` | Cursor legacy rules |
| `AGENT.md` | Cursor plus universal agent spec |
| `AGENTS.md` | Universal spec used by Codex, Jules, Factory |
| `.claude/rules/*.md` | Claude Code rules |
| `CLAUDE.md` | Claude Code master instructions |
| `GEMINI.md` | Gemini Code Assist and Jules |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.continue/config.json` and `.continuerules` | Continue.dev |
| `.windsurf/rules/*.md` | Windsurf and Codeium |
| `.aider.conf.yml` and `.aiderignore` | Aider |
| `.zed/settings.json` | Zed |
| `.idea/aiassistant.xml` | JetBrains AI |
| `antigravity.rules` or `.antigravity/rules.md` | Antigravity |

### 5.2 Rule Attachment Modes (Cursor 3 taxonomy)
| Mode | Use |
|---|---|
| Always | Always included in context |
| Auto-attached | Included when glob matches current file |
| Agent Requested | Agent decides whether to pull in |
| Manual | User invokes by slash command |

### 5.3 Universal Rule Categories Any Business Should Ship
| Category | Purpose |
|---|---|
| Architecture | Layering, DDD, clean architecture |
| API design | REST, GraphQL, gRPC conventions |
| Code quality | Immutability, file size, cyclomatic complexity |
| Database | Migrations, RLS, indexing |
| Dependencies | Lock files, audit policies |
| DevOps | GitOps, immutable infra |
| Documentation | ADRs, docstrings |
| Error handling | Structured errors, retry |
| Frontend | Component, accessibility, performance |
| Git | Conventional commits, branch naming |
| Monitoring | Structured logging, RED metrics |
| Naming | Case conventions |
| Performance | Caching, lazy loading |
| Review | PR checklists |
| Secrets | Vault, rotation, scanning |
| Security | Input validation, XSS, CSRF |
| Testing | TDD, coverage thresholds |
| Accessibility | WCAG 2.1 AA |
| AI safety | Prompt injection defense |
| AI cost | Token budgets |
| AI latency | Streaming first |
| AI eval | Regression gates |
| Prompt engineering | Few-shot, chain-of-thought |
| Observability | Tracing, spans, correlation IDs |
| Compliance | SOC 2, HIPAA, GDPR, PCI |
| Internationalization | i18n, l10n, RTL |
| Accessibility of outputs | Alt text, captions |

---

## 6. Skills

### 6.1 Cursor Agent Skills (SKILL.md)
Skills are dynamically loaded when the agent detects relevance. Location `.cursor/skills/<name>/SKILL.md`. Can include scripts, commands, hook integration.

### 6.2 Claude Code Skills
Located at `.claude/skills/<name>/SKILL.md`. Cursor can read these. Key ones that belong in any repo:

| Skill | Purpose |
|---|---|
| docx | Word document creation and editing |
| xlsx | Spreadsheet creation |
| pptx | Presentation creation |
| pdf | PDF creation and manipulation |
| pdf-reading | PDF extraction strategies |
| frontend-design | Design tokens and mockup standards |
| skill-creator | Creating new skills |
| product-self-knowledge | Product documentation patterns |
| file-reading | Router for reading uploaded files |

### 6.3 Universal Skill Pack for Any Business
| Skill | Purpose |
|---|---|
| api-patterns | API design patterns |
| auth-patterns | Auth flows |
| cache-patterns | Caching strategies |
| db-patterns | Database patterns |
| event-patterns | Event-driven architecture |
| frontend-patterns | Component and state patterns |
| k8s-patterns | Kubernetes patterns |
| security-patterns | Security patterns |
| testing-patterns | Testing strategies |
| monitoring-patterns | Observability patterns |
| gitops-patterns | GitOps workflows |
| multi-tenant-patterns | Multi-tenancy |
| migration-patterns | Zero-downtime migrations |
| performance-patterns | Performance optimization |
| deployment-patterns | Deployment strategies |
| llm-wiki | Karpathy wiki pattern |
| obsidian-linker | Auto-backlink markdown |
| guardrails | Hallucination prevention |
| codebase-exploration | Structured repo tours |
| rag-retrieval | Retrieval patterns |
| vector-search | Vector index patterns |
| multi-model-routing | Model-tier selection |
| cost-optimization | Token and infra cost |
| latency-optimization | Streaming and parallel tools |
| batch-processing | Anthropic and OpenAI batch API |
| streaming-responses | SSE and WebSocket |
| tool-calling-patterns | Function-calling conventions |
| agent-handoff-patterns | Swarm handoffs |
| prompt-engineering | Few-shot and CoT |
| self-consistency | Self-consistency ensembles |
| tree-of-thought | ToT branching |
| reflection-patterns | Reflexion loop |
| evals | Promptfoo and deepeval patterns |
| canvases | Cursor canvas authoring |
| artifacts | Antigravity artifact authoring |
| browser-automation | Playwright and Browser Use |
| business-onboarding | Customer onboarding flows |
| business-billing | Stripe and subscription patterns |
| business-ops | Ops runbooks |

---

## 7. Subagents

Subagents run in parallel under a parent agent. Each has its own context, tools, and model.

### 7.1 Cursor Default Subagents
| Subagent | Role |
|---|---|
| Codebase Researcher | Deep codebase search |
| Terminal Runner | Isolated terminal execution |
| Parallel Work Streams | Fan-out independent tasks |

### 7.2 Antigravity Parallel Agents (up to 5, expanding)
Each slot in the Agent Manager is effectively a subagent with its own workspace, model, and artifacts.

### 7.3 Custom Subagent Catalog (drop-in)
| Subagent | Role |
|---|---|
| code-searcher | Ripgrep plus semantic search |
| symbol-resolver | Cross-file symbol graph |
| dependency-resolver | Build-graph traversal |
| dead-code-finder | Unused code detection |
| test-runner | Parallel test execution |
| linter | Multi-linter orchestration |
| formatter | Multi-formatter orchestration |
| git-archaeologist | Blame plus log analysis |
| pr-drafter | Diff to PR description |
| changelog-writer | Commit to changelog |
| security-auditor | SAST plus SCA plus secret scan |
| performance-profiler | Benchmark orchestration |
| accessibility-auditor | axe-core plus manual checks |
| screenshot-comparator | Visual regression |
| browser-driver | Playwright control |
| api-caller | OpenAPI-driven HTTP |
| sql-runner | Read-only SQL runner |
| k8s-operator | kubectl wrapper |
| terraform-planner | tf plan plus diff |
| docs-updater | API docs plus README |
| translation-agent | Multi-locale sync |
| data-cleaner | Pandas or Polars cleanup |
| notebook-runner | Jupyter execution |
| image-describer | VLM-based alt text |
| video-transcriber | Whisper transcription |
| compliance-checker | Policy validator |
| cost-estimator | Token and infra cost |
| model-router | Per-task model selection |

---

## 8. Tools

### 8.1 Cursor Built-in Tools
| Tool | Role |
|---|---|
| read_file | File read |
| edit_file | Structured edit |
| write_file | Create file |
| run_terminal | Shell execution |
| search_codebase | Semantic code search |
| grep | Regex search |
| list_dir | Directory listing |
| fetch_webpage | HTTP fetch |
| browser_navigate | In-editor browser |
| browser_screenshot | Capture DOM |
| browser_console | Read console logs |
| browser_network | Inspect network |
| image_generate | Nano Banana Pro |
| await | Wait for long-running job or subagent |
| todo_manager | Todo card tracking |

### 8.2 Antigravity Built-in Tools
| Tool | Role |
|---|---|
| editor_edit | Inline editor edits |
| plan_artifact | Generate plan |
| terminal_run | Streamed terminal |
| browser_actuate | Click, type, submit in built-in Chrome |
| browser_record | Capture browser session |
| problems_fix | Explain-and-fix from Problems panel |
| screenshot_capture | Page or element screenshot |
| artifact_write | Produce plan, diff, screenshot, recording |
| mcp_call | Invoke MCP server tool |

### 8.3 Universal Tool Categories Any Business Should Wire Up
| Category | Tools |
|---|---|
| File system | read, write, edit, glob, watch |
| Shell | bash, powershell, fish |
| Git | blame, log, diff, bisect, worktree |
| HTTP | curl, httpie, fetch, graphql |
| Browser | Playwright, Puppeteer, Browser Use, Stagehand |
| Database | psql, mysql, mongosh, redis-cli |
| Cloud | aws-cli, az, gcloud, cloudflared |
| Container | docker, podman, nerdctl, buildah |
| Orchestration | kubectl, helm, kustomize, k9s |
| IaC | terraform, pulumi, ansible, packer |
| Observability | datadog-cli, loki-cli, promtool, tempocli |
| Security | trivy, semgrep, gitleaks, trufflehog |
| Docs | mkdocs, sphinx, typedoc, godoc |
| Notebook | jupyter, marimo, zeppelin |
| Data | pandas, polars, duckdb, dask |
| Images | imagemagick, ffmpeg, ghostscript |
| OCR | tesseract, surya, paddleocr |

---

## 9. MCP (Model Context Protocol)

Both Cursor and Antigravity speak MCP. Cursor stores MCP configs in `.cursor/mcp.json`. Antigravity added MCP support in early 2026.

### 9.1 Universal MCP Server Catalog
Every one of these can be wired into the repo and invoked by any agent.

| Category | Server |
|---|---|
| Core | filesystem, fetch, memory, sequential-thinking, everything |
| VCS | github, gitlab, bitbucket, gitea |
| Search | brave-search, google-search, perplexity, exa, tavily, serpapi |
| Browser | playwright, puppeteer, browserbase, browser-use |
| Chat and comms | slack, discord, teams, telegram, gmail, outlook |
| Project mgmt | linear, jira, asana, notion, clickup, monday, trello, github-projects |
| Docs | confluence, notion-docs, gitbook, readme-io |
| Observability | datadog, sentry, grafana, prometheus, loki, tempo, honeycomb, new-relic, lightstep |
| Databases | postgres, mysql, mongodb, redis, sqlite, supabase, planetscale, neon, turso, snowflake, bigquery, databricks, clickhouse |
| Vector DBs | qdrant, chroma, pinecone, weaviate, milvus, vespa, typesense, meilisearch |
| Graph | neo4j, tigergraph, dgraph |
| Cloud | aws, azure, gcp, cloudflare, vercel, fly, railway, render, digitalocean, hetzner |
| Containers | docker, kubernetes, helm, argocd |
| IaC | terraform, pulumi, ansible |
| Secrets | vault, aws-secrets-manager, gcp-secret-manager, doppler, 1password |
| Payments | stripe, paddle, lemonsqueezy, flutterwave, paystack |
| E-commerce | shopify, woocommerce, bigcommerce, medusa |
| CMS | contentful, sanity, strapi, payload, wordpress |
| CRM | salesforce, hubspot, pipedrive, zoho |
| Support | zendesk, intercom, freshdesk, help-scout |
| Marketing | klaviyo, mailchimp, sendgrid, postmark, resend |
| Analytics | mixpanel, amplitude, posthog, ga4, segment |
| AI infra | anthropic, openai, huggingface, replicate, modal, e2b, daytona |
| Code execution | e2b-sandbox, daytona, modal-functions, cloudflare-workers |
| Calendar | google-calendar, outlook-calendar, calendly |
| Drive | google-drive, dropbox, onedrive, box |
| Dev tools | github-actions, circleci, jenkins, buildkite |
| Design | figma, sketch, framer, miro, excalidraw |
| Diagrams | mermaid, plantuml, structurizr, d2 |
| Finance | quickbooks, xero, plaid, mercury |
| Testing | playwright-mcp, cypress-mcp, percy, chromatic |
| APM | apify, firecrawl, browserbase, scrapfly |
| Knowledge | obsidian-mcp, roam-mcp, logseq-mcp, anytype |
| Time and location | time, weather, maps |
| Self-hosted AI | ollama, vllm, localai |

### 9.2 MCP Discovery and Gateway
| Tool | Role |
|---|---|
| MCP Registry at github.com/mcp | Anthropic-hosted catalog |
| Docker MCP Gateway | Run MCPs as containers behind one endpoint |
| GitHub MCP Registry | Cloud-hosted MCP registry |
| Smithery | MCP marketplace |
| mcp.run | Hosted MCP runner |
| Toolhouse | Hosted MCP infra |
| Composio | Multi-tool MCP hub |

---

## 10. Hooks

Hooks intercept agent lifecycle events. Cursor and Claude Code both support hooks, and Cursor accepts Claude Code hooks.

### 10.1 Cursor Hook Events (v3.x)
| Event | Purpose |
|---|---|
| beforeSubmitPrompt | Modify user prompt before sending |
| PreToolUse | Gate tool call before execution |
| PostToolUse | Post-process tool result |
| Stop | Run on agent stop, can inject follow-up message for loop continuation |
| Notification | React to agent notification |
| SessionStart | Initialize on session open |

### 10.2 Claude Code Hook Events
| Event | Purpose |
|---|---|
| SessionStart | Init session |
| UserPromptSubmit | Pre-process prompt |
| PreToolUse | Gate tool |
| PostToolUse | Post-process tool |
| Notification | React |
| SubagentStop | React to subagent completion |
| PreCompact | Before context compaction |
| Stop | On end |

### 10.3 Git Hooks (run on clone, commit, push, receive)
| Hook | Purpose |
|---|---|
| pre-commit | Lint, format, secret scan |
| prepare-commit-msg | Auto-populate commit message |
| commit-msg | Validate conventional commits |
| post-commit | Coverage check, changelog |
| pre-push | Security scan, test |
| post-checkout | Install deps on branch switch |
| post-merge | Install deps on merge |
| post-rewrite | Reapply changes after rebase |
| pre-rebase | Safety checks |
| pre-receive | Server-side policy |
| update | Server-side per-ref policy |
| post-receive | Server-side post actions |

### 10.4 CI and CD Hooks
| Hook | Purpose |
|---|---|
| pre-deploy | Image scan, smoke test |
| post-deploy | Health check, notification |
| pre-rollback | State snapshot |
| post-rollback | Verification |
| pre-release | Tag and notes |
| post-release | Publish artifacts |

### 10.5 Hook Orchestrators
| Tool | Role |
|---|---|
| Husky | Node-based git hooks |
| Lefthook | Polyglot git hooks |
| pre-commit | Python pre-commit framework |
| Commitizen | Commit message prompts |
| commitlint | Commit message validation |
| lint-staged | Run on staged files |

---

## 11. Indexing

### 11.1 Cursor Codebase Indexing
Cursor maintains a Merkle-tree codebase index with embeddings. `.cursorindexignore` controls exclusions.

### 11.2 Antigravity Context Layer
Antigravity relies on the 2M-token Gemini context for whole-codebase reasoning, supplemented by the agent knowledge layer.

### 11.3 Universal Indexing Stack
| Tool | Role |
|---|---|
| Graphify | Tree-sitter AST plus knowledge graph |
| ctags plus cscope | Classic symbol index |
| LSIF or SCIP | Precise cross-repo index (Sourcegraph) |
| Stack Graphs | Scope-aware naming resolution |
| Kythe | Google-scale semantic index |
| Glean | Meta-scale semantic index |
| CodeQL database | Queryable semantic index |
| Semgrep full-codebase index | Pattern index |
| ast-grep index | Syntactic pattern index |
| Comby | Structural search index |
| Tree-sitter grammars | Per-language parsers |
| Qdrant, Chroma, Pinecone, Weaviate, Milvus | Vector indexes |
| Tantivy, Meilisearch, Typesense | BM25 full-text indexes |
| OpenSearch, Elasticsearch | Enterprise full-text |
| Vespa | Hybrid index |
| LlamaIndex, Haystack, DSPy | RAG frameworks |
| OpenWebUI | Local RAG UI |
| Continue.dev indexing | IDE-side index |
| Supabase pgvector | Postgres vector |
| Neo4j vector | Graph plus vector |

---

## 12. Docs

### 12.1 Doc Systems Compatible With Repo
| Tool | Role |
|---|---|
| MkDocs and Material | Python-friendly docs |
| Docusaurus | React-based docs site |
| VitePress | Vue-based docs |
| Nextra | Next.js-based docs |
| Astro Starlight | Astro docs framework |
| Mintlify | Hosted docs platform |
| GitBook | Hosted docs platform |
| ReadTheDocs | Hosted Sphinx |
| Sphinx | Python docs |
| Typedoc | TypeScript API docs |
| JSDoc | JavaScript API docs |
| PyDoc | Python API docs |
| Rustdoc | Rust API docs |
| Godoc | Go API docs |
| Javadoc | Java API docs |
| Doxygen | C and C++ docs |
| Swagger and Redoc | OpenAPI docs |
| GraphiQL plus GraphQL Docs | GraphQL docs |
| Storybook | Component docs |
| Histoire | Vue-native Storybook |
| Docz | MDX-based docs |
| Backstage TechDocs | Internal dev portal |
| Obsidian vault | Personal knowledge graph |
| Roam, Logseq, Anytype | Networked notes |
| Notion plus mdx-notion | Hosted docs |

### 12.2 Doc-Specific Tooling
| Tool | Role |
|---|---|
| ADR tools (adr-tools) | Architecture Decision Records |
| C4 plus Structurizr | Architecture diagrams as code |
| PlantUML, Mermaid, D2 | Diagrams as code |
| diagrams.net, Excalidraw | Visual diagrams |
| OpenAPI Diff | API change detection |
| cspell | Spellcheck |
| vale | Prose linter |
| alex | Inclusive language |
| interrogate | Docstring coverage |
| pydoctor | Python docs |
| cz-emoji and gitmoji | Commit-message emoji |
| changesets | Versioned changelog |

### 12.3 Brain Memory Layer
| Pattern | Implementation |
|---|---|
| LLM Wiki (Karpathy) | `docs/vault/raw`, `docs/vault/wiki`, `SCHEMA.md` |
| Memory cards | `.claude/memory/MEMORY.md` |
| ADR log | `.claude/memory/adrs/` |
| Decision log | `docs/decisions/` |
| Runbook library | `docs/runbooks/` |

---

## 13. Networks

### 13.1 Neural Network Runtimes (in-repo)
| Runtime | Role |
|---|---|
| PyTorch | Primary DL framework |
| TensorFlow and Keras | Alternative DL |
| JAX and Flax | Research DL |
| ONNX Runtime | Cross-framework inference |
| TensorRT | NVIDIA inference |
| OpenVINO | Intel inference |
| Core ML | Apple inference |
| TFLite | Edge inference |
| llama.cpp | CPU LLM inference |
| MLX | Apple Silicon |
| Candle | Rust DL |
| Burn | Rust DL |
| tinygrad | Minimal DL |

### 13.2 Agent Network Topologies
| Topology | Tool |
|---|---|
| Mesh | Ruflo swarm |
| Hierarchical | CrewAI, LangGraph |
| Pipeline | DSPy, Haystack |
| Blackboard | Camel-AI |
| Actor model | Temporal, Akka |
| MapReduce over agents | Ray, Dask |
| Gossip or pub-sub | NATS, Redis Streams |

### 13.3 Service Mesh and Container Networking
| Tool | Role |
|---|---|
| Linkerd | Default mesh |
| Istio | Feature-rich mesh |
| Consul Connect | HashiCorp mesh |
| Cilium | eBPF networking |
| Calico | K8s networking |
| Flannel | Simple overlay |
| Weave | Overlay |
| Traefik | Ingress and proxy |
| NGINX | Ingress and proxy |
| Envoy | L7 proxy |
| Caddy | Auto-TLS proxy |

### 13.4 Overlay, VPN, and Zero-Trust Networks
| Tool | Role |
|---|---|
| Tailscale | Zero-config VPN |
| WireGuard | Kernel VPN |
| Nebula | Mesh VPN |
| ZeroTier | Mesh VPN |
| OpenZiti | Zero-trust overlay |
| Boundary | HashiCorp zero-trust |
| Teleport | Zero-trust access |
| Cloudflare Tunnel | Tunneled access |

### 13.5 Service Discovery and Routing
| Tool | Role |
|---|---|
| Consul | Service discovery |
| etcd | Distributed config |
| CoreDNS | DNS-based discovery |
| Zookeeper | Coordination |

### 13.6 Agent Communication Protocols
| Protocol | Role |
|---|---|
| MCP (Model Context Protocol) | Anthropic tool protocol |
| A2A (Agent to Agent) | Google agent protocol |
| ACP (Agent Communication Protocol) | IBM agent protocol |
| AGNTCY | Open agent network |
| AutoGen protocol | Microsoft multi-agent |
| LangGraph protocol | Graph-based routing |
| FIPA-ACL | Legacy agent comms |
| OpenAI Realtime API | WebRTC agent streaming |
| Anthropic Computer Use | Desktop control |

---

## 14. Parallel-Execution Orchestration (cross-cutting)

Because the goal is true parallelism on clone, every category above needs a fan-out driver.

| Driver | Role |
|---|---|
| GNU parallel | Shell fan-out |
| xargs -P | Simple parallel |
| make -j | Recipe parallel |
| just | DAG-aware recipes |
| Turborepo | Monorepo build DAG |
| Nx | Affected-graph parallel |
| Bazel, Buck2, Pants | Hermetic parallel |
| moonrepo | Task runner |
| Dagger | Cache-aware pipelines |
| Earthly | Reproducible parallel builds |
| act | Local GitHub Actions |
| GitHub Actions matrix | Cloud matrix |
| Argo Workflows | DAG YAML on K8s |
| Temporal | Durable workflows |
| Prefect | Modern DAG |
| Airflow | Classic DAG |
| Flyte | Typed workflows |
| Luigi | Simple DAG |
| Ray | Parallel Python |
| Dask | Parallel Python |
| Celery | Distributed queue |
| RQ | Redis queue |
| tmux with send-keys | Terminal parallel |
| Zellij layouts | Terminal parallel |

---

## 15. Keep-in-Mind Table

| Dimension | Cursor | Antigravity |
|---|---|---|
| Default interface | Editor first with Agent Window | Agent Manager first with Editor View |
| Parallel agents | Unlimited subagents, panes in Agents Window | Up to 5 in Manager View |
| Built-in browser | Yes, MCP-based | Yes, native Chrome integration |
| Artifacts model | Canvases, durable side panel | Plan, Diff, Screenshot, Browser Recording |
| Primary models | Claude, GPT, Gemini, Composer | Gemini 3 Pro, Claude, GPT-OSS |
| MCP | First class | Added early 2026 |
| Hooks | beforeSubmitPrompt, Pre/Post tool, Stop | Plan-stage hooks, agent lifecycle |
| Skills | Cursor Agent Skills (SKILL.md) | Skills and Workflows (early 2026) |
| Subagents | Default three plus custom | Agent Manager slots |
| Plugins | Marketplace with MCP, skills, subagents, rules, hooks | VS Code extensions plus MCP |
| Rules | `.cursor/rules/*.mdc`, `AGENT.md` | `.antigravity/rules.md` |
| Cloud | Background Agents, Self-Hosted, Handoff | Cloud-first, all runs in Google cloud |
| Context window | 200K typical | 2M on Gemini 3.1 Pro |
| Price tier | Free, Pro, Teams, Enterprise | Free preview, Pro $20, Ultra $249.99 |

---

End of universal reference.
