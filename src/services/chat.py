import logging

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.run import RunService
from src.teams.single_agent import get_single_agent_team

logger = logging.getLogger(__name__)


async def handle_chat(
    session_id: str,
    websocket: WebSocket,
    request: TextMessage,
    db_session: AsyncSession,
    user_id: str,
) -> None:
    """Handle chat messages."""
    run_service = RunService(db_session)
    new_run = await run_service.create_new_run(session_id, user_id, request)
    team_state = await run_service.get_team_state(user_id)

    try:
        team = await get_single_agent_team()
        await team.load_state(team_state)
        stream = team.run_stream(task=request)

        async for message in stream:
            if isinstance(message, TaskResult):
                if message.stop_reason is None:
                    continue
                await run_service.update_run_with_result(
                    new_run, message.messages[-1].model_dump()
                )
                await websocket.send_json(message.messages[-1].model_dump())
                continue
            else:
                await run_service.update_run_with_message(new_run, message.model_dump())

        # Save team state
        team_state = await team.save_state()
        await run_service.update_run_with_team_state(new_run, team_state)  # type: ignore

    except Exception as e:
        # Send error message to client
        error_message = {
            "type": "error",
            "content": f"Error: {str(e)}",
            "source": "system",
        }
        logger.exception("Error handling chat message")
        await websocket.send_json(error_message)
