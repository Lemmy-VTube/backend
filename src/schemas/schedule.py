from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.database.models.schedule import Schedule


class ScheduleBase(BaseModel):
    photo_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=254,
        description="ID of the photo to be sent (1–254 chars)"
    )
    message_streamer_text: Optional[str] = Field(
        None,
        min_length=1,
        max_length=2000,
        description="Text of the message to be sent by the streamer (1–2000 chars)"
    )


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleUpdate(ScheduleBase):
    ...


class ScheduleRead(ScheduleBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ScheduleSchema(ScheduleRead):
    @classmethod
    def from_models(cls, schedule: Optional[Schedule]) -> Optional["ScheduleSchema"]:
        if schedule is None:
            return None
        return cls(
            photo_id=schedule.photo_id or "",
            message_streamer_text=schedule.message_streamer_text or "",
            created_at=schedule.created_at,
            updated_at=schedule.updated_at
        )
