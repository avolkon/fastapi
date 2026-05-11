"""
Декларативная база ORM для SQLAlchemy 2.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс моделей; метаданные используются при create_all."""
