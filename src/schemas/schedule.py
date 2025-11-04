from datetime import datetime

from pydantic import BaseModel, Field


class ScheduleBase(BaseModel):
    photo_id: str = Field(..., ge=1, description="ID of the photo to be sent")
    message_streamer_text: str = Field(
        ..., description="Text of the message to be sent by the streamer"
    )


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleUpdate(BaseModel):
    photo_id: str | None = None
    message_streamer_text: str | None = None


class ScheduleRead(ScheduleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
