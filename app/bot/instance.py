from aiogram import Bot, Dispatcher

from app.core.config import config

bot = Bot(config.tg_api_token)
dp = Dispatcher()
