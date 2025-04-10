import logging

from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.run_service import RunService
from src.teams.selector_group_chat import get_team

logger = logging.getLogger(__name__)


async def handle_task(
    session_id: str,
    websocket: WebSocket,
    request: TextMessage,
    user_id: str,
    db_session: AsyncSession,
) -> None:
    """Handle tasks from the client."""
    try:
        run_service = RunService(db_session)

        # Create new run
        new_run = await run_service.create_new_run(session_id, user_id, request)
        team = await get_team()

        # Load team state from previous run if available
        if new_run.team_state:
            await team.load_state(new_run.team_state)

        stream = team.run_stream(task=request)
        async for message in stream:
            if isinstance(message, TaskResult):
                if message.stop_reason is None:
                    continue

                # Update new run with task result
                await run_service.update_new_run_with_result(new_run, message.messages[-1].model_dump())

                # Send task result to client
                await websocket.send_json(message.messages[-1].model_dump())
                continue
            else:
                # Update new run with message including intermediary message
                await run_service.update_new_run_with_message(new_run, message.model_dump())

        # Update new run with team state
        await run_service.update_new_run_with_team_state(new_run, await team.save_state())

    except Exception as e:
        error_message = {
            "type": "error",
            "content": f"Error: {str(e)}",
            "source": "system",
        }
        logger.exception("Error handling task.")

        # Update new run with error message
        await run_service.update_new_run_with_error(new_run, error_message)

        # Send error message to client
        await websocket.send_json(error_message)
