import logging

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.settings import settings

logger = logging.getLogger(__name__)


class DBConnectionManager:
    """Singleton class to manage database connections."""

    _instance = None

    def __new__(cls):  # noqa: B008,ANN204
        """Create a new instance of the class if it does not exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self) -> None:
        """Initialize the database engine."""
        self._engine = create_async_engine(settings.DATABASE.postgres_url, echo=False)
        self.async_session_maker = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    @property
    def engine(self):  # noqa: ANN201
        """Return the database engine."""
        if self._engine is None:
            raise RuntimeError("DB engine not initialized.")  # noqa: TRY003
        return self._engine


class WebsocketConnectionManager:
    """Singleton class to manage WebSocket connections."""

    async def connect(self, session_id: str, websocket: WebSocket) -> None:
        """Register a new WebSocket connection."""
        await websocket.accept()
        logger.info(f"WebSocket connected for session: {session_id}")

    async def disconnect(self, session_id: str) -> None:
        """Handle WebSocket disconnection."""
        logger.info(f"WebSocket disconnected for session: {session_id}")


# Create singletons
db_manager = DBConnectionManager()
ws_manager = WebsocketConnectionManager()
