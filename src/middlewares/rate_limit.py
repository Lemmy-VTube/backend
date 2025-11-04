from time import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import config
from src.services.redis_service import redis_service
from src.utils.exceptions import too_many_requests_error

IGNORED_PATHS = {"/", "/versions", "/docs", "/openapi.json", "/favicon.ico"}


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.max_requests = config.RATELIMIT_MAX_REQUESTS
        self.window_seconds = config.RATELIMIT_WINDOW_SECONDS
        self.ban_seconds = config.RATELIMIT_BAN_SECONDS

    async def dispatch(self, request: Request, call_next):
        if request.url.path in IGNORED_PATHS:
            return await call_next(request)

        ip = request.client.host if request.client else "127.0.1.1"
        now = int(time())
        ban_until = await redis_service.get_ban(ip)
        
        if ban_until and ban_until > now:
            return too_many_requests_error(
                f"You are banned for {ban_until - now} more seconds",
            )

        count = await redis_service.count_requests(ip, self.window_seconds)
        await redis_service.add_request(ip, self.window_seconds)
        if count + 1 > self.max_requests:
            await redis_service.ban_ip(ip, self.ban_seconds)
            await redis_service.clear_requests(ip)
            return too_many_requests_error(
                f"Rate limit exceeded. You are banned for {self.ban_seconds // 60} minutes.",
            )
        return await call_next(request)
