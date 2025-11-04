from logging import getLogger
from typing import Sequence

from src.config import config
from src.database.models.user import User
from src.database.repositories.user import UserRepository
from src.schemas.user import UserCreate, UserRole

logger = getLogger(__name__)


class UserService:
    @staticmethod
    async def register_user(tg_id: int) -> User:
        logger.debug(f"Attempting to register user with tg_id: {tg_id}")
        existing = await UserRepository.get_user(tg_id)
        if existing:
            logger.debug(f"User with tg_id {tg_id} already exists, returning existing user")
            return existing
        role = UserRole.admin if tg_id in config.ADMIN_IDS else UserRole.user
        logger.debug(f"Assigned role '{role.value}' to user with tg_id: {tg_id}")
        logger.debug(f"Creating new user with tg_id: {tg_id}")
        user = await UserRepository.create_user(UserCreate(tg_id=tg_id, role=role))
        logger.debug(f"Successfully created user with id: {user.id}, tg_id: {tg_id}, role: {role}")
        return user

    @staticmethod
    async def delete_user(tg_id: int) -> bool:
        logger.debug(f"Attempting to delete user with tg_id: {tg_id}")
        result = await UserRepository.delete_user(tg_id)
        if result:
            logger.debug(f"Successfully deleted user with tg_id: {tg_id}")
        else:
            logger.warning(f"User with tg_id {tg_id} not found for deletion")
        return result

    @staticmethod
    async def make_admin(tg_id: int) -> User | None:
        logger.debug(f"Attempting to make user admin with tg_id: {tg_id}")
        user = await UserRepository.set_role(tg_id, UserRole.admin)
        if user:
            logger.debug(f"Successfully made user admin with tg_id: {tg_id}")
        else:
            logger.warning(f"User with tg_id {tg_id} not found when making admin")
        return user

    @staticmethod
    async def remove_admin(tg_id: int) -> User | None:
        logger.debug(f"Attempting to remove admin role from user with tg_id: {tg_id}")
        user = await UserRepository.set_role(tg_id, UserRole.user)
        if user:
            logger.debug(f"Successfully removed admin role from user with tg_id: {tg_id}")
        else:
            logger.warning(f"User with tg_id {tg_id} not found when removing admin role")
        return user

    @staticmethod
    async def get_user(tg_id: int) -> User | None:
        logger.debug(f"Getting user with tg_id: {tg_id}")
        user = await UserRepository.get_user(tg_id)
        if user:
            logger.debug(f"Found user with tg_id: {tg_id}, role: {user.role}")
        else:
            logger.debug(f"User with tg_id {tg_id} not found")
        return user

    @staticmethod
    async def get_all_users(limit: int = 100, offset: int = 0) -> Sequence[User]:
        logger.debug("Getting all users")
        users = await UserRepository.get_users(limit, offset)
        logger.debug(f"Retrieved {len(users)} users")
        return users

    @staticmethod
    async def get_all_admins(limit: int = 100, offset: int = 0) -> Sequence[User]:
        logger.debug("Getting all admin users")
        admins = await UserRepository.get_admins(limit, offset)
        logger.debug(f"Retrieved {len(admins)} admin users")
        return admins


user_service = UserService()
