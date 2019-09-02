from functools import wraps

from aiogram import types

from app.core.config import ADMIN_IDS


def admin_requires(f):
    @wraps(f)
    async def wrapped(message: types.Message, *args, **kwargs):
        if not ADMIN_IDS or message.from_user.id not in ADMIN_IDS:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            return None
        else:
            return await f(message, *args, **kwargs)

    return wrapped
