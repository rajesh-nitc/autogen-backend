from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, func
from sqlmodel import Column, Field, SQLModel


class Run(SQLModel, table=True):
    """Represents a single execution run.

    User sends a message -> handle_chat() processes the message -> Returns a response.
    """

    id: int | None = Field(
        default=None,
        description="Unique identifier for the run",
        sa_column=Column(Integer, primary_key=True, autoincrement=True),
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Time when the run was created",
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    session_id: str | None = Field(
        default=None,
        description="Session ID sent by the client",
        sa_column=Column(String, nullable=True),
    )
    user_id: str | None = Field(
        default=None,
        description="User ID",
        sa_column=Column(String, nullable=True),
    )
    task: dict | None = Field(
        default_factory=dict,
        description="User task",
        sa_column=Column(JSON, nullable=True),
    )
    task_result: dict | None = Field(
        default_factory=dict,
        description="User task result",
        sa_column=Column(JSON, nullable=True),
    )
    team_state: dict | None = Field(
        default_factory=dict,
        description="Team state",
        sa_column=Column(JSON, nullable=True),
    )
    messages: list[dict] | None = Field(
        default_factory=list,
        description="Messages generated",
        sa_column=Column(JSON, nullable=True),
    )
    error: dict | None = Field(
        default_factory=dict,
        description="Error message",
        sa_column=Column(JSON, nullable=True),
    )
