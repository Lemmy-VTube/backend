from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import setup_api_router
from src.config import config
from src.database import close_db, init_db
from src.middlewares.rate_limit import RateLimitMiddleware
from src.services.twitch_service import twitch_service

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.debug("Starting application initialization...")
    logger.debug("Initializing database...")
    await init_db()
    logger.debug("Database initialized successfully")
    await twitch_service.startup()
    logger.debug("TwitchService started successfully")
    logger.debug("Application started successfully")
    
    yield

    logger.debug("Shutting down application...")
    await twitch_service.shutdown()
    logger.debug("TwitchService shutdown completed")
    logger.debug("Closing database connections...")
    await close_db()
    logger.debug("Database connections closed successfully")


app = FastAPI(
    lifespan=lifespan,
    version=config.PROJECT_VERSION,
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.include_router(setup_api_router())