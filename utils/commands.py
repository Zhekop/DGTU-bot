from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='santa',
            description='Запуск санты(можно только в лс бота)'
        ),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
