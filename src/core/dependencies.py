from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.connection import db_manager

async_session_factory = sessionmaker(
    db_manager.engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_db_session():  # noqa: ANN201
    """Get a database session."""
    async with async_session_factory() as session:
        yield session


async def get_user_id() -> str:
    """Get the user ID."""
    return "rajesh-nitc"
