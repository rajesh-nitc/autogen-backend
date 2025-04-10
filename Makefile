SHELL := /bin/bash

APP_CONTAINER=autogen-backend
DB_CONTAINER=autogen-db
DOCKER_NETWORK=autogen-network
POSTGRES_USER=chatuser
POSTGRES_DB=chatdb

.PHONY: run_db run_embeddings run_app run_app_docker precommit

run_db:
	docker network create $(DOCKER_NETWORK) || true
	docker run --name $(DB_CONTAINER) \
	--network=$(DOCKER_NETWORK) \
  	-e POSTGRES_USER=$(POSTGRES_USER) \
  	-e POSTGRES_DB=$(POSTGRES_DB) \
	--env-file <(env | grep -E 'POSTGRES_PASSWORD') \
  	-p 5432:5432 \
  	-d pgvector/pgvector:pg16

run_embeddings:
	uv run embeddings.py

run_app:
	uv sync --frozen
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

run_app_docker:
	docker build -t $(APP_CONTAINER) .
	docker run -d -p 8000:8000 \
	--network=$(DOCKER_NETWORK) \
	-e RUN_DOCKER=1 \
	--env-file <(env | grep -E 'AZURE_OPENAI_API_KEY|POSTGRES_PASSWORD|OPENWEATHER_API_KEY') \
    --name $(APP_CONTAINER) \
    $(APP_CONTAINER)

precommit:
	uv run pre-commit install
	uv run pre-commit run --all-files
