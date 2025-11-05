from fastapi import APIRouter

from src.api.v1 import schedule
from src.api.v1.admins import admin
from src.api.v1.users import user
from src.api.v1.webhooks import twitch


def setup_api_v1() -> APIRouter:
    router = APIRouter()

    router.include_router(user.router)
    router.include_router(admin.router)
    router.include_router(twitch.router)
    router.include_router(schedule.router)

    return router