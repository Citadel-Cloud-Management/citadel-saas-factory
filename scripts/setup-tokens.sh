#!/usr/bin/env bash
set -euo pipefail

echo "=== Citadel SaaS Factory — Token Setup ==="
echo ""

# Anthropic API Key
read -sp "Enter your Anthropic API Key (sk-ant-...): " ANTHROPIC_API_KEY
echo ""

if [[ -z "$ANTHROPIC_API_KEY" ]]; then
  echo "Error: Anthropic API Key is required."
  exit 1
fi

# GitHub Personal Access Token
read -sp "Enter your GitHub Personal Access Token (ghp_...): " GITHUB_TOKEN
echo ""

if [[ -z "$GITHUB_TOKEN" ]]; then
  echo "Error: GitHub Token is required."
  exit 1
fi

# Write to shell profile
PROFILE="${HOME}/.bashrc"
if [[ -f "${HOME}/.zshrc" ]]; then
  PROFILE="${HOME}/.zshrc"
fi

{
  echo ""
  echo "# Citadel SaaS Factory tokens"
  echo "export ANTHROPIC_API_KEY=\"${ANTHROPIC_API_KEY}\""
  echo "export GITHUB_TOKEN=\"${GITHUB_TOKEN}\""
  echo "export GITHUB_PERSONAL_ACCESS_TOKEN=\"${GITHUB_TOKEN}\""
} >> "$PROFILE"

# Export for current session
export ANTHROPIC_API_KEY
export GITHUB_TOKEN
export GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_TOKEN"

# Authenticate GitHub CLI
echo ""
echo "Authenticating GitHub CLI..."
echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null && echo "GitHub CLI authenticated." || echo "Warning: gh auth failed. Install GitHub CLI first."

echo ""
echo "Tokens saved to $PROFILE"
echo "Run: source $PROFILE"
echo "Done."
