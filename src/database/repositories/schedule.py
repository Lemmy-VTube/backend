from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.database.models.schedule import Schedule
from src.schemas.schedule import ScheduleCreate, ScheduleUpdate


class ScheduleRepository:
    @staticmethod
    async def get_schedule(id: int = 1) -> Schedule | None:
        async with async_session() as session:
            return await session.scalar(select(Schedule).where(Schedule.id == id)) or None

    @staticmethod
    async def create_schedule(schedule_data: ScheduleCreate) -> Schedule:
        async with async_session() as session:
            try:
                session.add(schedule := Schedule(**schedule_data.model_dump()))
                await session.commit()
                await session.refresh(schedule)
                return schedule
            except IntegrityError:
                await session.rollback()
                raise

    @staticmethod
    async def update_schedule(id: int, schedule_data: ScheduleUpdate) -> Schedule | None:
        async with async_session() as session:
            if not (schedule := await session.scalar(select(Schedule).where(Schedule.id == id))):
                return None
            for key, value in schedule_data.model_dump(exclude_unset=True).items():
                setattr(schedule, key, value)
            await session.commit()
            await session.refresh(schedule)
            return schedule