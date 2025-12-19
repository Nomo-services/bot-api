import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from logging.config import fileConfig

from src.core.settings.settings import settings
from src.core.database.base import Base
from src.core.logging.logging import get_logger

# target_metadata = Base.metadata

logger = get_logger(settings.API_TITLE)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = settings.ASYNC_DATABASE_URI
    connectable = create_async_engine(url=str(url), echo=True, future=True)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    logger.info("Can't run migrations offline")
else:
    asyncio.run(run_migrations_online())
