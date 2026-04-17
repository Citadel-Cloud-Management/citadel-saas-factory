# Citadel SaaS Factory — Justfile
# Usage: just <recipe>
# Install just: cargo install just || brew install just || npm i -g just

# Default recipe
default: status

# Bootstrap everything in parallel
bootstrap:
    ./scripts/parallel-bootstrap.sh

# Dry run bootstrap
bootstrap-dry:
    ./scripts/parallel-bootstrap.sh --dry-run

# Detect business vertical
detect:
    ./scripts/detect-business.sh

# Install models (Ollama + open-weights)
models:
    ./scripts/install-models.sh

# Install MCP servers
mcp:
    ./scripts/install-mcp.sh

# Install git hooks
hooks:
    ./scripts/install-hooks.sh

# Render agents to all IDE formats
render-agents:
    ./scripts/render-agents.sh

# Run model evaluations
eval:
    npx promptfoo eval -c evals/promptfoo.yaml

# Run verification
verify:
    ./scripts/verify-install.sh

# System status
status:
    @echo "=== Citadel SaaS Factory Status ==="
    @echo "Agents: $(grep -c '^  - id:' .claude/agents/_registry.yaml 2>/dev/null || echo 0)"
    @echo "Models: $(grep -c '    - id:' models/catalog.yaml 2>/dev/null || echo 0)"
    @echo "Rules: $(ls .claude/rules/*.md 2>/dev/null | wc -l || echo 0)"
    @echo "Skills: $(ls -d .claude/skills/*/ 2>/dev/null | wc -l || echo 0)"
    @echo "Scripts: $(ls scripts/*.sh 2>/dev/null | wc -l || echo 0)"
    @echo "Providers: $(ls agents/providers/*.yaml 2>/dev/null | wc -l || echo 0)"

# Clean generated files
clean:
    rm -rf logs/bootstrap/ BUSINESS_PROFILE.yaml
    rm -rf .cursor/subagents/ .antigravity/workflows/

# Lint docs
docs-lint:
    vale docs/ 2>/dev/null || echo "Install vale: brew install vale"
    cspell docs/**/*.md 2>/dev/null || echo "Install cspell: npm i -g cspell"
