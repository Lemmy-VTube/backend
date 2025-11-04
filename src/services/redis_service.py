import uuid
from time import time
from typing import Optional

from redis.asyncio import from_url

from src.config import config


class RedisService:
    def __init__(self):
        self.redis = from_url(
            config.REDIS_URL.get_secret_value(),
            decode_responses=True
        )

    async def get_ban(self, ip: str) -> Optional[int]:
        ban_until = await self.redis.get(f"ban:{ip}")
        return int(ban_until) if ban_until else None

    async def ban_ip(self, ip: str, seconds: int):
        now = int(time())
        await self.redis.set(f"ban:{ip}", now + seconds, ex=seconds)

    async def add_request(self, ip: str, window_seconds: int):
        now = int(time())
        key = f"req:{ip}"
        await self.redis.zadd(key, {f"{now}:{uuid.uuid4()}": now})
        await self.redis.expire(key, window_seconds)

    async def count_requests(self, ip: str, window_seconds: int) -> int:
        now = int(time())
        key = f"req:{ip}"
        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, 0, now - window_seconds)
            pipe.zcard(key)
            _, count = await pipe.execute()
        return count

    async def clear_requests(self, ip: str):
        await self.redis.delete(f"req:{ip}")


redis_service = RedisService()
