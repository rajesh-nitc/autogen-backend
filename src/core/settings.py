from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str = Field(
        ...,  # Required field (this means it must be provided through env)
        json_schema_extra={"env": "AZURE_OPENAI_API_KEY"},
        description="Azure OpenAI API key.",
    )
    AZURE_OPENAI_API_VERSION: str = Field(
        "2024-10-21",
        description="Latest GA API release.",
    )
    AZURE_OPENAI_ENDPOINT: str = Field(
        "https://autogen-backend.openai.azure.com/",
        description="Azure OpenAI endpoint.",
    )
    ENV: Literal["local", "dev", "npr", "prd"] = Field(
        "local", description="Application environment."
    )
    HTTP_CLIENT_BASE_URL: str = Field(
        "https://api.openweathermap.org", description="OpenWeather API base url"
    )
    LLM_MODEL: Literal[
        "gpt-4",
        "gpt-4o",
        "gpt-4o-mini",
    ] = Field("gpt-4o-mini", description="The foundation model to use.")
    LLM_SYSTEM_INSTRUCTION: str = Field(
        "You are a helpful assistant.",
        description="System instruction for the Model.",
    )
    OPENWEATHER_API_KEY: str = Field(
        ...,  # Required field (this means it must be provided through env)
        json_schema_extra={"env": "OPENWEATHER_API_KEY"},
        description="OpenWeather API key.",
    )


settings = Settings()  # type: ignore
