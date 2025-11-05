from typing import List

from fastapi import APIRouter

from src.api.utils import check_user
from src.schemas.user import UserRole, UserSchema
from src.services.user_service import user_service
from src.utils.dependencies import UserDep
from src.utils.exceptions import (
    error_response_http,
    forbidden_json_error,
    not_found_json_error,
    success_response,
)
from src.utils.responses import custom_responses

router = APIRouter(prefix="/v1/admins", tags=["v1 - admins"])


@router.get(
    "/",
    summary="Get all admins",
    description="Returns a paginated list of all admins in the system.",
    responses=custom_responses,
    response_model=List[UserSchema]
)
async def get_admins(limit: int = 100, offset: int = 0):
    try:
        admins = await user_service.get_all_admins(limit, offset)
        admins_data = []

        for admin in admins:
            schema = UserSchema.from_models(admin)
            admins_data.append(schema.model_dump(mode="json") if schema else None)
        
        return success_response(
            data={"admins": admins_data},
            message=f"Retrieved {len(admins_data)} admins"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.get(
    "/get",
    summary="Get admin by id",
    description="Returns an admin by id.",
    responses=custom_responses,
    response_model=UserSchema
)
async def get_admin(id: int):
    try:    
        admin = await user_service.get_admin_by_id(id)
        if not admin:
            return not_found_json_error("Admin not found")

        schema = UserSchema.from_models(admin)
        return success_response(
            data={"admin": schema.model_dump(mode="json") if schema else None},
            message=f"Retrieved admin with id {id}"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.post(
    "/make/admin",
    summary="Make user admin",
    description="Makes a user an admin.",
    responses=custom_responses,
    response_model=UserSchema
)
async def make_admin_role(user_data: UserDep, tg_id: int):
    try:
        user = await check_user(user_data.user.id if user_data.user else 100000)
        if user and user.role != UserRole.admin:
            return forbidden_json_error("You do not have permission to make users admin.")
    
        user = await user_service.make_admin(tg_id)
        if not user:
            return not_found_json_error(f"User with id {tg_id} not found")

        schema = UserSchema.from_models(user)
        return success_response(
            data={"user": schema.model_dump(mode="json") if schema else None},
            message=f"User with id {tg_id} successfully set role to admin"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))

    
@router.post(
    "/remove/admin",
    summary="Remove admin role from user",
    description="Removes the admin role from a user.",
    responses=custom_responses,
    response_model=UserSchema
)
async def remove_admin_role(user_data: UserDep, tg_id: int):
    try:
        user = await check_user(user_data.user.id if user_data.user else 100000)
        if user and user.role != UserRole.admin:
            return forbidden_json_error(
                "You do not have permission to remove admin roles from users."
            )
    
        user = await user_service.remove_admin(tg_id)
        if not user:
            return not_found_json_error(f"User with id {tg_id} not found")

        schema = UserSchema.from_models(user)
        return success_response(
            data={"user": schema.model_dump(mode="json") if schema else None},
            message=f"User with id {tg_id} successfully removed admin role"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))