from aiogram.utils import executor

from app.core.config import skip_updates
from app.core.helper import load_modules
from app.core.misc import dp, loop


def run():
    load_modules()
    executor.start_polling(dp, loop=loop, skip_updates=skip_updates)
