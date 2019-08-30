from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.core.misc import mp


class StatisticMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self,
                                            callback_query: types.CallbackQuery,
                                            data: dict):
        if "q_type" in callback_query.data:
            mp.track(callback_query.message.chat.id, callback_query.data)
        elif "predict" in callback_query.data:
            mp.track(callback_query.message.chat.id, callback_query.data)

    async def on_pre_process_update(self, update: types.Update, data: dict):
        mp.track(update.update_id, "update_count")
