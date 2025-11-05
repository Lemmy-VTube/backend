from fastapi import APIRouter

from src.api.utils import check_user
from src.schemas.schedule import ScheduleCreate, ScheduleSchema, ScheduleUpdate
from src.schemas.user import UserRole
from src.services.schedule_service import schedule_service
from src.utils.dependencies import UserDep
from src.utils.exceptions import (
    error_response_http,
    forbidden_json_error,
    not_found_json_error,
    success_response,
)
from src.utils.responses import custom_responses

router = APIRouter(prefix="/v1/schedule", tags=["v1 - schedule"])

@router.get(
    "/",
    summary="Get stream schedule",
    description=(
        "Returns the current stream schedule with all available entries. "
        "Accessible to all users."
    ),
    responses=custom_responses,
    response_model=ScheduleSchema
)
async def get_schedule():
    try:
        schedule = await schedule_service.get_schedule()
        schema = ScheduleSchema.from_models(schedule)
        return success_response(
            data={ "schedule": schema.model_dump(mode="json") if schema else None},
            message="Successfully fetched the stream schedule"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.post(
    "/create",
    summary="Create a new schedule entry",
    description=(
        "Creates a new stream schedule entry. "
        "Only administrators are allowed to perform this action."
    ),
    responses=custom_responses,
    response_model=ScheduleSchema
)
async def create_schedule(user_data: UserDep, schedule_data: ScheduleCreate):
    try:
        user = await check_user(user_data.user.id if user_data.user else 100000)
        if user and user.role != UserRole.admin:
            return forbidden_json_error("You do not have permission to create schedules.")
    
        schedule = await schedule_service.create_schedule(schedule_data)
        schema = ScheduleSchema.from_models(schedule)
        return success_response(
            data={ "schedule": schema.model_dump(mode="json") if schema else None},
            message="Schedule successfully created"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.put(
    "/update/{id}",
    summary="Update an existing schedule",
    description=(
        "Updates the data of an existing stream schedule entry. "
        "Only administrators are allowed to perform this action."
    ),
    responses=custom_responses,
    response_model=ScheduleSchema
)
async def update_schedule(id: int, user_data: UserDep, schedule_data: ScheduleUpdate):
    try:
        user = await check_user(user_data.user.id if user_data.user else 100000)
        if user and user.role != UserRole.admin:
            return forbidden_json_error("You do not have permission to update schedules.")
    
        schedule = await schedule_service.update_schedule(id, schedule_data)
        if not schedule:
            return not_found_json_error(f"Schedule with id {id} not found.")
    
        schema = ScheduleSchema.from_models(schedule)
        return success_response(
            data={ "schedule": schema.model_dump(mode="json") if schema else None},
            message="Schedule successfully updated"
    )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.delete(
    "/delete/{id}",
    summary="Delete a schedule entry",
    description=(
        "Deletes a stream schedule entry by ID. "
        "Only administrators are allowed to perform this action."
    ),
    responses=custom_responses
)
async def delete_schedule(id: int, user_data: UserDep):
    try:
        user = await check_user(user_data.user.id if user_data.user else 100000)
        if user and user.role != UserRole.admin:
            return forbidden_json_error("You do not have permission to delete schedules.")
    
        deleted = await schedule_service.delete_schedule(id)
        if not deleted:
            return not_found_json_error(f"Schedule with id {id} not found.")
    
        return success_response(
            data={"deleted_id": id},
            message=f"Schedule with id {id} successfully deleted"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))