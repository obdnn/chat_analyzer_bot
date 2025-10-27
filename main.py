import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv

from bot.handlers import chat_messages, stats

load_dotenv(find_dotenv())


async def main():
    bot_token = os.getenv("API_BOT")

    bot = Bot(token=bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(chat_messages.router)
    dp.include_router(stats.router)

    print("Start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Stop")
