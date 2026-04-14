#!/usr/bin/env bash
set -euo pipefail
cp .env.example .env 2>/dev/null || true
chmod +x setup.sh start.sh stop.sh scripts/*.sh || true
