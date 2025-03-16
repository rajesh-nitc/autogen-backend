import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.settings import settings
from src.utils.http_client import HTTPClientSingleton

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup tasks
    logger.info(f"Loaded application settings: {settings.model_dump()}")
    # Initialize a client for each API using its base URL
    HTTPClientSingleton.get_instance(base_url=settings.APIS.WEATHER.BASE_URL)

    yield  # This represents the lifespan of the application

    # Application shutdown tasks
    await HTTPClientSingleton.close_all_instances()
