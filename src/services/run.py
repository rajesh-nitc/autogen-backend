import logging

from autogen_agentchat.messages import TextMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import attributes

from src.models.run import Run

logger = logging.getLogger(__name__)


class RunService:
    """Service to interact with the DB Run model."""

    def __init__(self, db_session: AsyncSession):  # noqa: ANN204
        """Initialize the service."""
        self.db_session = db_session

    async def create_new_run(
        self, session_id: str, user_id: str, request: TextMessage
    ) -> Run:
        """Create a new run."""
        new_run = Run(
            session_id=session_id,
            task=request.model_dump(),
            messages=[],
            task_result={},
            team_state={},
            user_id=user_id,
        )
        self.db_session.add(new_run)
        await self.db_session.commit()
        return new_run

    async def update_new_run_with_result(self, run: Run, result: dict) -> None:
        """Update new run with result."""
        run.task_result = result
        await self.db_session.commit()

    async def update_new_run_with_message(self, run: Run, message: dict) -> None:
        """Update new run with message."""
        attributes.flag_modified(run, "messages")
        run.messages.append(message)
        await self.db_session.commit()

    async def update_new_run_with_team_state(self, run: Run, team_state: dict) -> None:
        """Update new run with team state."""
        run.team_state = team_state
        await self.db_session.commit()

    async def get_team_state_from_previous_run(self, user_id: str) -> dict:
        """Get team state from the previous run."""
        result = await self.db_session.execute(
            select(Run.team_state)
            .where(Run.user_id == user_id)
            .order_by(Run.id.desc())
            .offset(1)
            .limit(1)
        )
        team_state = result.scalars().first() or {}
        return team_state

    async def update_new_run_with_error(self, run: Run, error: str) -> None:
        """Update new run with error message."""
        run.error = error
        await self.db_session.commit()
