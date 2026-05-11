"""Публичное представление пользователя без секретных полей."""

from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """Данные учётной записи, безопасные для ответа API."""

    id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
