"""
Доступ к истории сообщений чата пользователя.
"""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    """Репозиторий сообщений: добавление, выборка, полная очистка."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        """Сохраняет одно сообщение и фиксирует транзакцию."""

        row = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(row)
        await self._session.commit()

    async def get_last_n(self, user_id: int, n: int) -> list[ChatMessage]:
        """
        Возвращает до n последних сообщений в хронологическом порядке (старые раньше).
        """

        if n <= 0:
            return []
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(n)
        )
        res = await self._session.execute(stmt)
        rows = list(res.scalars().all())
        rows.reverse()
        return rows

    async def delete_all(self, user_id: int) -> None:
        """Удаляет всю историю пользователя."""

        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
