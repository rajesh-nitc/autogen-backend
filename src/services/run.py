import logging

from autogen_agentchat.messages import TextMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import attributes

from src.models.run import Run

logger = logging.getLogger(__name__)


class RunService:
    """Test."""

    def __init__(self, db_session: AsyncSession):  # noqa: ANN204
        """Test."""
        self.db_session = db_session

    async def create_new_run(
        self, session_id: str, user_id: str, request: TextMessage
    ) -> Run:
        """Test."""
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

    async def update_run_with_result(self, run: Run, result: dict) -> None:
        """Update run with final task result."""
        run.task_result = result
        await self.db_session.commit()

    async def update_run_with_message(self, run: Run, message: dict) -> None:
        """Append new message to the run's messages."""
        attributes.flag_modified(run, "messages")
        run.messages.append(message)  # type: ignore
        await self.db_session.commit()

    async def update_run_with_team_state(self, run: Run, team_state: dict) -> None:
        """Save team state."""
        run.team_state = team_state
        await self.db_session.commit()

    async def get_team_state(self, user_id: str) -> dict:
        """Fetch the team state from the most recent run for a user."""
        result = await self.db_session.execute(
            select(Run.team_state)  # type: ignore
            .where(Run.user_id == user_id)
            .order_by(Run.id.desc())  # type: ignore
            .offset(1)
            .limit(1)
        )

        team_state = result.scalars().first() or {}
        return team_state
