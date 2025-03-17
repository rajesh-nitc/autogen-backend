from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class AzureOpenAISettings(BaseSettings):
    """Azure OpenAI settings."""

    API_KEY: SecretStr = Field(
        ...,  # Required field (this means it must be provided through env)
        alias="AZURE_OPENAI_API_KEY",
        description="Azure OpenAI API key.",
    )
    API_VERSION: str = Field(
        "2024-10-21",
        description="Latest GA API release.",
    )
    ENDPOINT: str = Field(
        "https://autogen-backend-01.openai.azure.com/",
        description="Azure OpenAI endpoint.",
    )
    MODEL: Literal["gpt-4", "gpt-4o", "gpt-4o-mini"] = Field(
        "gpt-4o-mini", description="LLM model."
    )


class WeatherSettings(BaseSettings):
    """Weather API settings."""

    BASE_URL: str = Field(
        "https://api.openweathermap.org", description="OpenWeather API base URL"
    )
    API_KEY: SecretStr = Field(
        ...,  # Required field
        alias="OPENWEATHER_API_KEY",
        description="OpenWeather API key.",
    )
    TIMEOUT: float = Field(10.0, description="Timeout for Weather API requests")


class APIsSettings(BaseSettings):
    """APIs settings."""

    WEATHER: WeatherSettings = WeatherSettings()  # type: ignore


class Settings(BaseSettings):
    """Application settings."""

    APIS: APIsSettings = APIsSettings()
    AZURE_OPENAI: AzureOpenAISettings = AzureOpenAISettings()  # type: ignore
    ENV: Literal["local", "dev", "npr", "prd"] = Field(
        "local", description="Application environment."
    )


settings = Settings()  # type: ignore
