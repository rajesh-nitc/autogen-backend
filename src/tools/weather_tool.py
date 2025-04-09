from typing import Annotated, Any

from src.core.settings import settings
from src.utils.http_client import HTTPClientSingleton


async def get_location_coordinates_tool(
    location: Annotated[
        str,
        "Location e.g. Paris,FR; New York,NY,US. Use ISO 3166-1 alpha-2 country codes",
    ],
) -> Annotated[dict[str, float], "Returns latitude (lat) and longitude (lon)"]:
    """Tool function to retrieve geographic coordinates for a given location name."""
    weather_client = HTTPClientSingleton.get_instance(
        base_url=settings.APIS.WEATHER.BASE_URL, timeout=settings.APIS.WEATHER.TIMEOUT
    )
    response = await weather_client.get(
        "/geo/1.0/direct",
        params={
            "q": location,
            "appid": settings.APIS.WEATHER.API_KEY.get_secret_value(),
        },
    )
    response.raise_for_status()
    data = response.json()
    required_data = {
        "lat": data[0]["lat"],
        "lon": data[0]["lon"],
    }
    return required_data


async def get_weather_by_coordinates_tool(
    lat: Annotated[float, "Latitude"], lon: Annotated[float, "Longitude"]
) -> Annotated[Any, "Returns weather data"]:  # noqa: ANN401
    """Tool function to retrieve current weather data based on geographic coordinates."""
    weather_client = HTTPClientSingleton.get_instance(
        base_url=settings.APIS.WEATHER.BASE_URL, timeout=settings.APIS.WEATHER.TIMEOUT
    )
    response = await weather_client.get(
        "/data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "appid": settings.APIS.WEATHER.API_KEY.get_secret_value(),
        },
    )
    response.raise_for_status()
    data = response.json()
    return data.get("main")
