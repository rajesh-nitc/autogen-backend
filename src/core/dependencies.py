from src.core.connection import db_manager


async def get_db():  # noqa: ANN201
    """Test."""
    async with db_manager.get_session() as session:
        yield session


async def get_user_id() -> str:
    """Test."""
    return "rajesh-nitc"
