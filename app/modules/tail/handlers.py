from aiogram import types

from app.core.misc import bot


async def invalid_msg(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


async def invalid_clb_data(query: types.CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
