from logging import getLogger
from typing import Sequence

from aiogram.utils.web_app import WebAppInitData

from src.config import config
from src.database.models.user import User
from src.database.repositories.user import UserRepository
from src.schemas.user import UserCreate, UserRole, UserUpdate

logger = getLogger(__name__)


class UserService:
    @staticmethod
    async def register_user(user_data: WebAppInitData) -> User | None:
        if not user_data.user:
            return None
        
        tg_id = user_data.user.id
        username = user_data.user.username
        first_name = user_data.user.first_name
        last_name = user_data.user.last_name
        photo_url = user_data.user.photo_url

        logger.debug(f"Attempting to register user with tg_id: {tg_id}")
        existing = await UserRepository.get_user(tg_id)
        if existing:
            logger.debug(f"User with tg_id {tg_id} already exists, returning existing user")
            return existing
        role = UserRole.admin if tg_id in config.ADMIN_IDS else UserRole.user
        logger.debug(f"Assigned role '{role.value}' to user with tg_id: {tg_id}")
        logger.debug(f"Creating new user with tg_id: {tg_id}")
        user = await UserRepository.create_user(
            UserCreate(
                tg_id=tg_id,
                role=role,
                username=username,
                first_name=first_name,
                last_name=last_name,
                photo_url=photo_url
            )
        )
        logger.debug(f"Successfully created user with id: {user.id}, tg_id: {tg_id}, role: {role}")
        return user
    
    @staticmethod
    async def update_user(tg_id: int, data: UserUpdate) -> User | None:
        logger.debug(f"Updating user {tg_id} with data: {data}")
        user = await UserRepository.update_user(tg_id, data)
        if user:
            logger.debug(f"Successfully updated user {tg_id}")
        else:
            logger.warning(f"User {tg_id} not found for update")
        return user
    
    @staticmethod
    async def accept_privacy_policy(tg_id: int) -> User | None:
        logger.debug(f"User {tg_id} attempts to accept privacy policy")
        user = await UserRepository.set_privacy_policy(tg_id, True)
        if user:
            logger.debug(f"User {tg_id} accepted privacy policy")
        else:
            logger.warning(f"User {tg_id} not found when accepting privacy policy")
        return user

    @staticmethod
    async def decline_privacy_policy(tg_id: int) -> User | None:
        logger.debug(f"User {tg_id} attempts to decline privacy policy")
        user = await UserRepository.set_privacy_policy(tg_id, False)
        if user:
            logger.debug(f"User {tg_id} declined privacy policy")
        else:
            logger.warning(f"User {tg_id} not found when declining privacy policy")
        return user

    @staticmethod
    async def set_not_new(tg_id: int) -> User | None:
        logger.debug(f"Setting user {tg_id} as not new (is_new=False)")
        user = await UserRepository.set_not_new(tg_id)
        if user:
            logger.debug(f"User {tg_id} is now marked as not new")
        else:
            logger.warning(f"User {tg_id} not found when setting is_new=False")
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
    async def get_user_by_id(id: int) -> User | None:
        logger.debug(f"Getting user with id: {id}")
        user = await UserRepository.get_user_by_id(id)
        if user:
            logger.debug(f"Found user with id: {id}, role: {user.role}")
        else:
            logger.debug(f"User with id {id} not found")
        return user

    @staticmethod
    async def get_admin_by_id(id: int) -> User | None:
        logger.debug(f"Getting admin with id: {id}")
        admin = await UserRepository.get_admin_by_id(id)
        if admin:
            logger.debug(f"Found admin with id: {id}, role: {admin.role}")
        else:
            logger.debug(f"Admin with id {id} not found")
        return admin

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
