from logging import getLogger

from src.database.models.schedule import Schedule
from src.database.repositories.schedule import ScheduleRepository
from src.schemas.schedule import ScheduleCreate, ScheduleUpdate

logger = getLogger(__name__)


class ScheduleService:
    @staticmethod
    async def get_schedule(id: int = 1) -> Schedule | None:
        logger.debug(f"Getting schedule with id: {id}")
        schedule = await ScheduleRepository.get_schedule(id)
        if schedule:
            logger.debug(f"Found schedule with id: {id}")
        else:
            logger.debug(f"Schedule with id {id} not found")
        return schedule
    
    @staticmethod
    async def create_schedule(schedule_data: ScheduleCreate) -> Schedule:
        logger.debug(f"Creating schedule with data: {schedule_data}")
        schedule = await ScheduleRepository.create_schedule(schedule_data)
        logger.debug(f"Successfully created schedule with id: {schedule.id}")
        return schedule

    @staticmethod
    async def update_schedule(schedule_data: ScheduleUpdate, id: int = 1) -> Schedule | None:
        logger.debug(f"Updating schedule with id: {id} and data: {schedule_data}")
        schedule = await ScheduleRepository.update_schedule(id, schedule_data)
        if schedule:
            logger.debug(f"Successfully updated schedule with id: {id}")
        else:
            logger.warning(f"Schedule with id {id} not found for update")
        return schedule
    


schedule_service = ScheduleService()
