import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from bot.handlers.start_handler import start_router
from bot.handlers.monitoring_handler import monitoring_router
from bot.handlers.streamer_handler import router
from bot.config.command_list import private


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot=bot)
    dp.include_router(start_router)
    dp.include_router(monitoring_router)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
