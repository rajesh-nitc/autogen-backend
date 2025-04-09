import logging

from autogen_agentchat.messages import TextMessage
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import attributes

from src.core.settings import settings
from src.models.run_model import Run

logger = logging.getLogger(__name__)


class RunService:
    """Service to interact with the DB Run model."""

    def __init__(self, db_session: AsyncSession):  # noqa: ANN204
        """Initialize the service."""
        self.db_session = db_session
        self.reset_state_at_nth_run = settings.RUN.RESET_STATE_AT_NTH_RUN

    async def create_new_run(
        self,
        session_id: str,
        user_id: str,
        request: TextMessage,
    ) -> Run:
        """Create a new run."""
        # Check the number of runs for the user
        run_count = await self.get_run_count(user_id)

        # Reset team_state if the threshold is reached
        if run_count % self.reset_state_at_nth_run == 0:
            team_state = {}
        else:
            # Retrieve team_state from the previous run
            team_state = await self.get_team_state_from_previous_run(user_id)

        new_run = Run(
            session_id=session_id,
            task=request.model_dump(),
            messages=[],
            task_result={},
            team_state=team_state,
            user_id=user_id,
            error={},
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
            select(Run.team_state).where(Run.user_id == user_id).order_by(Run.created_at.desc()).limit(1)
        )
        team_state = result.scalars().first() or {}
        return team_state

    async def update_new_run_with_error(self, run: Run, error: dict) -> None:
        """Update new run with error message."""
        run.error = error
        self.db_session.add(run)
        await self.db_session.commit()

    async def get_run_count(self, user_id: str) -> int:
        """Get the total number of runs for a user."""
        result = await self.db_session.execute(select(func.count()).select_from(Run).where(Run.user_id == user_id))
        return result.scalar() or 0
