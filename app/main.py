"""
Сборка приложения FastAPI: роуты, CORS, DDL и обработка доменных ошибок.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import routes_auth, routes_chat
from app.core.config import settings
from app.core.errors import (
    AppError,
    ConflictError,
    ExternalServiceError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)
from app.db import models  # noqa: F401 — регистрация ORM-моделей
from app.db.base import Base
from app.db.session import engine


def _http_code_for(exc: AppError) -> int:
    """Подбирает HTTP-код по типу исключения (без падения приложения)."""

    if isinstance(exc, ConflictError):
        return 409
    if isinstance(exc, UnauthorizedError):
        return 401
    if isinstance(exc, ForbiddenError):
        return 403
    if isinstance(exc, NotFoundError):
        return 404
    if isinstance(exc, ExternalServiceError):
        return 502
    return 500


def create_app() -> FastAPI:
    """
    Конфигурирует FastAPI без бизнес-логики внутри маршрутов.

    Таблицы создаются на старте через async DDL (run_sync create_all).
    """

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    origins = settings.cors_origins_list()
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.exception_handler(AppError)
    async def domain_handler(_request: Request, exc: AppError) -> JSONResponse:
        """Переводит доменные исключения в JSON с предсказуемым кодом."""

        headers = {}
        status_code = _http_code_for(exc)
        if isinstance(exc, UnauthorizedError):
            headers["WWW-Authenticate"] = "Bearer"
        payload = {"detail": exc.message}
        if isinstance(exc, ExternalServiceError) and exc.ref_id:
            payload["ref_id"] = exc.ref_id
        return JSONResponse(
            status_code=status_code,
            content=payload,
            headers=headers,
        )

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Лёгкий эндпоинт статуса для балансировщиков и разработчиков."""

        return {"status": "ok", "env": settings.env}

    app.include_router(routes_auth.router)
    app.include_router(routes_chat.router)

    return app


app = create_app()
