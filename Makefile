APP_NAME=autogen-backend

.PHONY: help run precommit docker docker_clean

help: ## Self-documenting help command
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

run: ## Run the application locally
	uv sync
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

precommit: ## Run pre-commit checks
	uv run pre-commit install
	uv run pre-commit run --all-files

docker: ## Run in docker (Add Openai API key, OpenWeather API key and update other variables)
	sudo docker build -t $(APP_NAME) .
	sudo docker run -d -p 8000:8000 \
		-e AZURE_OPENAI_API_KEY="" \
		-e AZURE_OPENAI_API_VERSION="2024-10-21" \
		-e AZURE_OPENAI_ENDPOINT="https://autogen-backend.openai.azure.com/" \
        -e ENV="local" \
		-e HTTP_CLIENT_BASE_URL="https://api.openweathermap.org" \
        -e LLM_MODEL="gpt-4o-mini" \
        -e LLM_SYSTEM_INSTRUCTION="You are a helpful assistant." \
		-e OPENWEATHER_API_KEY="" \
        --name $(APP_NAME) \
        $(APP_NAME)

docker_clean: ## Stop and remove the Docker container
	sudo docker stop $(APP_NAME)
	sudo docker rm $(APP_NAME)
