from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from src.schemas.roles import UserRole

if TYPE_CHECKING:
    from src.database.models.user import User


class UserBase(BaseModel):
    tg_id: int = Field(..., ge=1, description="Telegram ID of the user")
    role: UserRole = Field(default=UserRole.user, description="User role")
    is_new: bool = Field(default=True, description="Indicates whether the user is new")
    accepted_privacy_policy: bool = Field(
        default=False,
        description="Has the user accepted the privacy policy"
    )
    username: str | None = Field(None, description="Telegram username of the user (without @)")
    first_name: str = Field(..., description="First name of the user in Telegram")
    last_name: str | None = Field(None, description="Last name of the user in Telegram")
    photo_url: str | None = Field(None, description="URL of the user's Telegram profile photo")


class UserCreate(UserBase):
    ...


class UserUpdate(BaseModel):
    role: UserRole | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    photo_url: str | None = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserSchema(UserRead):
    @classmethod
    def from_models(cls, user: Optional[User]) -> Optional["UserSchema"]:
        if user is None:
            return None
        return cls(
            id=user.id,
            tg_id=user.tg_id,
            role=user.role,
            is_new=user.is_new,
            accepted_privacy_policy=user.accepted_privacy_policy,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
