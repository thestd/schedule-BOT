import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import Executor

from app.core.client import ApiClient
from app.core.config import TOKEN, MONGO_URL, MONGO_PORT, SKIP_UPDATES
from app.core.utils import RedisCache

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

api_client = ApiClient(RedisCache())

bot = Bot(token=TOKEN, loop=loop)
storage = MongoStorage(host=MONGO_URL, port=MONGO_PORT)
dp = Dispatcher(bot, storage=storage)

runner = Executor(dp, skip_updates=SKIP_UPDATES)
