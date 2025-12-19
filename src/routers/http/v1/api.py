from fastapi import APIRouter

from .auth.router import AuthRouter

from src.usecases.auth.auth import AuthUseCase

APIV1Router = APIRouter(prefix="/v1")
auth_ucase = AuthUseCase()


APIV1Router.include_router(
    router=AuthRouter,
)