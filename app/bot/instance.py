from aiogram import Bot, Dispatcher
from redis.asyncio import Redis

from app.core.config import config
from app.storage.temp import TempStorage

redis_client = Redis(host=config.redis.host, password=config.redis.password)

storage = TempStorage(redis_client, config.redis.long_ttl, config.redis.short_ttl)

bot = Bot(config.bot.token)
dp = Dispatcher(storage=storage)
