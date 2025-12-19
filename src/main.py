from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.logging.logging import get_logger
from src.core.settings.settings import settings
from src.core.middlewares.profile import add_profile_middleware
from src.core.middlewares.http import add_log_request_middleware, add_security_headers_middleware
from src.routers.http.v1.api import APIV1Router
from src.routers.http.v1.error_handler import add_exception_handlers_v1

# __version__ = version("bot-api")

logger = get_logger(settings.API_TITLE)
logger.info("Starting application")


app = FastAPI(
    title=settings.API_TITLE,
    prefix=settings.API_PREFIX,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    # version=__version__
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=APIV1Router, prefix=settings.API_PREFIX)


add_exception_handlers_v1(app=app)

if settings.PROFILING_ENABLED is True:
    add_profile_middleware(app=app)

if settings.USE_SECURE_COOKIES is True:
    add_security_headers_middleware(app=app)

add_log_request_middleware(app=app)

@app.get("/api/healthcheck")
async def healthcheck():
    return {"status": "ok"}
