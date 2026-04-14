SHELL := /bin/bash

.PHONY: help setup up down logs reset ps lint

help:
	@echo "make setup  - prepare environment"
	@echo "make up     - build and start all services"
	@echo "make down   - stop all services"
	@echo "make logs   - stream logs"
	@echo "make reset  - stop and remove volumes"
	@echo "make ps     - show service status"

setup:
	chmod +x setup.sh start.sh stop.sh scripts/*.sh || true
	./setup.sh

up:
	./start.sh

down:
	./stop.sh

logs:
	docker compose logs -f --tail=200

reset:
	docker compose down -v --remove-orphans

ps:
	docker compose ps
