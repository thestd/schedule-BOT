from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.core.misc import db

__all__ = ["UserStorageMiddleware", ]


class UserStorageMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserStorageMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if not user:
            user = await db.add_user(message.from_user.to_python())
        data["user"] = user

    async def on_pre_process_callback_query(self,
                                            callback_query: types.CallbackQuery,
                                            data: dict):
        user_id = callback_query.from_user.id
        user = await db.get_user(user_id)
        if not user:
            user = await db.add_user(callback_query.from_user.to_python())
        data["user"] = user
