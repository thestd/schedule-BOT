from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.core.misc import mp, logger


class StatisticMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self,
                                            callback_query: types.CallbackQuery,
                                            data: dict):
        if mp:
            if "q_type" in callback_query.data:
                try:
                    mp.track(callback_query.message.chat.id,
                             callback_query.data)
                except Exception as e:
                    logger.error(e)
            elif "predict" in callback_query.data:
                try:
                    mp.track(callback_query.message.chat.id,
                             callback_query.data)
                except Exception as e:
                    logger.error(e)

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
                mp.track(update.update_id, "update_count")
            except Exception as e:
                logger.error(e)
