import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from app.dispatcher import add_handlers


def run(bot_token, skip_updates=True):
    loop = asyncio.get_event_loop()
    bot = Bot(token=bot_token, loop=loop)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    add_handlers(dp)
    executor.start_polling(dp, loop=loop, skip_updates=skip_updates)
