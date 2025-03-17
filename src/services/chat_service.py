import json
import logging

import aiofiles
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from fastapi import WebSocket

from src.teams.single_agent_team import get_single_agent_team
from src.utils.team_history import get_history

logger = logging.getLogger(__name__)

state_path = "team_state.json"
history_path = "team_history.json"


async def handle_chat(websocket: WebSocket, request: TextMessage) -> None:
    """Handle chat messages.

    :param websocket: WebSocket
    :param request: TextMessage
    """
    try:
        team = await get_single_agent_team()
        history = await get_history()
        stream = team.run_stream(task=request)

        async for message in stream:
            if isinstance(message, TaskResult):
                logger.info(message)
                await websocket.send_json(message.messages[-1].model_dump())
                continue
            else:
                # Uncomment below to send intermediate messages
                # await websocket.send_json(message.model_dump())
                history.append(message.model_dump())

        # Save team state to file
        async with aiofiles.open(state_path, "w") as file:
            state = await team.save_state()
            await file.write(json.dumps(state))

        # Save chat history to file
        async with aiofiles.open(history_path, "w") as file:
            await file.write(json.dumps(history))

    except Exception as e:
        # Send error message to client
        error_message = {
            "type": "error",
            "content": f"Error: {str(e)}",
            "source": "system",
        }
        logger.exception("Error handling chat message")
        await websocket.send_json(error_message)
