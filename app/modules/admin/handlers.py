from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, \
    MessageToDeleteNotFound

from app.core.misc import bot, storage, redis_cache
from app.modules.admin.utils import admin_requires


@admin_requires
async def users_count(message: types.Message):
    try:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
    db = await storage.get_db()
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{await db['aiogram_data'].count()}",
    )


@admin_requires
async def flush_cache(message: types.Message):
    try:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
    await redis_cache.flush_database()
    await bot.send_message(
        chat_id=message.chat.id,
        text="Cache flushed"
    )
