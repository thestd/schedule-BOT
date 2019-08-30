import asyncio
import logging

import uvloop
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import Executor
from mixpanel import Mixpanel

from app.api_client.base import ApiClient
from app.core.bot import ClearBot
from app.core.config import TOKEN, MONGO_URL, MONGO_PORT, SKIP_UPDATES, \
    MIX_PANEL_TOKEN
from app.core.utils import RedisCache

logger = logging.getLogger(__name__)

# Just some tricks to speed-up bot
uvloop.install()

loop = asyncio.get_event_loop()

api_client = ApiClient(RedisCache())

bot = ClearBot(token=TOKEN, loop=loop)
storage = MongoStorage(host=MONGO_URL, port=MONGO_PORT)
dp = Dispatcher(bot, storage=storage)

runner = Executor(dp, skip_updates=SKIP_UPDATES)

if MIX_PANEL_TOKEN:
    mp = Mixpanel(MIX_PANEL_TOKEN)
