from fastapi import APIRouter

from src.schemas.user import UserSchema
from src.services.user_service import user_service
from src.utils.dependencies import UserDep
from src.utils.exceptions import error_response_http, not_found_json_error, success_response
from src.utils.responses import custom_responses

router = APIRouter(prefix="/v1/users", tags=["v1 - users"])


@router.get(
    "/",
    summary="Get all users",
    description="Returns a paginated list of all users in the system.",
    responses=custom_responses
)
async def get_users(limit: int = 100, offset: int = 0):
    try:
        users = await user_service.get_all_users(limit, offset)
        users_data = []

        for user in users:
            schema = UserSchema.from_models(user=user)
            users_data.append(schema.model_dump(mode="json") if schema else None)
        
        return success_response(
            data={"users": users_data},
            message=f"Retrieved {len(users_data)} users"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.get(
    "/get",
    summary="Get user by id",
    description="Returns a user by id.",
    responses=custom_responses
)
async def get_user(id: int):
    try:    
        user = await user_service.get_user_by_id(id)
        if not user:
            return not_found_json_error(details="User not found")

        schema = UserSchema.from_models(user=user)
        return success_response(
            data={"user": schema.model_dump(mode="json") if schema else None},
            message=f"Retrieved user with id {id}"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.get(
    "/get/me",
    summary="Get current user",
    description="Returns the current user.",
    responses=custom_responses
)
async def get_me(user_data: UserDep):
    ...
