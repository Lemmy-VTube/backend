from datetime import datetime
from enum import Enum
from typing import Optional

from aiogram.utils.web_app import WebAppInitData
from pydantic import BaseModel, Field

from src.database.models.user import User


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    tg_id: int = Field(..., ge=1, description="Telegram ID of the user")
    role: UserRole = Field(default=UserRole.user, description="User role")
    is_new: bool = Field(default=True, description="Indicates whether the user is new")
    accepted_privacy_policy: bool = Field(
        default=False,
        description="Has the user accepted the privacy policy"
    )


class UserCreate(UserBase):
    ...


class UserUpdate(BaseModel):
    role: UserRole | None = None
    accepted_privacy_policy: bool | None = None


class UserRead(BaseModel):
    id: int
    role: UserRole = Field(default=UserRole.user, description="User role in the system")
    username: str | None = Field(None, description="Telegram username of the user (without @)")
    first_name: str = Field(..., description="First name of the user in Telegram")
    last_name: str | None = Field(None, description="Last name of the user in Telegram")
    photo_url: str | None = Field(None, description="URL of the user's Telegram profile photo")
    is_new: bool = Field(..., description="Whether the user is new or returning")
    accepted_privacy_policy: bool = Field(
        ...,
        description="Whether the user accepted the privacy policy"
    )
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserSchema(UserRead):
    @classmethod
    def from_models(
        cls,
        user_data: WebAppInitData,
        user: Optional[User]
    ) -> Optional["UserSchema"]:
        if user is None:
            return None
        return cls(
            id=user.id,
            role=user.role,
            username=user_data.user.username if user_data.user else None,
            first_name=user_data.user.first_name if user_data.user else "Unknown",
            last_name=user_data.user.last_name if user_data.user else None,
            photo_url=user_data.user.photo_url if user_data.user else None,
            is_new=user.is_new,
            accepted_privacy_policy=user.accepted_privacy_policy,
            created_at=user.created_at,
            updated_at=user.updated_at
        )