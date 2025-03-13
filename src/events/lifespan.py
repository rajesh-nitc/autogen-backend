from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.utils.http_client import HTTPClientSingleton


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Application startup tasks
    HTTPClientSingleton.get_instance()
    yield  # This represents the lifespan of the application

    # Application shutdown tasks
    await HTTPClientSingleton.close_instance()
