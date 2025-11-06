from fastapi import Request, Response
from faststream.rabbit.fastapi import RabbitRouter

from src.config import config
from src.services.twitch_service import twitch_service

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
    
    subscription = data.get("subscription", {})
    event = data.get("event", {})
    subscription_type = subscription.get("type")
    
    if subscription_type == "stream.online" and event:
        user_id = event["broadcaster_user_id"]
        user_name = event["broadcaster_user_name"]
        stream_info = await twitch_service.get_current_stream_info(user_id)
        await router.broker.publish(
            {
                "event": "stream_online",
                "user_name": user_name,
                "title": stream_info["title"],
                "game_name": stream_info["game_name"]
            },
            queue="twitch_streams",
        )
    elif subscription_type == "stream.offline" and event:
        user_name = event["broadcaster_user_name"]
        await router.broker.publish(
            {
                "event": "stream_offline",
                "user_name": user_name,
                "title": None,
                "game_name": None
            },
            queue="twitch_streams",
        )
    return {"ok": True}
