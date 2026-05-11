"""Схемы регистрации и ответа с токеном."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Тело регистрации пользователя."""

    email: EmailStr = Field(description="Электронная почта пользователя.")
    password: str = Field(
        min_length=8,
        max_length=512,
        description="Пароль (минимум 8 символов).",
    )


class TokenResponse(BaseModel):
    """Ответ с JWT для OAuth2 Bearer."""

    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {"access_token": "<jwt>", "token_type": "bearer"}
        }
    }
