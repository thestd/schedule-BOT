from aiogram import types
from aiogram.dispatcher import FSMContext

from app.core.misc import bot
from app.modules.base.handlers import cmd_start


async def invalid_msg(message: types.Message, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        # Delete old markups
        await bot.send_message(
            chat_id=message.chat.id,
            text=".",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await cmd_start(message, state)
        return

    await bot.delete_message(message.chat.id, message.message_id)


async def invalid_clb_data(query: types.CallbackQuery, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        # Delete old markups
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=".",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await cmd_start(query.message, state)
        return

    await bot.delete_message(query.message.chat.id, query.message.message_id)
