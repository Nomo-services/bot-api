import abc
from typing import Any
from uuid import UUID

from src.entities.user import User


class AbstractAuthRepository(abc.ABC):
    session: Any

    @abc.abstractmethod
    async def get_by_id(self, id: UUID) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_telegram_id(self, telegram_id: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_master_id_by_telegram_id(self, telegram_id: str) -> UUID | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_client_id_by_telegram_id(self, telegram_id: str) -> UUID | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, data: User, user_role: str) -> None:
        raise NotImplementedError
