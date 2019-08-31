import logging
from datetime import datetime

from aiogram import Dispatcher

from app.core.config import WEBHOOK_URL, WEBHOOK_ENABLE, \
    WEBHOOK_SERVER
from app.core.helper import module_loader

from app.core.misc import runner


async def shutdown_webhook(dp: Dispatcher):
    await dp.bot.delete_webhook()


async def startup_webhook(dp: Dispatcher):
    await dp.bot.set_webhook(WEBHOOK_URL)


async def shutdown_polling(dp: Dispatcher):
    dp.stop_polling()


async def startup_polling(dp: Dispatcher):
    await dp.bot.delete_webhook()


def run():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        filename=f"logs/{datetime.now().strftime('%d.%m.%Y-%H:%M')}.txt"
    )
    module_loader()
    runner.on_startup(startup_polling, polling=True, webhook=False)
    runner.on_shutdown(shutdown_polling, polling=True, webhook=False)
    runner.on_startup(startup_webhook, polling=False, webhook=True)
    runner.on_shutdown(shutdown_webhook, polling=False, webhook=True)

    if WEBHOOK_ENABLE:
        runner.start_webhook(**WEBHOOK_SERVER)
    else:
        runner.start_polling()
