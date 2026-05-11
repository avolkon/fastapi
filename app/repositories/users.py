"""
Доступ к таблице пользователей (только ORM, без JWT и без хеширования).
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    """Репозиторий учётных записей."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """Возвращает пользователя по email или None."""

        stmt = select(User).where(User.email == email)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Возвращает пользователя по id или None."""

        return await self._session.get(User, user_id)

    async def create(self, email: str, password_hash: str, role: str) -> User:
        """
        Создаёт пользователя, фиксирует изменения и обновляет объект.

        При нарушении уникальности email выбросит ошибку от движка БД —
        её классифицирует слой сценария.
        """

        user = User(email=email, password_hash=password_hash, role=role)
        self._session.add(user)
        await self._session.flush()
        await self._session.commit()
        await self._session.refresh(user)
        return user
