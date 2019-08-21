import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from app.core.client import ApiClient
from app.core.config import bot_token

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
bot = Bot(token=bot_token, loop=loop)
api_client = ApiClient()
storage = MongoStorage(username="root", password="example")
dp = Dispatcher(bot, storage=storage)
