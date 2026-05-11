"""
Зависимости FastAPI: сессия БД, репозитории, JWT и клиент провайдера.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_db_session
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_user_repository(session: SessionDep) -> UserRepository:
    """Фабрика репозитория пользователей на запрос."""

    return UserRepository(session)


async def get_chat_repository(session: SessionDep) -> ChatMessageRepository:
    """Фабрика репозитория сообщений на запрос."""

    return ChatMessageRepository(session)


def get_llm_client() -> OpenRouterClient:
    """Единственный параметризованный клиент провайдера на процесс."""

    return OpenRouterClient(settings)


async def get_auth_usecase(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthUseCase:
    """Сценарий учётной записи на запрос."""

    return AuthUseCase(repo)


async def get_chat_usecase(
    repo: Annotated[ChatMessageRepository, Depends(get_chat_repository)],
    llm: Annotated[OpenRouterClient, Depends(get_llm_client)],
) -> ChatUseCase:
    """Сценарий чата на запрос."""

    return ChatUseCase(repo, llm)


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> int:
    """
    Читает sub из JWT; при ошибке отдаёт 401 в стиле OAuth2.

    Не логирует сам токен.
    """

    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise ValueError("нет sub в токене")
        return int(sub)
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
