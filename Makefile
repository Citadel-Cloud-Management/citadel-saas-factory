.PHONY: help dev stop backend frontend test lint security deploy clean vault-sync vault-audit vault-generate wiki-ingest wiki-lint wiki-sync run-paid run-free run-local engine-status

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

vault-generate: ## Regenerate the 265 agent notes in docs/vault/agents/
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
