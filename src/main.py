import logging

from fastapi import FastAPI

from src.core.logging import setup_logging
from src.core.security import setup_cors
from src.core.settings import settings
from src.events.lifespan import lifespan
from src.routers import chat_router, health_router

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="autogen-backend",
    description="autogen-backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(chat_router.router, prefix="/ws", tags=["chat"])
app.include_router(health_router.router, prefix="/api", tags=["health"])
setup_cors(app)

logger.info(f"Loaded application settings: {settings.model_dump()}")
