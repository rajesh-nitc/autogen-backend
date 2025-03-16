import logging

from fastapi import FastAPI

from src.api.routers import router
from src.core.logging import setup_logging
from src.core.security import setup_cors
from src.core.settings import settings
from src.events.lifespan import lifespan

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="autogen-backend",
    description="autogen-backend",
    version="1.0.0",
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(router)

logger.info(f"Loaded application settings: {settings.model_dump()}")
