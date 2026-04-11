.PHONY: help dev stop backend frontend test lint security deploy clean

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
