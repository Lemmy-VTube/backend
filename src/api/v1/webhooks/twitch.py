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

    # Twitch сначала отправляет challenge-запрос при регистрации webhook-а
    if "challenge" in data:
        logger.info("🔐 Проверка webhook-а от Twitch...")
        return Response(content=data["challenge"], media_type="text/plain")

    # Обрабатываем событие начала стрима
    if data.get("subscription", {}).get("type") == "stream.online":
        event = data["event"]
        user_id = event["broadcaster_user_id"]
        logger.info(f"🔴 {event['broadcaster_user_name']} начал стрим! (user_id: {user_id})")

    return {"ok": True}