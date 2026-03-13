from loguru import logger

import app.storage.models  # noqa: F401
from app.core.config import config
from app.storage.base import Base
from app.storage.instance import engine
from app.storage.schema_sync import ensure_schema_constraints


async def init_db():
    logger.debug("Initializing the database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.debug("Tables created")
    await ensure_schema_constraints(
        config.db_schema.question_text_max_len,
        config.db_schema.answer_text_max_len,
        config.db_schema.question_embedding_dim,
    )
    logger.info("The database is initialized")


async def close_db():
    logger.debug("Closing the database")
    await engine.dispose()
    logger.info("The database connection pool closed")
