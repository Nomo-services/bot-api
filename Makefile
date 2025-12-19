#!/usr/bin/make

include .env

run-docker-compose:
	docker compose -f docker/docker-compose.yaml up -d --build

stop-docker-compose:
	docker compose -f docker/docker-compose.yaml down

run-database:
	docker compose -f docker/docker-compose.yaml up -d nomo-db

stop-database:
	docker compose -f docker/docker-compose.yaml down nomo-db

run-app:
	uvicorn src.main:app --reload --port $(APP_PORT)

# make revision msg="message"
.PHONY: revision
revision:
	@if [ -z "$(msg)" ]; then \
		echo "ERROR: you must pass MSG=\"your message\""; \
		exit 1; \
	fi

	alembic upgrade head

	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade base
	
lint:
	ruff check src
