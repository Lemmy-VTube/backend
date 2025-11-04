from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass

from src.database.models.schedule import Schedule  # noqa: E402
from src.database.models.user import User  # noqa: E402

__all__ = [
    "Base",
    "Schedule",
    "User"
]