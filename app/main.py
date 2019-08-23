from aiogram.utils import executor

from app.core.config import SKIP_UPDATES
from app.core.helper import module_loader
from app.core.misc import dp, loop


def run():
    module_loader()
    executor.start_polling(dp, loop=loop, skip_updates=SKIP_UPDATES)
