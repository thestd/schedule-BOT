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

logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler("logs/bot.log")
fh.setLevel(logging.INFO)
error_file_handle = logging.FileHandler("logs/bot_errors.log")
error_file_handle.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
error_file_handle.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(error_file_handle)
# Just some tricks to speed-up bot
uvloop.install()

loop = asyncio.get_event_loop()

redis_cache = RedisCache()
api_client = ApiClient(redis_cache)

bot = ClearBot(token=TOKEN, loop=loop)
storage = MongoStorage(host=MONGO_URL, port=MONGO_PORT)
dp = Dispatcher(bot, storage=storage)

runner = Executor(dp, skip_updates=SKIP_UPDATES)

if MIX_PANEL_TOKEN:
    mp = Mixpanel(MIX_PANEL_TOKEN)
else:
    mp = None
