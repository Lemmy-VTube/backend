import asyncio
from datetime import datetime, timedelta, timezone
from logging import getLogger

from twitchAPI.helper import first
from twitchAPI.twitch import Twitch

from src.config import config

logger = getLogger(__name__)


class TwitchService:
    def __init__(
        self,
        target_username: str = config.STREAMER_USERNAME,
        callback_url: str = f"{config.BACKEND_URL.get_secret_value()}/v1/webhooks/twitch/callback",
        twitch_client_id: str = config.TWITCH_CLIENT_ID.get_secret_value(),
        twitch_client_secret: str = config.TWITCH_CLIENT_SECRET.get_secret_value(),
        twitch_webhook_secret: str = config.TWITCH_WEBHOOK_SECRET.get_secret_value()
    ):
        self.target_username = target_username
        self.callback_url = callback_url
        self.twitch_client_id = twitch_client_id
        self.twitch_client_secret = twitch_client_secret
        self.twitch_webhook_secret = twitch_webhook_secret

        self.subscription_online = "stream.online"
        self.subscription_offline = "stream.offline"

        self.twitch: Twitch
        self.user_id: str = "724335221"

    async def startup(self):
        logger.debug("Starting TwitchService...")
        self.twitch = await Twitch(self.twitch_client_id, self.twitch_client_secret)
        logger.debug("Twitch client initialized")
        user = await first(self.twitch.get_users(logins=[self.target_username]))
        if user:
            self.user_id = user.id
            logger.debug(f"Streamer {self.target_username} found with user_id: {self.user_id}")
        else:
            logger.warning(
                f"Streamer {self.target_username} not found, using default user_id: {self.user_id}"
            )
        asyncio.create_task(self._auto_renew_subscription())
        logger.debug("Auto-renew subscription task started")

    async def shutdown(self):
        logger.debug("Shutting down TwitchService...")
        await self.twitch.close()
        logger.debug("Twitch client closed")

    async def get_current_stream_info(self, user_id: str):
        stream = await first(self.twitch.get_streams(user_id=[user_id]))
        if stream:
            return {
                "title": stream.title,
                "game_name": stream.game_name,
                "is_live": True,
            }
        return {"title": None, "game_name": None, "is_live": False}

    async def _auto_renew_subscription(self):
        while True:
            try:
                logger.debug("Checking existing EventSub subscriptions...")
                subs = await self.twitch.get_eventsub_subscriptions()
                online_sub = None
                offline_sub = None

                for sub in subs.data:
                    broadcaster_user_id = sub.condition.get("broadcaster_user_id")
                    if broadcaster_user_id != self.user_id:
                        continue
                    if sub.type == self.subscription_online:
                        online_sub = sub
                    elif sub.type == self.subscription_offline:
                        offline_sub = sub

                if not online_sub or (
                    online_sub.created_at + timedelta(days=5) < datetime.now(timezone.utc)
                ):
                    if online_sub:
                        await self.twitch.delete_eventsub_subscription(online_sub.id)
                        logger.debug(f"Online subscription {online_sub.id} deleted")
                    logger.debug("Creating a new EventSub subscription for stream.online...")
                    await self.twitch.create_eventsub_subscription(
                        subscription_type=self.subscription_online,
                        version="1",
                        condition={"broadcaster_user_id": self.user_id},
                        transport={
                            "method": "webhook",
                            "callback": self.callback_url,
                            "secret": self.twitch_webhook_secret
                        }
                    )
                    logger.debug("✅ EventSub subscription for stream.online created/renewed")

                if not offline_sub or (
                    offline_sub.created_at + timedelta(days=5) < datetime.now(timezone.utc)
                ):
                    if offline_sub:
                        await self.twitch.delete_eventsub_subscription(offline_sub.id)
                        logger.debug(f"Offline subscription {offline_sub.id} deleted")
                    logger.debug("Creating a new EventSub subscription for stream.offline...")
                    await self.twitch.create_eventsub_subscription(
                        subscription_type=self.subscription_offline,
                        version="1",
                        condition={"broadcaster_user_id": self.user_id},
                        transport={
                            "method": "webhook",
                            "callback": self.callback_url,
                            "secret": self.twitch_webhook_secret
                        }
                    )
                    logger.debug("✅ EventSub subscription for stream.offline created/renewed")
            except Exception as e:
                logger.error(f"⚠️ Error while checking/updating subscriptions: {e}")
            await asyncio.sleep(24 * 60 * 60)


twitch_service = TwitchService()