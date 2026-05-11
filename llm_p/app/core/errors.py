"""
Доменные исключения приложения без зависимости от FastAPI.
"""


class AppError(Exception):
    """Базовая ошибка сценария; обрабатывается HTTP-слоем."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ConflictError(AppError):
    """Конфликт данных (например, email уже занят)."""


class UnauthorizedError(AppError):
    """Невозможность аутентифицировать клиента."""

    LOGIN_MESSAGE = (
        "Неверный адрес почты или пароль"
    )

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.LOGIN_MESSAGE)


class ForbiddenError(AppError):
    """Доступ к ресурсу запрещён."""


class NotFoundError(AppError):
    """Сущность не найдена."""


class ExternalServiceError(AppError):
    """Ошибка внешнего провайдера (например, OpenRouter)."""

    def __init__(
        self,
        message: str,
        *,
        ref_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.ref_id = ref_id
