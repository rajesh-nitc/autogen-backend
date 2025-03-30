# autogen-backend

This API uses the Autogen framework.

A new run is created for every user request sent via websocket and stored in the database. The team state is reset for the user at the completion of every nth run, regardless of the session.

The data for vector search is taken from `azure-search-openai-demo` repo.
 

## Use Cases

1. **Generation with APIs** (e.g., `get_location_coordinates_tool`, `get_weather_by_coordinates_tool`)
2. **Generation with Vector Search** (e.g., `get_vector_search_tool`)

## Getting Started 🚀

### Prerequisites

1. **Azure Authentication**

```
echo 'export AZURE_OPENAI_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

2. **PostgresSQL Authentication**

```
echo 'export POSTGRES_PASSWORD=YOUR_PASSWORD_HERE' >> ~/.zshrc
```

3. **OpenWeather Authentication**

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

# Run app in docker
make run_app_docker

```

### Test with Postman

```
ws://localhost:8000/ws/chat/session-foo
```

**Generation with APIs**
```
{
    "content": "how is the weather in bengaluru and mumbai?",
    "source": "user"
}

```
**Generation with Vector Search**
```
{
    "content": "how much will be deducted from salary for the standard plan?",
    "source": "user"
}
```
