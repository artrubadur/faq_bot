from aiogram import Bot, Dispatcher

from app.core.config import API_TOKEN

# session = AiohttpSession(timeout=aiohttp.ClientTimeout(total=60, connect=10))
bot = Bot(API_TOKEN)  # pyright: ignore[reportArgumentType]
dp = Dispatcher()
