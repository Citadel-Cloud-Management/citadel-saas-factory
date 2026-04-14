---
name: Multi-Engine LLM Backends
description: Three swappable LLM backends for Claude Code — paid, free, and local.
tags: [engines, llm, claude-code, multi-backend]
---

# Multi-Engine LLM Backends

Citadel SaaS Factory supports **three swappable LLM engine backends** for Claude Code, so you can pick the right quality/cost/privacy tradeoff for every task without changing any application code.

All three engines work because Claude Code respects the standard `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, and `ANTHROPIC_AUTH_TOKEN` environment variables. A thin proxy (y-router or LiteLLM) translates non-Anthropic upstreams into the Messages API format.

## Comparison matrix

| Dimension        | **Paid** (Anthropic) | **Free** (OpenRouter) | **Local** (Ollama) |
|------------------|----------------------|-----------------------|---------------------|
| Monthly cost     | ~$20–200 (usage)     | **$0**                | **$0**              |
| Primary model    | Claude Sonnet 4.6    | Llama 3.3 70B         | Qwen 2.5 Coder 32B  |
| Small/fast model | Claude Haiku 4.5     | Qwen 3 8B             | Qwen 2.5 Coder 7B   |
| Latency (p50)    | ~800 ms              | ~2–5 s                | ~300 ms (local NIC) |
| Coding quality   | 100% baseline        | ~80% of baseline      | ~70% of baseline    |
| Rate limits      | Tier-based           | Aggressive (free)     | None                |
| Data egress      | To Anthropic         | To OpenRouter         | **Zero**            |
| Offline capable  | No                   | No                    | **Yes**             |
| Best for         | Production work      | Prototyping, CI       | Air-gapped, regulated |

## Quick start

```bash
# Paid (Claude 4.6 direct)
make run-paid

# Free (OpenRouter free tier)
make run-free

# Local (Ollama + y-router)
make run-local

# Print current engine config
make engine-status
```

Or source the engine file directly and launch Claude Code yourself:

```bash
source engines/paid.env && claude
source engines/openrouter-free.env && claude
source engines/local-ollama.env && claude
```

## Shell aliases

Add this to `~/.bashrc` or `~/.zshrc`:

```bash
source /path/to/citadel-saas-factory/engines/switch-engine.sh
```

You now have:

- `cc-paid` — launch Claude Code against Anthropic direct
- `cc-free` — launch against OpenRouter free tier
- `cc-local` — launch against local Ollama
- `cc-status` — print the currently configured engine

## Engine 1 — Paid (Anthropic direct)

**Use when:** you're doing production work, reviewing security-sensitive code, or any task where the extra ~20% quality matters more than cost.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export ANTHROPIC_MODEL="claude-sonnet-4-6"
export ANTHROPIC_SMALL_FAST_MODEL="claude-haiku-4-5-20251001"
claude
```

No `BASE_URL` override needed — traffic goes directly to `api.anthropic.com`. Get an API key at [console.anthropic.com](https://console.anthropic.com/settings/keys).

## Engine 2 — Free (OpenRouter)

**Use when:** prototyping, running CI checks, onboarding new developers, or any task where occasional 429s are acceptable.

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="sk-or-..."
export ANTHROPIC_MODEL="meta-llama/llama-3.3-70b-instruct:free"
export ANTHROPIC_SMALL_FAST_MODEL="qwen/qwen3-8b:free"
claude
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys). OpenRouter's free tier has aggressive rate limits but no monthly cap.

**Working free coding models (2026):**

| Model | Best for |
|-------|----------|
| `meta-llama/llama-3.3-70b-instruct:free` | General coding, strong instruction following |
| `qwen/qwen-2.5-coder-32b-instruct:free`  | Pure code generation — the strongest free coder |
| `deepseek/deepseek-r1:free`              | Multi-step reasoning, debugging |
| `google/gemma-3-27b-it:free`             | Balanced reasoning + coding |
| `mistralai/mistral-7b-instruct:free`     | Lowest latency, simple tasks |
| `qwen/qwen3-8b:free`                     | Fast classification and tool routing |

## Engine 3 — Local (Ollama + y-router)

**Use when:** you need zero data egress (regulated industry, air-gapped environment), zero rate limits, or want to iterate overnight without burning API budget.

### Prerequisites

1. Install [Ollama](https://ollama.com/download)
2. Pull coding models:
   ```bash
   ollama pull qwen2.5-coder:32b   # primary
   ollama pull qwen2.5-coder:7b    # small/fast
   ```
3. Install y-router (Anthropic-compatible proxy for OpenAI-style upstreams):
   ```bash
   npm install -g @musistudio/y-router
   # or use LiteLLM if you prefer Python:
   pip install 'litellm[proxy]'
   ```
4. Start the proxy on port 8787:
   ```bash
   y-router --upstream http://localhost:11434 --port 8787
   ```

### Run Claude Code against it

```bash
export ANTHROPIC_BASE_URL="http://localhost:8787"
export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_MODEL="qwen2.5-coder:latest"
claude
```

### Hardware targets

| GPU VRAM | Recommended model         | Tokens/sec |
|----------|---------------------------|------------|
| 8 GB     | `qwen2.5-coder:7b`        | ~40        |
| 16 GB    | `qwen2.5-coder:14b`       | ~25        |
| 24 GB    | `qwen2.5-coder:32b` (Q4)  | ~18        |
| 48 GB+   | `qwen2.5-coder:32b` (Q8)  | ~22        |
| CPU only | `qwen2.5-coder:7b` (Q4)   | ~4         |

## Engine benchmarks

Every PR to `main` runs the engine benchmark harness via `.github/workflows/engine-bench.yml`, scoring all three engines across six dimensions:

1. **Reasoning** — multi-step logic tests
2. **Tokenization** — context utilization and cost per 1K tokens
3. **Management** — task orchestration and parallel tool calls
4. **Research** — documentation retrieval accuracy
5. **Brain** — MCP memory persistence across sessions
6. **Skill** — code generation quality and slash-command execution

Results land at `docs/benchmark-results.md`.

## Recommended workflow

- **Morning standup prep, doc writing, sprint planning** → `cc-free` (free, good enough)
- **Feature development, refactoring, reviews** → `cc-paid` (best quality)
- **Long-running autonomous loops overnight** → `cc-local` (no rate limits, no bill)
- **Regulated data (HIPAA, GDPR, SOC2 scoped) or air-gapped** → `cc-local` (zero egress)

## Vault Links

- [[../README|Project README]]
- [[../.claude/CLAUDE|CLAUDE.md]]
- [[../Makefile|Makefile]]
- [[adr/ADR-001-fastapi|ADR-001]]
