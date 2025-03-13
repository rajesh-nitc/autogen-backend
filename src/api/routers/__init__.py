from fastapi import APIRouter

from src.api.routers import chat, health

router = APIRouter()

router.include_router(chat.router, prefix="/ws", tags=["chat"])
router.include_router(health.router, prefix="/api", tags=["health"])
