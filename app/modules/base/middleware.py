from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

__all__ = ["StatMiddleware", ]


class StatMiddleware(BaseMiddleware):
    def __init__(self):
        super(StatMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        pass

    async def on_pre_process_callback_query(self,
                                            callback_query: types.CallbackQuery,
                                            data: dict):
        pass
