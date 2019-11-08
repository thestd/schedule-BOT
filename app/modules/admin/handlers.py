import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageCantBeDeleted, MessageToDeleteNotFound
)

from app.core.misc import storage, redis_cache, logger
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


@admin_requires
async def cmd_msg_to_users(message: types.Message, state: FSMContext):
    await message.answer("Enter message text:")
    await state.set_state("msg_to_send")
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


@admin_requires
async def msg_to_users(message: types.Message, state: FSMContext):
    await state.set_state("")
    db = await storage.get_db()
    users_list = await db['aiogram_data'].find({}).to_list()
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Видалити мене", callback_data="delete_me")
    )
    sent_count = 0
    err_count = 0
    for user in users_list:
        try:
            is_sent = await message.bot.send_message(
                chat_id=user["chat"],
                text=message.text,
                reply_markup=markup,
                clear=True
            )
            if is_sent:
                sent_count += 1
            else:
                err_count += 1
        except Exception as e:
            err_count += 1
            logger.error(e, exc_info=True)
            
        await asyncio.sleep(0.1)
    await message.answer(
        f"Total send: {sent_count}\n Errors: {err_count}"
    )
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


async def delete_msg(query: types.CallbackQuery):
    try:
        await query.message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
