# Tool Integrations

## MCP Servers (43 in registry)
- **Core**: filesystem, fetch, memory, sequential-thinking
- **Version Control**: github, gitlab
- **Search**: brave-search, exa, tavily
- **Database**: postgres, mongodb, redis, supabase
- **Vector**: chroma, pinecone, qdrant, weaviate
- **Monitoring**: prometheus, grafana, datadog, sentry
- **Communication**: slack, discord, gmail
- **Design**: figma
- **Project Management**: jira, asana, linear, notion
- **AI/ML**: anthropic, openai, ollama, huggingface, replicate
- **Infrastructure**: docker, kubernetes, cloudflare, aws
- **Other**: playwright, mermaid, obsidian, stripe, context7

## Model Providers (12)
Anthropic, OpenAI, Google, xAI, DeepSeek, Mistral, Cohere, Meta, Alibaba (Qwen), Zhipu (GLM), MiniMax, Ollama

## Model Tiers (8)
- reasoning_deep: Claude Opus 4.6
- reasoning_fast: Claude Sonnet 4.6
- cheap_fast: Claude Haiku 4.5
- long_context: Gemini 3.1 Pro (2M tokens)
- code_specialist: Codestral 25
- vision: Claude Opus 4.6
- local_only: Llama 4 Maverick
- ultra_context: Llama 4 Scout (10M tokens)

## IDE/Agent Platforms (10+)
Claude Code, Cursor, GitHub Copilot, OpenAI Codex, Google Jules, Antigravity, Windsurf, Continue.dev, Devin, Factory AI, CodeRabbit, Daytona, Codegen

## Guardrails Stack
- Layer 1: Guardrails AI (schema enforcement, hub validators)
- Layer 2: NeMo Guardrails (Colang dialogue control)
- Layer 3: DeepEval + promptfoo (CI/CD continuous evaluation)
- Threshold: score >= 0.85 pass, < 0.85 retry (max 3) then reject

## Observability
- Prometheus: metrics collection + alerting rules
- Grafana: dashboards
- Loki: log aggregation
- AlertManager: alert routing
- Falco: runtime threat detection
- Sigma: detection rules
