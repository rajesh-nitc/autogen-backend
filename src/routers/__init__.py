"""Initializes the FastAPI router."""

from fastapi import APIRouter

from src.routers import chat, health

router = APIRouter()

router.include_router(chat.router, prefix="/ws", tags=["chat"])
router.include_router(health.router, prefix="/api", tags=["health"])
