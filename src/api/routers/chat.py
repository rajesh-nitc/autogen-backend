import logging

from autogen_agentchat.messages import TextMessage
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.services.chat_service import handle_chat

router: APIRouter = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/chat")
async def get_chat_response(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            request = TextMessage.model_validate(data)
            await handle_chat(websocket, request)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        try:
            await websocket.send_json(
                {
                    "type": "error",
                    "content": f"Unexpected error: {str(e)}",
                    "source": "system",
                }
            )
        except Exception:
            pass
