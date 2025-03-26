from sqlalchemy import create_engine

from alembic import context
from src.core.settings import settings  # Assuming settings holds your DB config
from models.run_model import Run

# Target metadata from your models
target_metadata = Run.metadata

# Create a sync engine for migrations
sync_engine = create_engine(settings.DATABASE.postgres_url)


def run_migrations_online():
    with sync_engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline():
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
