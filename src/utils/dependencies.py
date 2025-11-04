from typing import Annotated

from aiogram.utils.web_app import WebAppInitData
from fastapi import Depends

from src.api.utils import auth as auth_func

auth = Depends(auth_func)
UserDep = Annotated[WebAppInitData, auth]
