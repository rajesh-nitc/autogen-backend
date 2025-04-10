import json
import logging

from autogen_agentchat.messages import TextMessage
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.connection import ws_manager
from src.core.dependencies import get_db_session, get_user_id
from src.services.chat_service import handle_task

router: APIRouter = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/chat/{session_id}")
async def get_task_result(
    session_id: str,
    websocket: WebSocket,
    user_id: str = Depends(get_user_id),  # noqa: B008
    db_session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> None:
    """WebSocket endpoint for chat."""
    await ws_manager.connect(session_id, websocket)

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except json.JSONDecodeError:
                logger.warning("Invalid input: expected valid JSON.")
                await websocket.send_json(
                    {
                        "type": "error",
                        "content": "Invalid input: expected valid JSON.",
                        "source": "system",
                    }
                )
                continue

            try:
                request = TextMessage.model_validate(data)
                await handle_task(session_id, websocket, request, user_id, db_session)
            except WebSocketDisconnect as e:
                logger.info(f"WebSocket disconnected Inner: {str(e)}")
                break

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket disconnected Outer: {str(e)}")
        await ws_manager.disconnect(session_id)
    except Exception:
        logger.exception("Unexpected error in WebSocket handling")
