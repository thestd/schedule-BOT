from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.core.misc import mp, logger


class StatisticMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            logger.info(
                f"New update: {update.message}"
            )
        elif update.callback_query:
            logger.info(
                f"New update: {update.callback_query}"
            )
        if mp:
            try:
                mp.track("update", )
            except Exception as e:
                logger.error(e)
