from pydantic import BaseModel

class DomainUser(BaseModel):
    id: int
    telegram_user_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    timezone: str
    locale: str


class TelegramAuthData(BaseModel):
    telegram_user_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    raw_user: dict[str, any]
    auth_date: int
    query_id: str | None


class LoginViaTelegramResult(BaseModel):
    user: DomainUser
    is_new: bool
