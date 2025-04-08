from src.core.connection import db_manager

async_session_factory = db_manager.async_session_maker


async def get_db_session():  # noqa: ANN201
    """Get the database session."""
    async with db_manager.get_session() as session:
        yield session


# Temporary function to get user ID
async def get_user_id() -> str:
    """Get the user ID."""
    return "rajesh-nitc"
