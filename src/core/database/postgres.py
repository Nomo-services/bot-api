from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from src.core.logging.logging import get_logger
from src.core.settings.settings import settings


logger = get_logger("Database")
logger.info(
    "Creating AsyncPostgreSQLEngine",
    extra={
        "database_name": str(settings.DATABASE_NAME),
        "echo": settings.SQLALCHEMY_ECHO,
        "isolation_level": settings.SQLALCHEMY_ISOLATION_LEVEL,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.MAX_OVERFLOW,
    },
)

AsyncPostgreSQLEngine = create_async_engine(
    url=str(settings.ASYNC_DATABASE_URI),
    echo=settings.SQLALCHEMY_ECHO,
    isolation_level=settings.SQLALCHEMY_ISOLATION_LEVEL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)

AsyncPostgreSQLScopedSession = async_scoped_session(
    async_sessionmaker(
        AsyncPostgreSQLEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)


def get_async_postgresql_session() -> AsyncSession:
    return AsyncPostgreSQLScopedSession()


async def async_postgresql_session_context_manager() -> AsyncGenerator[
    AsyncSession, None
]:
    async with AsyncPostgreSQLScopedSession() as session:
        yield session
