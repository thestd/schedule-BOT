import asyncio
import logging

import uvloop
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import Executor

from app.api_client.base import ApiClient
from app.core.bot import ClearBot
from app.core.config import (
    TOKEN, MONGO_URL, MONGO_PORT, SKIP_UPDATES, MONGO_DB, MONGO_USER, MONGO_PSWD, REDIS_URI
)
from app.core.utils import RedisCache


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Just some tricks to speed-up bot
uvloop.install()

loop = asyncio.get_event_loop()

redis_cache = RedisCache(uri=REDIS_URI)
api_client = ApiClient(redis_cache)

bot = ClearBot(token=TOKEN, loop=loop)
storage = MongoStorage(host=MONGO_URL, port=MONGO_PORT, db_name=MONGO_DB, username=MONGO_USER, password=MONGO_PSWD)
dp = Dispatcher(bot, storage=storage)

runner = Executor(dp, skip_updates=SKIP_UPDATES)
