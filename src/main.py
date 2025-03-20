import logging

from fastapi import FastAPI

from src.core.logging import setup_logging
from src.core.security import setup_cors
from src.core.settings import settings
from src.events.lifespan import lifespan
from src.routers import chat, health

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="autogen-backend",
    description="autogen-backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(chat.router, prefix="/ws", tags=["chat"])
app.include_router(health.router, prefix="/api", tags=["health"])
setup_cors(app)

logger.info(f"Loaded application settings: {settings.model_dump()}")
