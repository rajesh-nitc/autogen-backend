# autogen-backend

A backend API powered by [Autogen](https://github.com/microsoft/autogen).

A new run is created for every user request sent via websocket and stored in the database. The team state is reset for the user at the completion of every nth run, regardless of the session. (temporary workaround for https://github.com/microsoft/autogen/issues/6227)

The data for vector search is taken from `azure-search-openai-demo` repo.
 

## Use Cases

1. **Generation with APIs** (`WeatherAgent`)
2. **Generation with Vector Search** (`VectorSearchAgent`)

## Getting Started 🚀

### Prerequisites

```bash
# Azure OpenAI
echo 'export AZURE_OPENAI_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc

# PostgresSQL
echo 'export POSTGRES_PASSWORD=YOUR_PASSWORD_HERE' >> ~/.zshrc

# OpenWeather
echo 'export POSTGRES_PASSWORD=YOUR_PASSWORD_HERE' >> ~/.zshrc
```

### Run

```bash
# Run db
make run_db

# Run embeddings
make run_embeddings

# Run app
make run_app

# OR run app in docker
make run_app_docker

```

### Test with Postman

```bash
# URL
ws://localhost:8000/ws/chat/session-foo

# Message format
{
  "content": "your message here",
  "source": "user"
}
```

## Examples
### 1. Generation with APIs (`WeatherAgent`)
**Request**
```json
{
    "content": "how is the weather in bengaluru and mumbai?",
    "source": "user"
}

```
**Response**
```json
{
    "source": "WeatherAgent",
    "models_usage": {
        "prompt_tokens": 477,
        "completion_tokens": 140
    },
    "metadata": {},
    "content": "The current weather in Bengaluru and Mumbai is as follows:\n\n**Bengaluru:**\n- Temperature: 300.49 K (approximately 27.34 °C)\n- Feels Like: 300.27 K (approximately 27.12 °C)\n- Humidity: 40%\n- Pressure: 1012 hPa\n\n**Mumbai:**\n- Temperature: 303.48 K (approximately 30.33 °C)\n- Feels Like: 305.05 K (approximately 31.90 °C)\n- Humidity: 52%\n- Pressure: 1009 hPa\n\nWould you like to know anything else? \n\nTERMINATE",
    "type": "TextMessage"
}
```
### 2. Generation with Vector Search (`VectorSearchAgent`)
**Request**
```json
{
    "content": "how much will be deducted from salary for the standard plan?",
    "source": "user"
}
```

**Response**
```json
{
    "source": "VectorSearchAgent",
    "models_usage": {
        "prompt_tokens": 1107,
        "completion_tokens": 102
    },
    "metadata": {},
    "content": "{\n    \"answer\": \"For the Northwind Standard plan, the premium amounts deducted from salary are as follows: $45.00 for Employee Only, $65.00 for Employee +1, and $78.00 for Employee +2 or more. These deductions are taken from payroll on a pre-determined schedule.\",\n    \"sources\": [\n        {\n            \"source\": \"data/Benefit_Options.pdf\",\n            \"page_label\": \"4\"\n        }\n    ]\n}\n\nTERMINATE",
    "type": "TextMessage"
}
```
