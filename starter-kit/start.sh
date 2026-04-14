#!/usr/bin/env bash
set -euo pipefail

[[ -f .env ]] || cp .env.example .env

docker compose up --build -d

echo "Services starting..."
echo "UI:         http://localhost:3000"
echo "API docs:   http://localhost:8000/docs"
echo "Prometheus: http://localhost:9090"
echo "Grafana:    http://localhost:3001"
