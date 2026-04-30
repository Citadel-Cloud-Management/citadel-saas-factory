.PHONY: help dev stop backend frontend test lint security deploy clean vault-sync vault-audit vault-generate wiki-ingest wiki-lint wiki-sync run-paid run-free run-local engine-status strategy-html bootstrap-parallel bootstrap-dry detect-business install-models install-mcp install-hooks setup-claude setup-claude-target render-agents eval ai-setup ai-eval ai-eval-mock ai-eval-dry ai-prompt-lint ai-agent ai-agent-mock ai-validate ai-list-tasks ai-list-tools status sync-adapters

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start full development stack
	docker compose up -d
	@echo "Stack running: postgres:5432 redis:6379 keycloak:8080 minio:9000 rabbitmq:5672 mailhog:8025"

stop: ## Stop all services
	docker compose down

backend: ## Start backend dev server
	cd backend && uvicorn app.main:app --reload --port 8000

frontend: ## Start frontend dev server
	cd frontend && npm run dev

test: ## Run all tests
	cd backend && pytest
	cd frontend && npm test

lint: ## Run linters
	cd backend && ruff check .
	cd frontend && npm run lint

security: ## Run security scans
	semgrep --config auto backend/
	trivy fs --severity HIGH,CRITICAL .

deploy: ## Deploy to target environment
	./scripts/deploy.sh

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
	docker compose down -v

vault-generate: ## Regenerate the 500+ agent notes in docs/vault/agents/
	python scripts/generate-vault.py
	python scripts/sync-vault-memory.py

vault-sync: ## Refresh Graphify knowledge graph + memory mirrors in the Obsidian vault
	graphify . --update --obsidian-dir docs/vault/knowledge-graph 2>/dev/null || echo "  (graphify not installed — skipping knowledge graph refresh)"
	python scripts/sync-vault-memory.py
	@echo "Vault sync complete. Open docs/vault/ in Obsidian."

vault-audit: ## Invoke the obsidian-curator agent to audit vault integrity
	@echo "Invoking obsidian-curator agent to audit docs/vault/..."
	@echo "  In Claude Code, run: use the obsidian-curator subagent to audit the vault"
	@echo "  Or run the headless audit: python scripts/vault-autolink.py docs/vault/_index.md"

wiki-ingest: ## Ingest a raw source into the LLM Wiki (usage: make wiki-ingest FILE=raw/articles/foo.md)
	@if [ -z "$(FILE)" ]; then echo "Usage: make wiki-ingest FILE=raw/articles/foo.md"; exit 1; fi
	@echo "Ingesting docs/vault/$(FILE) into the LLM Wiki..."
	@echo "  In Claude Code, run: /project:wiki-ingest $(FILE)"
	@echo "  The wiki-curator agent will update entities, concepts, index, and log."

wiki-lint: ## Health-check the LLM Wiki (orphans, stale claims, missing cross-refs, data gaps)
	@echo "Linting docs/vault/wiki/..."
	@echo "  In Claude Code, run: /project:wiki-lint"
	@echo "  Findings will be appended to docs/vault/wiki/log.md"

wiki-sync: ## Refresh Graphify output into the wiki and run a lint pass
	graphify . --update --obsidian-dir docs/vault/wiki/knowledge-graph 2>/dev/null || echo "  (graphify not installed — skipping knowledge graph refresh)"
	@$(MAKE) wiki-lint
	@echo "Wiki sync complete. Open docs/vault/wiki/ in Obsidian."

run-paid: ## Launch Claude Code against the paid Anthropic API (Claude 4.6)
	@bash -c 'source engines/paid.env && claude'

run-free: ## Launch Claude Code against the OpenRouter free tier
	@bash -c 'source engines/openrouter-free.env && claude'

run-local: ## Launch Claude Code against local Ollama via y-router
	@bash -c 'source engines/local-ollama.env && claude'

engine-status: ## Print the currently configured LLM engine
	@echo "Engine:   $${CITADEL_ENGINE:-unset}"
	@echo "Provider: $${CITADEL_ENGINE_PROVIDER:-unset}"
	@echo "Model:    $${ANTHROPIC_MODEL:-unset}"
	@echo "Base URL: $${ANTHROPIC_BASE_URL:-api.anthropic.com (direct)}"

strategy-html: ## Regenerate docs/strategy.html from .claude/agents/_registry.yaml
	python scripts/generate-strategy-html.py

