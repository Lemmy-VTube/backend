import logging

from fastapi import Request, Response
from faststream.rabbit.fastapi import RabbitRouter

from src.config import config

logger = logging.getLogger(__name__)


router = RabbitRouter(
    url=config.RABBITMQ_URL.get_secret_value(),
    prefix="/v1/webhooks/twitch",
    tags=["v1 - webhooks - twitch"],
)

@router.post("/callback")
async def twitch_event(request: Request):
    data = await request.json()

    if "challenge" in data:
        return Response(content=data["challenge"], media_type="text/plain")

    if data.get("subscription", {}).get("type") == "stream.online":
        logger.info(data)
        event = data["event"]
    return {"ok": True}