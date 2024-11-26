from .conf import TOKEN_API

from aiogram import Bot, Dispatcher

bot = Bot(TOKEN_API)
dp = Dispatcher()

db_name:str = 'database'