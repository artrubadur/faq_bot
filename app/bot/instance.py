from aiogram import Bot, Dispatcher

from app.core.config import config

bot = Bot(config.api_token)
dp = Dispatcher()
