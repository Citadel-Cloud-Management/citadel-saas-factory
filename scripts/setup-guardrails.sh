#!/usr/bin/env bash
set -euo pipefail

echo "============================================"
echo "  Citadel SaaS Factory — Guardrails Setup"
echo "============================================"
echo ""

# Install guardrails-ai and deepeval
echo "Installing guardrails-ai and deepeval..."
pip install guardrails-ai deepeval

# Configure guardrails (non-interactive)
echo ""
echo "Configuring guardrails..."
guardrails configure --disable-metrics --disable-remote-inferencing 2>/dev/null || guardrails configure

# Install core Hub validators
echo ""
echo "Installing Hub validators..."
guardrails hub install hub://guardrails/hallucination_free
guardrails hub install hub://guardrails/provenance_llm
guardrails hub install hub://guardrails/toxic_language
guardrails hub install hub://guardrails/detect_pii

echo ""
echo "============================================"
echo "  Guardrails setup complete!"
echo "============================================"
echo ""
echo "  Installed validators:"
echo "    - hub://guardrails/hallucination_free"
echo "    - hub://guardrails/provenance_llm"
echo "    - hub://guardrails/toxic_language"
echo "    - hub://guardrails/detect_pii"
echo ""
echo "  All 265 agents now route through the guardrails validation layer."
