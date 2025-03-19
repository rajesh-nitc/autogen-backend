import logging

from autogen_agentchat.messages import TextMessage
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.connection import ws_manager
from src.core.dependencies import get_db, get_user_id
from src.services.chat import handle_chat

router: APIRouter = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/chat/{session_id}")
async def get_chat_response(
    session_id: str,
    websocket: WebSocket,
    db_session: AsyncSession = Depends(get_db),  # noqa: B008
    user_id: str = Depends(get_user_id),  # noqa: B008
) -> None:
    """WebSocket endpoint for chat."""
    await ws_manager.connect(session_id, websocket)

    try:
        while True:
            try:
                data = await websocket.receive_json()
                request = TextMessage.model_validate(data)
                await handle_chat(session_id, websocket, request, db_session, user_id)

            except Exception as e:
                logger.exception("Error handling request")
                await websocket.send_json(
                    {
                        "type": "error",
                        "content": f"Unexpected error: {str(e)}",
                        "source": "system",
                    }
                )

    except WebSocketDisconnect:
        await ws_manager.disconnect(session_id)
