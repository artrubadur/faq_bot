from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.storage.models  # noqa: F401
from app.core.config import config

engine = create_async_engine(config.database_url)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
