import logging

import aiohttp
from fastapi import HTTPException, Request
from faststream.rabbit.fastapi import RabbitRouter

from src.config import config

logger = logging.getLogger(__name__)


router = RabbitRouter(
    url=config.RABBITMQ_URL.get_secret_value(),
    prefix="/v1/webhooks/twitch",
    tags=["v1 - webhooks - twitch"],
)


TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_API_BASE = "https://api.twitch.tv/helix"


async def _get_app_access_token() -> str:
    timeout = aiohttp.ClientTimeout(total=30)
    params = {
        "client_id": config.TWITCH_CLIENT_ID.get_secret_value(),
        "client_secret": config.TWITCH_CLIENT_SECRET.get_secret_value(),
        "grant_type": "client_credentials",
    }
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(TWITCH_TOKEN_URL, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Twitch token error: {text}")
            data = await resp.json()
            return data["access_token"]


async def _get_user_id_by_login(access_token: str, username: str) -> str | None:
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID.get_secret_value(),
        "Authorization": f"Bearer {access_token}",
    }
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(
            f"{TWITCH_API_BASE}/users", headers=headers, params={"login": username}
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                logger.error("Failed to fetch user id: %s", text)
                return None
            data = (await resp.json()).get("data", [])
            return data[0]["id"] if data else None


async def _subscribe_stream_online(
    access_token: str,
    broadcaster_user_id: str,
    callback_url: str,
) -> dict:
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID.get_secret_value(),
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "type": "stream.online",
        "version": "1",
        "condition": {"broadcaster_user_id": broadcaster_user_id},
        "transport": {
            "method": "webhook",
            "callback": callback_url,
            "secret": config.TWITCH_WEBHOOK_SECRET.get_secret_value(),
        },
    }
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            f"{TWITCH_API_BASE}/eventsub/subscriptions", headers=headers, json=payload
        ) as resp:
            data = await resp.json()
            return {"status_code": resp.status, **data}


@router.post("/")
async def twitch_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Challenge verification
    challenge = data.get("challenge")
    if challenge:
        logger.info("Twitch challenge received")
        return {"challenge": challenge}

    subscription = (data or {}).get("subscription", {})
    event = (data or {}).get("event", {})
    if subscription.get("type") == "stream.online":
        message = {
            "provider": "twitch",
            "type": "stream.online",
            "broadcaster_user_id": event.get("broadcaster_user_id"),
            "broadcaster_user_name": event.get("broadcaster_user_name"),
            "started_at": event.get("started_at"),
            "raw": data,
        }

        await router.broker.publish(
            message,
            queue="events.twitch.stream_online",
        )
        logger.info(
            "Published stream.online event for %s",
            event.get("broadcaster_user_name"),
        )

    return {"status": "ok"}


@router.post("/subscribe")
async def subscribe_stream_online():
    access_token = await _get_app_access_token()
    username = config.STREAMER_USERNAME
    print(access_token)
    user_id = await _get_user_id_by_login(access_token, username)
    if not user_id:
        raise HTTPException(status_code=404, detail=f"User {username} not found")

    callback_url = f"{config.BACKEND_URL}/v1/webhooks/twitch"
    result = await _subscribe_stream_online(access_token, user_id, callback_url)

    if result.get("status_code") not in (200, 202):
        raise HTTPException(status_code=400, detail=result)

    return {
        "status": "subscribed",
        "username": username,
        "user_id": user_id,
        "twitch_response": result,
    }