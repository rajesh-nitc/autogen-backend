import os
from typing import Any, Literal

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
        "https://autogen-backend-local.openai.azure.com/",
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


class DatabaseSettings(BaseSettings):
    """Database settings."""

    POSTGRES_HOST: str = Field(
        "autogen-db" if os.getenv("RUN_DOCKER") else "localhost",
        description="Database host",
    )
    POSTGRES_PORT: int = Field(5432, description="Database port")
    POSTGRES_USER: str = Field("chatuser", description="Database user")
    POSTGRES_PASSWORD: SecretStr = Field(..., description="Database password")
    POSTGRES_DB: str = Field("chatdb", description="Database name")

    @property
    def postgres_url(self) -> str:
        """Database connection URL."""
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD.get_secret_value()
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        db = self.POSTGRES_DB
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"


class Settings(BaseSettings):
    """Application settings."""

    APIS: APIsSettings = APIsSettings()
    AZURE_OPENAI: AzureOpenAISettings = AzureOpenAISettings()  # type: ignore
    DATABASE: DatabaseSettings = DatabaseSettings()  # type: ignore
    ENV: Literal["local", "dev", "npr", "prd"] = Field(
        "local", description="Application environment."
    )

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize settings and apply environment-specific overrides."""
        super().__init__(**kwargs)

        # Sample environment-specific overrides
        if self.ENV == "dev":
            self.AZURE_OPENAI.ENDPOINT = "https://autogen-backend-dev.openai.azure.com/"
        if self.ENV == "npr":
            self.AZURE_OPENAI.ENDPOINT = "https://autogen-backend-npr.openai.azure.com/"
        elif self.ENV == "prd":
            self.AZURE_OPENAI.ENDPOINT = "https://autogen-backend-prd.openai.azure.com/"


settings = Settings()  # type: ignore
