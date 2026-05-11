"""
HTTP-клиент OpenRouter для chat/completions.
"""

from __future__ import annotations

import uuid
from typing import Any

import httpx

from app.core.config import Settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """
    Изолированный асинхронный клиент: без БД и без user_id в контракте.

    Ошибки сети и ответов провайдера переводятся в ExternalServiceError
    без утечки токена в текст для клиента.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._base = settings.openrouter_base_url.rstrip("/")
        self._timeout = httpx.Timeout(60.0)

    def _headers(self) -> dict[str, str]:
        """Собирает заголовки по ТЗ: Bearer, Referer, X-Title."""

        return {
            "Authorization": f"Bearer {self._settings.openrouter_api_key}",
            "Referer": self._settings.openrouter_site_url,
            "X-Title": self._settings.openrouter_app_name,
            "Content-Type": "application/json",
        }

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float,
        request_id: str | None = None,
    ) -> str:
        """
        Вызывает POST /chat/completions и возвращает текст ответа ассистента.

        При 4xx/5xx или неверном JSON выбрасывает ExternalServiceError.
        """

        rid = request_id or str(uuid.uuid4())
        payload: dict[str, Any] = {
            "model": self._settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.post(
                    f"{self._base}/chat/completions",
                    headers=self._headers(),
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as exc:
                msg = (
                    f"Ответ провайдера недоступен (код {exc.response.status_code})"
                )
                raise ExternalServiceError(msg, ref_id=rid) from None
            except (httpx.RequestError, ValueError) as exc:
                raise ExternalServiceError(
                    (
                        "Сеть или разбор ответа провайдера: "
                        f"{type(exc).__name__}"
                    ),
                    ref_id=rid,
                ) from None

        try:
            return str(data["choices"][0]["message"]["content"]).strip()
        except (KeyError, IndexError, TypeError):
            raise ExternalServiceError(
                "Неверный формат ответа LLM-провайдера",
                ref_id=rid,
            ) from None
