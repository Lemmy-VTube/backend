from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from fastapi import Request

from src.config import config
from src.database.models import User
from src.services.user_service import user_service
from src.utils.exceptions import unauthorized_error


def auth(request: Request) -> WebAppInitData:
    try:
        auth_string = request.headers.get("initData", None)
        if auth_string:
            data = safe_parse_webapp_init_data(
                config.TOKEN_BOT.get_secret_value(),
                auth_string
            )
            return data
        raise unauthorized_error()
    except Exception:
        raise unauthorized_error()
    

async def check_user(tg_id: int) -> User:
    user = await user_service.get_user(tg_id)
    if not user:
        raise unauthorized_error()
    return user