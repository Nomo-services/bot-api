from src.core.security.security import verify_password
from src.di.unit_of_work import AbstractUnitOfWork
from src.errors.auth import IncorrectSigninError
from src.models.auth import AuthModel


async def authenticate(
    async_unit_of_work: AbstractUnitOfWork, data: AuthModel
) -> AuthModel:
    async with async_unit_of_work as auow:
        user: AuthModel = await auow.auth_repo.get_by_telegram_id(
            telegram_id=data.telegram_id
        )
        if user is None:
            raise IncorrectSigninError()

        if not await verify_password(data.password_hash, user.password_hash):
            raise IncorrectSigninError()

    return user
