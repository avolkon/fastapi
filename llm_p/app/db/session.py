"""
Асинхронный движок SQLite и фабрика сессий.
"""

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

_app_root = Path(__file__).resolve().parent.parent.parent

if settings.sqlite_path.startswith("sqlite+"):
    _engine_url = settings.sqlite_path
else:
    _db_path = Path(settings.sqlite_path)
    if not _db_path.is_absolute():
        _db_path = (_app_root / _db_path).resolve()
    _engine_url = f"sqlite+aiosqlite:///{_db_path.as_posix()}"

engine = create_async_engine(_engine_url, echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Выдаёт сессию БД для FastAPI Depends.

    Транзакции фиксируются в репозиториях и сценариях, где это нужно.
    """

    async with AsyncSessionLocal() as session:
        yield session
