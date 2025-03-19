SHELL := /bin/bash
APP_NAME=autogen-backend
DB_NAME=autogen-db

.PHONY: help run db run_docker precommit

help: ## Self-documenting help command
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

run: ## Run app
	uv sync --frozen
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

db: ## Run PostgreSQL
	docker network create autogen-network || true
	docker run --name $(DB_NAME) \
	--network=autogen-network \
  	-e POSTGRES_USER=chatuser \
  	-e POSTGRES_DB=chatdb \
	--env-file <(env | grep -E 'POSTGRES_PASSWORD') \
  	-p 5432:5432 \
  	-d postgres

run_docker: ## Run app in docker
	docker build -t $(APP_NAME) .
	docker run -d -p 8000:8000 \
	--network=autogen-network \
	--env-file <(env | grep -E 'AZURE_OPENAI_API_KEY|POSTGRES_PASSWORD|OPENWEATHER_API_KEY') \
    --name $(APP_NAME) \
    $(APP_NAME)

precommit: ## Run pre-commit
	uv run pre-commit install
	uv run pre-commit run --all-files
