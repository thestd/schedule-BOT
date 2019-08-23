import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from app.core.client import ApiClient
from app.core.config import TOKEN, MONGO_URL
from app.core.utils import RedisCache

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

api_client = ApiClient(RedisCache())

bot = Bot(token=TOKEN, loop=loop)
storage = MongoStorage(host=MONGO_URL)
dp = Dispatcher(bot, storage=storage)
