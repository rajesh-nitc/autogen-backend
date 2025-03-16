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

2. **OpenWeather Authentication**:

```
echo 'export OPENWEATHER_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

3. **Application Settings**: Update `src/core/settings.py`


### Run

```
# Run
make run

# Run in Docker - Add AZURE_OPENAI_API_KEY, OPENWEATHER_API_KEY in Makefile
make docker

```

### Test with Postman

URL:
```
ws://localhost:8000/ws/chat
```

Message:
```
{
    "content": "what is 1+1 and how is the weather in bengaluru and mumbai?",
    "source": "user"
}

```
