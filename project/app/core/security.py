"""
Утилиты безопасности: хеш пароля и JWT.

Модуль не обращается к БД и не знает о маршрутах FastAPI.
"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Хеширует пароль алгоритмом bcrypt через passlib."""

    return _crypt.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Сравнивает открытый пароль и хеш; при неверных данных безопасно False.

    Не журналируйте строку пароля.
    """

    try:
        return _crypt.verify(plain, hashed)
    except ValueError:
        return False


def create_access_token(*, user_id: int, role: str) -> str:
    """
    Формирует JWT со стандартными полями sub, role, iat, exp — по ТЗ.

    Время жизни берётся из настроек; метки времени — UNIX epoch.
    """

    now = datetime.now(timezone.utc)
    ttl = timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + ttl).timestamp()),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


def decode_token(token: str) -> dict:
    """
    Проверяет подпись и срок действия JWT; возвращает полезную нагрузку.

    Битый или просроченный токен — исключение jose.JWTError.
    """

    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_alg],
    )
