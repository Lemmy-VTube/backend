from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import setup_api_router
from src.config import config
from src.database import close_db, init_db
from src.middlewares.rate_limit import RateLimitMiddleware

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.debug("Starting application initialization...")
    logger.debug("Initializing database...")
    await init_db()
    logger.debug("Database initialized successfully")
    logger.debug("Application started successfully")
    
    yield

    logger.debug("Shutting down application...")    
    logger.debug("Closing database connections...")
    await close_db()
    logger.debug("Database connections closed successfully")


app = FastAPI(
    lifespan=lifespan,
    docs_url="/swagger",
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