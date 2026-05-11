"""
Сценарии работы чата и историей сообщений пользователя.
"""

from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """Собирает контекст диалога, вызывает LLM и сохраняет сообщения."""

    def __init__(
        self,
        messages: ChatMessageRepository,
        llm: OpenRouterClient,
    ) -> None:
        self._messages = messages
        self._llm = llm

    async def ask(
        self,
        *,
        user_id: int,
        prompt: str,
        system: str | None,
        max_history: int,
        temperature: float,
    ) -> str:
        """
        Формирует messages для провайдера, сохраняет user-текущий ход ответ модели.

        При сбое LLM после сохранения user-сообщения данные уже в БД — это ожидаемо.
        """

        history = await self._messages.get_last_n(user_id, max_history)
        body: list[dict[str, str]] = []
        if system:
            body.append({"role": "system", "content": system})
        for row in history:
            body.append({"role": row.role, "content": row.content})
        body.append({"role": "user", "content": prompt})

        await self._messages.add_message(user_id, "user", prompt)
        answer = await self._llm.chat_completion(body, temperature=temperature)
        await self._messages.add_message(user_id, "assistant", answer)
        return answer

    async def get_history(self, user_id: int, limit: int) -> list[ChatMessage]:
        """Возвращает последние limit сообщений в порядке «старый → новый»."""

        if limit <= 0:
            return []
        return await self._messages.get_last_n(user_id, limit)

    async def clear_history(self, user_id: int) -> None:
        """Полная очистка истории пользователя."""

        await self._messages.delete_all(user_id)
