from aiogram import Router

from .santa import RouterSanta

RouterMain = Router()

RouterMain.include_routers(
    RouterSanta
)