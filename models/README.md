# Models — Multi-Model AI Routing

12 providers, 12 tiers. Agents reference tiers, not specific models. Swap providers by changing one env var.

## Files

| File | Purpose |
|------|---------|
| `catalog.yaml` | All model definitions with capabilities |
| `routing.yaml` | Tier-based routing rules |
| `embeddings.yaml` | Embedding model configuration |
| `vision.yaml` | Vision model configuration |
| `rerankers.yaml` | Reranker model configuration |
| `engines/` | Engine configs (paid, free, local) |

## Tiers

| Tier | Default Model | Use Case |
|------|---------------|----------|
| `reasoning_deep` | Claude Opus 4.6 | Architecture, critical decisions |
| `reasoning_fast` | Claude Sonnet 4.6 | Default coding tasks |
| `cheap_fast` | Claude Haiku 4.5 | Completion, boilerplate |
| `local_only` | Llama 4 Maverick | Air-gapped, zero cost |

## Switch Engine

```bash
bash models/engines/switch-engine.sh local   # Ollama (free)
bash models/engines/switch-engine.sh paid    # Anthropic/OpenAI
bash models/engines/switch-engine.sh free    # OpenRouter free tier
```

## Add a Provider

1. Add model entry to `catalog.yaml`
2. Map to tier in `routing.yaml`
3. Add API key to `.env`
