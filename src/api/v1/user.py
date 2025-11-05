from fastapi import APIRouter

from src.schemas.user import UserSchema
from src.services.user_service import user_service
from src.utils.dependencies import auth
from src.utils.exceptions import success_response
from src.utils.responses import custom_responses

router = APIRouter(prefix="/v1/users", tags=["v1 - users"], dependencies=[auth])


@router.get(
    "/",
    summary="Get all users",
    description="Returns a paginated list of all users in the system.",
    responses=custom_responses
)
async def get_users(limit: int = 100, offset: int = 0):
    users = await user_service.get_all_users(limit, offset)
    users_data = []

    for user in users:
        schema = UserSchema.from_models(user=user)
        if schema:
            users_data.append(schema.model_dump(mode="json"))
    
    return success_response(
        data={"users": users_data},
        message=f"Retrieved {len(users_data)} users"
    )