import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from app.core.client import ApiClient
from app.core.config import bot_token
from app.core.utils import RedisCache

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
bot = Bot(token=bot_token, loop=loop)
storage = MongoStorage(username="root", password="example")
redis_storage = RedisCache()
api_client = ApiClient(redis_storage)
dp = Dispatcher(bot, storage=storage)
