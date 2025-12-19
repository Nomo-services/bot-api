from urllib.parse import urlparse

from src.core.settings.settings import settings

IS_RELATIONAL_DB = False

DATABASE_TYPE, _, _ = urlparse(str(settings.ASYNC_DATABASE_URI)).scheme.partition("+")

if DATABASE_TYPE == "postgresql":
    from .postgres import AsyncPostgreSQLEngine as AsyncRelationalDBEngine  # noqa: F401
    from .postgres import AsyncPostgreSQLScopedSession as AsyncScopedSession  # noqa: F401
    from .postgres import get_async_postgresql_session as get_async_session  # noqa: F401

    IS_RELATIONAL_DB = True

else:
    raise RuntimeError(
        f"Invalid database type '{DATABASE_TYPE}' provided in DATABASE_URI: {settings.ASYNC_DATABASE_URI}"
    )
