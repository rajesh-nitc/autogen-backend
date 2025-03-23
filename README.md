# autogen-backend

This API uses the Autogen framework.

A new run is created for every user request sent via websocket and stored in the database. The team state is reset for the user at every (n+1)th run, regardless of the session. 

## Features

1. **Generation with APIs** (e.g., `get_location_coordinates`, `get_weather_by_coordinates`)
2. **Generation with Vector Search** - TODO

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
make db

# Run app
make run

# Run app in Docker
make run_docker

```

### Test with Postman

URL:

```
ws://localhost:8000/ws/chat/session-foo
```

Message:

```
{
    "content": "how is the weather in bengaluru and mumbai?",
    "source": "user"
}

```
