# autogen-backend

This API uses Autogen framework

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
ws://localhost:8000/ws/chat/sessionidfoo
```

Message:

```
{
    "content": "how is the weather in bengaluru and mumbai?",
    "source": "user"
}

```
