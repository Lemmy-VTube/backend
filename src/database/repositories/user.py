from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.database.models.user import User
from src.schemas.user import UserCreate, UserRole


async def _get_by_tg(session, tg_id: int) -> User | None:
    return await session.scalar(select(User).where(User.tg_id == tg_id)) or None


class UserRepository:
    @staticmethod
    async def get_user(tg_id: int) -> User | None:
        async with async_session() as session:
            return await _get_by_tg(session, tg_id)

    @staticmethod
    async def get_users(limit: int = 100, offset: int = 0) -> Sequence[User]:
        async with async_session() as session:
            return (await session.scalars(select(User).offset(offset).limit(limit))).all()

    @staticmethod
    async def get_admins(limit: int = 100, offset: int = 0) -> Sequence[User]:
        async with async_session() as session:
            stmt = select(User).where(User.role == UserRole.admin).offset(offset).limit(limit)
            return (await session.scalars(stmt)).all()

    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        async with async_session() as session:
            try:
                session.add(user := User(**user_data.model_dump()))
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError:
                await session.rollback()
                raise

    @staticmethod
    async def delete_user(tg_id: int) -> bool:
        async with async_session() as session:
            if not (user := await _get_by_tg(session, tg_id)):
                return False
            await session.delete(user)
            await session.commit()
            return True

    @staticmethod
    async def set_role(tg_id: int, role: UserRole) -> User | None:
        async with async_session() as session:
            if not (user := await _get_by_tg(session, tg_id)):
                return None
            user.role = role
            await session.commit()
            await session.refresh(user)
            return user