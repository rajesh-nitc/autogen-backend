from contextlib import asynccontextmanager

from src.core.connection import db_manager

async_session_factory = db_manager.async_session_maker


@asynccontextmanager
async def get_db_session():  # noqa: ANN201
    """Get a database session."""
    async with async_session_factory() as session:
        yield session


async def get_user_id() -> str:
    """Get the user ID."""
    return "rajesh-nitc"
