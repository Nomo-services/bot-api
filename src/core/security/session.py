from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from fastapi import Request, Response
import jwt
from pydantic import BaseModel
from src.core.settings.settings import settings
from src.di.unit_of_work import AbstractUnitOfWork
from src.di.dependency_injection import injector
from src.errors.session import (
    DecodeSessionTokenError,
    InvalidSessionPayloadError,
    MalformedSessionTokenError,
    SessionExpiredError,
    SessionNotFoundError,
)


SESSION_COOKIE_NAME = "Host-session-token"
USER_INFO_COOKIE_NAME = "Host-user-info"
SESSION_PREFIX = "sess:"


class SessionPayload(BaseModel):
    session_id: str
    user_id: str
    user_role: str
    user_role_id: str
    expires: str


class SessionAdapter:
    _auow: AbstractUnitOfWork | None = None

    @property
    def async_unit_of_work(self) -> AbstractUnitOfWork:
        if self._auow is None:
            self._auow = injector.get(AbstractUnitOfWork)
        return self._auow

    def __init__(
        self,
        *,
        algorithm: str = "HS256",
    ):
        self._secret = settings.SESSION_SECRET_KEY
        self._algo = algorithm

    async def create_session(
        self,
        response: Response,
        user_id: UUID,
        user_role: str,
        user_role_id: UUID,
        lifetime: timedelta,
    ) -> None:
        lifetime = lifetime or timedelta(minutes=settings.SESSION_EXPIRE_MINUTES)
        session_id = str(uuid4())
        expires_at = datetime.now(timezone.utc) + lifetime
        payload = SessionPayload(
            session_id=session_id,
            user_id=str(user_id),
            user_role=user_role,
            user_role_id=str(user_role_id),
            expires=expires_at.isoformat(),
        )
        session_token = jwt.encode(payload.model_dump(), self._secret, algorithm=self._algo).decode("utf-8")
        async with self.async_unit_of_work as auow:
            await auow.kv_store_repo.create(key=f"{SESSION_PREFIX}{session_id}", value=session_token)

        max_age = int(lifetime.total_seconds())
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_token,
            httponly=True,
            secure=settings.USE_SECURE_COOKIES,
            samesite="lax",
            max_age=max_age,
            expires=max_age,
            path="/",
        )
        user_info = jwt.encode(
            {"user_id":str(user_id), "user_role":user_role, "user_role_id":str(user_role_id)}, 
            self._secret,
            algorithm=self._algo
        ).decode("utf-8")

        response.set_cookie(
            key=USER_INFO_COOKIE_NAME,
            value=user_info,
            httponly=False,
            secure=False,
            samesite="lax",
            max_age=max_age,
            expires=max_age,
            path="/",
        )

    async def get_session(
        self,
        request: Request,
    ) -> SessionPayload:
        session_token = request.cookies.get(SESSION_COOKIE_NAME)
        if not session_token:
            raise SessionNotFoundError()
        try:
            data = jwt.decode(session_token, self._secret, algorithms=[self._algo])
            session_id = data.get("session_id")
        except jwt.ExpiredSignatureError as e:
            async with self.async_unit_of_work as auow:
                await auow.kv_store_repo.delete(key=f"{SESSION_PREFIX}{session_id}")
            raise SessionExpiredError() from e
        except jwt.PyJWTError as e:
            raise MalformedSessionTokenError() from e

        async with self.async_unit_of_work as auow:
            record = await auow.kv_store_repo.get(key=f"{SESSION_PREFIX}{session_id}")

        if not record:
            raise SessionNotFoundError()
        if record.value != session_token:
            raise InvalidSessionPayloadError()

        expires_str = data.get("expires")
        try:
            expires_at = datetime.fromisoformat(expires_str)
        except Exception as e:
            raise InvalidSessionPayloadError() from e

        return SessionPayload(
            session_id=session_id,
            user_id=data.get("user_id"),
            user_role=data.get("user_role"),
            user_role_id=data.get("user_role_id"),
            expires=expires_at.isoformat(),
        )

    async def delete_session(
        self,
        request: Request,
        response: Response | None = None,
    ) -> None:
        session_token = request.cookies.get(SESSION_COOKIE_NAME)
        if not session_token:
            return None
        try:
            data = jwt.decode(session_token, self._secret, algorithms=[self._algo], options={"verify_exp": False})
            session_id = UUID(data.get("session_id"))
        except jwt.PyJWTError as e:
            raise DecodeSessionTokenError() from e

        async with self.async_unit_of_work as auow:
            await auow.kv_store_repo.delete(key=f"{SESSION_PREFIX}{session_id}")

        if response is not None:
            response.delete_cookie(
                key=SESSION_COOKIE_NAME,
                path="/",
            )
            response.delete_cookie(
                key=USER_INFO_COOKIE_NAME,
                path="/",
            )
