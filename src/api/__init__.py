from fastapi import APIRouter

from src.api import common
from src.api.v1 import setup_api_v1


def setup_api_router() -> APIRouter:
    router = APIRouter()

    router.include_router(common.router)
    router.include_router(setup_api_v1())

    return router