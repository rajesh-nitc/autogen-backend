SHELL := /bin/bash
APP_NAME=autogen-backend
DB_NAME=autogen-db

.PHONY: run_db run_embeddings run_app run_app_docker precommit

run_db: ## Run pgvector
	docker network create autogen-network || true
	docker run --name $(DB_NAME) \
	--network=autogen-network \
  	-e POSTGRES_USER=chatuser \
  	-e POSTGRES_DB=chatdb \
	--env-file <(env | grep -E 'POSTGRES_PASSWORD') \
  	-p 5432:5432 \
  	-d pgvector/pgvector:pg16

run_embeddings: ## Run embeddings
	uv run embeddings.py

run_app: ## Run app
	uv sync --frozen
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

run_app_docker: ## Run app in docker
	docker build -t $(APP_NAME) .
	docker run -d -p 8000:8000 \
	--network=autogen-network \
	-e RUN_DOCKER=1 \
	--env-file <(env | grep -E 'AZURE_OPENAI_API_KEY|POSTGRES_PASSWORD|OPENWEATHER_API_KEY') \
    --name $(APP_NAME) \
    $(APP_NAME)

precommit: ## Run pre-commit
	uv run pre-commit install
	uv run pre-commit run --all-files
