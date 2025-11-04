from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    tg_id: int = Field(..., ge=1, description="Telegram ID of the user")
    role: UserRole = Field(default=UserRole.user, description="User role")


class UserCreate(UserBase):
    ...


class UserUpdate(BaseModel):
    role: UserRole | None = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
