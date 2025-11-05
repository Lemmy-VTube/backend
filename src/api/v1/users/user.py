from typing import List

from fastapi import APIRouter

from src.schemas.user import UserSchema, UserUpdate
from src.services.user_service import user_service
from src.utils.dependencies import UserDep
from src.utils.exceptions import error_response_http, not_found_json_error, success_response
from src.utils.responses import custom_responses

router = APIRouter(prefix="/v1/users", tags=["v1 - users"])


@router.get(
    "/",
    summary="Get all users",
    description="Returns a paginated list of all users in the system.",
    responses=custom_responses,
    response_model=List[UserSchema]
)
async def get_users(limit: int = 100, offset: int = 0):
    try:
        users = await user_service.get_all_users(limit, offset)
        users_data = []

        for user in users:
            schema = UserSchema.from_models(user)
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
    responses=custom_responses,
    response_model=UserSchema
)
async def get_user(id: int):
    try:    
        user = await user_service.get_user_by_id(id)
        if not user:
            return not_found_json_error("User not found")

        schema = UserSchema.from_models(user)
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
    responses=custom_responses,
    response_model=UserSchema
)
async def get_me(user_data: UserDep):
    try:
        user = await user_service.register_user(user_data)
        if user and user.is_new:
            await user_service.set_not_new(user.tg_id)

        schema = UserSchema.from_models(user)
        return success_response(
            data={"user": schema.model_dump(mode="json") if schema else None},
            message="Successfully retrieved current user"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.put(
    "/update/me",
    summary="Update current user",
    description="Updates the current user.",
    responses=custom_responses,
    response_model=UserSchema
)
async def update_me(user_data: UserDep):
    try:
        tg_id = user_data.user.id if user_data.user else 100000
        user = await user_service.get_user(tg_id)
        if not user:
            return not_found_json_error("User not found")

        update_data = UserUpdate.model_validate(user_data.model_dump(exclude_unset=True))
        user = await user_service.update_user(tg_id, update_data)
        schema = UserSchema.from_models(user)

        return success_response(
            data={"user": schema.model_dump(mode="json") if schema else None},
            message="Successfully updated current user"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.delete(
    "/delete/me",
    summary="Delete current user",
    description="Deletes the current user.",
    responses=custom_responses
)
async def delete_me(user_data: UserDep):
    try:
        tg_id = user_data.user.id if user_data.user else 100000
        await user_service.delete_user(tg_id)
        return success_response(
            data={"deleted_id": tg_id},
            message=f"User with id {tg_id} successfully deleted"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.put(
    "/accept/privacy/policy",
    summary="Accept privacy policy",
    description="Accepts the privacy policy.",
    responses=custom_responses
)
async def accept_privacy_policy(user_data: UserDep):
    try:
        tg_id = user_data.user.id if user_data.user else 100000
        await user_service.accept_privacy_policy(tg_id)
        return success_response(
            data={"accepted_id": tg_id},
            message=f"User with id {tg_id} successfully accepted privacy policy"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.put(
    "/decline/privacy/policy",
    summary="Decline privacy policy",
    description="Declines the privacy policy.",
    responses=custom_responses
)
async def decline_privacy_policy(user_data: UserDep):
    try:
        tg_id = user_data.user.id if user_data.user else 100000
        await user_service.decline_privacy_policy(tg_id)
        return success_response(
            data={"declined_id": tg_id},
            message=f"User with id {tg_id} successfully declined privacy policy"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))