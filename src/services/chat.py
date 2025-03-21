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

    # Create new run with session ID, user ID and user request
    new_run = await run_service.create_new_run(session_id, user_id, request)

    # Get team state from the previous run
    team_state = await run_service.get_team_state_from_previous_run(user_id)

    try:
        team = await get_single_agent_team()
        await team.load_state(team_state)
        stream = team.run_stream(task=request)

        async for message in stream:
            if isinstance(message, TaskResult):
                if message.stop_reason is None:
                    continue

                # Update new run with task result
                await run_service.update_new_run_with_result(
                    new_run, message.messages[-1].model_dump()
                )

                # Send task result to client
                await websocket.send_json(message.messages[-1].model_dump())
                continue
            else:
                # Update new run with message including intermediary message
                await run_service.update_new_run_with_message(
                    new_run, message.model_dump()
                )

        team_state = await team.save_state()

        # Update new run with team state
        await run_service.update_new_run_with_team_state(new_run, team_state)

    except Exception as e:
        error_message = {
            "type": "error",
            "content": f"Error: {str(e)}",
            "source": "system",
        }
        logger.exception("Error handling chat message in services.chat")

        # Update new run with error message
        await run_service.update_new_run_with_error(new_run, error_message)

        # Send error message to client
        await websocket.send_json(error_message)
