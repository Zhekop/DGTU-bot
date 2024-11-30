import asyncio 
from time import strftime 
from config import bot, dp
import app


async def main():
    dp.include_routers(
        app.RouterMain
    )

    # await set_command(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        now_time = strftime("%H:%M")
        print(f'Bot started at {now_time}')
        asyncio.run(main()) 
    except KeyboardInterrupt:
        pass