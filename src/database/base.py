from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import config
from src.database.models import Base

engine = create_async_engine(url=config.DB_URL.get_secret_value(), echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()