# ─── Multi-Model & Cross-IDE Targets ───

bootstrap-parallel: ## Run parallel bootstrap (models, MCP, hooks, agents)
	./scripts/parallel-bootstrap.sh

bootstrap-dry: ## Dry-run parallel bootstrap
	./scripts/parallel-bootstrap.sh --dry-run

detect-business: ## Detect business vertical and generate BUSINESS_PROFILE.yaml
	./scripts/detect-business.sh

install-models: ## Install Ollama and open-weights models
	./scripts/install-models.sh

install-mcp: ## Install MCP server dependencies
	./scripts/install-mcp.sh

install-hooks: ## Install git hooks via Lefthook
	./scripts/install-hooks.sh

setup-claude: ## Install Claude Code master prompt + .claude/ scaffolding into this project
	./scripts/setup-claude-code.sh

setup-claude-target: ## Install Claude Code master prompt into another project (usage: make setup-claude-target TARGET=/path/to/project)
	@if [ -z "$(TARGET)" ]; then echo "Usage: make setup-claude-target TARGET=/path/to/project"; exit 1; fi
	./scripts/setup-claude-code.sh "$(TARGET)"

render-agents: ## Render agents to Cursor and Antigravity formats
	./scripts/render-agents.sh

eval: ## Run model evaluation suite (promptfoo)
	npx promptfoo eval -c evals/promptfoo.yaml

setup-skills: ## Verify and configure integrated skills library
	./scripts/setup-skills.sh

convert-skills: ## Convert skills to all agent formats (Cursor, Aider, Windsurf, etc.)
	./scripts/convert.sh --tool all

install-skills: ## Install converted skills into target project
	@echo "Usage: make install-skills TOOL=cursor TARGET=."
	./scripts/install.sh --tool $${TOOL:-cursor} --target $${TARGET:-.}

ai-setup: ## Bootstrap the AI layer (verify runtimes, structure, permissions)
	bash ai/setup.sh

ai-eval: ## Run AI layer eval suite (set ANTHROPIC_API_KEY or use ai-eval-mock)
	node ai/evals/run.js

ai-eval-mock: ## Run AI layer eval suite in mock mode (no API key needed)
	node ai/evals/run.js --mock

ai-eval-dry: ## Dry-run: validate test cases without calling the API
	node ai/evals/run.js --dry-run

ai-prompt-lint: ## Lint all AI prompt files for frontmatter and structure
	node ai/prompts/lint.js

ai-agent: ## Run an AI agent task (usage: make ai-agent TASK=summarize-document INPUT='{"document_text":"..."}')
	python3 ai/agents/run.py --task $${TASK} --input '$${INPUT}'

ai-agent-mock: ## Run an AI agent task in mock mode (usage: make ai-agent-mock TASK=summarize-document)
	python3 ai/agents/run.py --task $${TASK} --mock

ai-validate: ## Validate the entire ai/ layer integrity
	python3 ai/agents/run.py --validate

ai-list-tasks: ## List all available AI tasks
	python3 ai/agents/run.py --list-tasks

ai-list-tools: ## List all available AI tools
	python3 ai/agents/run.py --list-tools

status: ## System status (agents, models, rules, skills, providers)
	@echo "=== Citadel SaaS Factory Status ==="
	@echo "Agents:    $$(grep -c '^  - id:' .claude/agents/_registry.yaml 2>/dev/null || echo 0)"
	@echo "Models:    $$(grep -c '    - id:' models/catalog.yaml 2>/dev/null || echo 0)"
	@echo "Rules:     $$(ls .claude/rules/*.md 2>/dev/null | wc -l || echo 0)"
	@echo "Skills:    $$(ls -d .claude/skills/*/ 2>/dev/null | wc -l || echo 0)"
	@echo "Commands:  $$(ls .claude/commands/*.md .claude/commands/*.yaml 2>/dev/null | wc -l || echo 0)"
	@echo "Personas:  $$(ls .claude/agents/personas/*.md 2>/dev/null | wc -l || echo 0)"
	@echo "Providers: $$(ls agents/providers/*.yaml 2>/dev/null | wc -l || echo 0)"
	@echo "Scripts:   $$(ls scripts/*.sh 2>/dev/null | wc -l || echo 0)"

sync-adapters: ## Verify all AI instruction files reference context.md
	./scripts/sync-adapters.sh
