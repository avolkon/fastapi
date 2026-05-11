"""Схемы запроса к LLM и ответа истории сообщений."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """Текущий промпт пользователя и параметры вызова модели."""

    prompt: str = Field(max_length=32_768)
    system: str | None = Field(None, max_length=16_384)
    max_history: int = Field(default=16, ge=0, le=500)
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    """Ответ ассистента."""

    answer: str


class ChatHistoryItem(BaseModel):
    """Одна запись сохранённого диалога."""

    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
