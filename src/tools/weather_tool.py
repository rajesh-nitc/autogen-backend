from typing import Annotated, Any

from src.core.settings import settings
from src.utils.http_client import HTTPClientSingleton


async def get_location_coordinates(
    location: Annotated[
        str,
        "Location e.g. Paris,FR; New York,NY,US. Use ISO 3166-1 alpha-2 country codes",
    ],
) -> Annotated[dict[str, float], "Returns latitude (lat) and longitude (lon)"]:
    client = HTTPClientSingleton.get_instance()
    response = await client.get(
        "/geo/1.0/direct",
        params={"q": location, "appid": settings.OPENWEATHER_API_KEY},
    )
    response.raise_for_status()
    data = response.json()
    required_data = {
        "lat": data[0]["lat"],
        "lon": data[0]["lon"],
    }
    return required_data


async def get_weather_by_coordinates(
    lat: Annotated[float, "Latitude"], lon: Annotated[float, "Longitude"]
) -> Annotated[Any, "Returns weather info"]:
    client = HTTPClientSingleton.get_instance()
    response = await client.get(
        "/data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "appid": settings.OPENWEATHER_API_KEY,
        },
    )
    response.raise_for_status()
    data = response.json()
    return data
