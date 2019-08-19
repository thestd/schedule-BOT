from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.core.misc import dp


class MyMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        print(message)
        data["User"] = message.from_user.id


dp.middleware.setup(MyMiddleware())
