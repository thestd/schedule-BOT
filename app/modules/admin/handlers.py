from aiogram import types
from aiogram.utils.exceptions import (
    MessageCantBeDeleted, MessageToDeleteNotFound
)

from app.core.misc import storage, redis_cache
from app.modules.admin.utils import admin_requires


@admin_requires
async def users_count(message: types.Message):
    db = await storage.get_db()
    await message.answer(
        text=f"{await db['aiogram_data'].count()}",
    )
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


@admin_requires
async def flush_cache(message: types.Message):
    await redis_cache.flush_database()
    await message.answer(
        text="Cache flushed"
    )
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


@admin_requires
async def get_user(message: types.Message):
    await message.answer(
        text=f"<a href='tg://user?id={message.text.split()[-1]}'>User</a>",
        parse_mode='HTML'
    )
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
