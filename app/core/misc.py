import asyncio
import logging

import uvloop
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import Executor

from app.api_client.base import ApiClient
from app.core.bot import ClearBot
from app.core.config import (
    TOKEN, MONGO_URL, MONGO_PORT, SKIP_UPDATES, MONGO_DB
)
from app.core.utils import RedisCache

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/bot.log")
file_handler.setLevel(logging.INFO)
error_file_handle = logging.FileHandler("logs/bot_errors.log")
error_file_handle.setLevel(logging.ERROR)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
error_file_handle.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_file_handle)

# Just some tricks to speed-up bot
uvloop.install()

loop = asyncio.get_event_loop()

redis_cache = RedisCache()
api_client = ApiClient(redis_cache)

bot = ClearBot(token=TOKEN, loop=loop)
storage = MongoStorage(host=MONGO_URL, port=MONGO_PORT, db_name=MONGO_DB)
dp = Dispatcher(bot, storage=storage)

runner = Executor(dp, skip_updates=SKIP_UPDATES)
