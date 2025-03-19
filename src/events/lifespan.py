import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from src.core.connection import db_manager
from src.core.settings import settings
from src.utils.http_client import HTTPClientSingleton

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):  # noqa: ANN201
    """Application lifespan context manager.

    :param app: FastAPI application
    """
    # Application startup tasks
    # Create database tables if they don't exist
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Initialize a client for each API using its base URL
    HTTPClientSingleton.get_instance(base_url=settings.APIS.WEATHER.BASE_URL)

    yield  # This represents the lifespan of the application

    # Application shutdown tasks
    # Dispose engine (close connection pool)
    await db_manager.engine.dispose()
    await HTTPClientSingleton.close_all_instances()
