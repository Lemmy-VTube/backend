from fastapi import APIRouter

from src.api.v1 import admin, schedule, user


def setup_api_v1() -> APIRouter:
    router = APIRouter()

    router.include_router(user.router)
    router.include_router(admin.router)
    router.include_router(schedule.router)

    return router