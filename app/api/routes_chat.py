"""
Эндпоинты диалога с LLM и истории сообщений.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.schemas.chat import ChatHistoryItem, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])

UserIdDep = Annotated[int, Depends(get_current_user_id)]


@router.post("", response_model=ChatResponse)
async def chat_ask(
    body: ChatRequest,
    uid: UserIdDep,
    chat: Annotated[ChatUseCase, Depends(get_chat_usecase)],
) -> ChatResponse:
    """Запрос к модели с учётом системной инструкции и истории."""

    answer = await chat.ask(
        user_id=uid,
        prompt=body.prompt,
        system=body.system,
        max_history=body.max_history,
        temperature=body.temperature,
    )
    return ChatResponse(answer=answer)


@router.get("/history", response_model=list[ChatHistoryItem])
async def chat_history(
    uid: UserIdDep,
    chat: Annotated[ChatUseCase, Depends(get_chat_usecase)],
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> list[ChatHistoryItem]:
    """Последние сообщения пользователя в хронологическом порядке."""

    rows = await chat.get_history(uid, limit)
    return [ChatHistoryItem.model_validate(r) for r in rows]


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def chat_clear(
    uid: UserIdDep,
    chat: Annotated[ChatUseCase, Depends(get_chat_usecase)],
) -> Response:
    """Удаляет историю сообщений текущего пользователя."""

    await chat.clear_history(uid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
