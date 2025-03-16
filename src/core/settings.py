from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class AzureOpenAISettings(BaseSettings):
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


class LLMSettings(BaseSettings):
    MODEL: Literal["gpt-4", "gpt-4o", "gpt-4o-mini"] = Field(
        "gpt-4o-mini", description="The foundation model to use."
    )


class WeatherSettings(BaseSettings):
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
    WEATHER: WeatherSettings = WeatherSettings()  # type: ignore


class Settings(BaseSettings):
    APIS: APIsSettings = APIsSettings()
    AZURE_OPENAI: AzureOpenAISettings = AzureOpenAISettings()  # type: ignore
    ENV: Literal["local", "dev", "npr", "prd"] = Field(
        "local", description="Application environment."
    )
    LLM: LLMSettings = LLMSettings()  # type: ignore


settings = Settings()  # type: ignore
