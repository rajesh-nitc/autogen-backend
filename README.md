# autogen-backend

This API uses the Autogen framework.

A new run is created for every user request sent via websocket and stored in the database. The team state is reset for the user at the completion of every nth run, regardless of the session.
 

## Features

1. **Generation with APIs** (e.g., `get_location_coordinates_tool`, `get_weather_by_coordinates_tool`)
2. **Generation with Vector Search** (e.g., `get_vector_search_tool`)

## Getting Started 🚀

### Prerequisites

1. **Azure Authentication**:

```
echo 'export AZURE_OPENAI_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

2. **PostgresSQL Authentication**:

```
echo 'export POSTGRES_PASSWORD=YOUR_PASSWORD_HERE' >> ~/.zshrc
```

3. **OpenWeather Authentication**:

```
echo 'export OPENWEATHER_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

### Run

```
# Run db
make run_db

# Run embeddings
make run_embeddings

# Run app
make run_app

# Run app in Docker
make run_app_docker

```

### Test with Postman

URL:

```
ws://localhost:8000/ws/chat/session-foo
```

**Generation with APIs**:
```
{
    "content": "how is the weather in bengaluru and mumbai?",
    "source": "user"
}

```
**Generation with Vector Search**:
```
{
    "content": "how much is it to include family in health plan?",
    "source": "user"
}
```

**Note**: The data is sourced from ```azure-search-openai-demo```