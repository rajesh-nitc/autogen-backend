from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, func
from sqlmodel import Column, Field, SQLModel


class Run(SQLModel, table=True):
    """Represents a single execution run i.e.

    User sends a message -> handle_chat() processes the message -> Returns a response.
    """

    id: int | None = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),  # type: ignore
    )

    # Store session_id
    session_id: str | None = Field(
        default=None,
        sa_column=Column(String, nullable=True),  # type: ignore
    )

    # Store user task
    task: dict | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),  # type: ignore
    )

    # Store TaskResult
    task_result: dict | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),  # type: ignore
    )

    # Team state
    team_state: dict | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),  # type: ignore
    )

    # Store messages
    messages: list[dict] | None = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=True),  # type: ignore
    )

    # User ID
    user_id: str | None = Field(
        default=None,
        sa_column=Column(String, nullable=True),  # type: ignore
    )
