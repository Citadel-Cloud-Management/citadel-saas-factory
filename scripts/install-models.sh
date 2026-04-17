#!/usr/bin/env bash
# Install model infrastructure — Ollama + open-weights models + .env.example
# Idempotent: skips already-installed components
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() { echo "[models] $*"; }

# Install Ollama if not present
if ! command -v ollama &>/dev/null; then
  log "Installing Ollama..."
  if [[ "$(uname)" == "Darwin" ]]; then
    brew install ollama 2>/dev/null || curl -fsSL https://ollama.ai/install.sh | sh
  elif [[ "$(uname)" == "Linux" ]]; then
    curl -fsSL https://ollama.ai/install.sh | sh
  else
    log "Windows detected — install Ollama from https://ollama.ai/download"
  fi
else
  log "Ollama already installed"
fi

# Pull open-weights models in parallel (if Ollama is running)
if command -v ollama &>/dev/null; then
  log "Pulling open-weights models (background)..."
  models=(
    "llama3.3:latest"
    "qwen2.5-coder:32b"
    "nomic-embed-text:latest"
  )
  for model in "${models[@]}"; do
    if ! ollama list 2>/dev/null | grep -qF "$model"; then
      ollama pull "$model" &
      log "  Queued: $model"
    else
      log "  Already pulled: $model"
    fi
  done
  wait
fi

# Generate .env.example with all provider key slots
if [[ ! -f "$REPO_ROOT/.env.example" ]]; then
  log "Generating .env.example..."
  cat > "$REPO_ROOT/.env.example" << 'ENVEOF'
# ─── Model Provider API Keys ───
# Set the keys for providers you want to use. At minimum, set one.
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
XAI_API_KEY=
DEEPSEEK_API_KEY=
MISTRAL_API_KEY=
COHERE_API_KEY=
VOYAGE_API_KEY=
JINA_API_KEY=
ELEVENLABS_API_KEY=

# ─── Gateway Keys ───
OPENROUTER_API_KEY=
TOGETHER_API_KEY=
FIREWORKS_API_KEY=
GROQ_API_KEY=
CEREBRAS_API_KEY=

# ─── Cloud Provider Keys ───
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
GOOGLE_APPLICATION_CREDENTIALS=

# ─── Service Keys ───
GITHUB_TOKEN=
STRIPE_SECRET_KEY=
DATABASE_URL=
REDIS_URL=

# ─── Cost Controls ───
DAILY_MODEL_BUDGET=50
OFFLINE_MODE=false

# ─── LiteLLM Proxy ───
LITELLM_MASTER_KEY=
LITELLM_PORT=4000
ENVEOF
else
  log ".env.example already exists"
fi

log "Models installation complete"
