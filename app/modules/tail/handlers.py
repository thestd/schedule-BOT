from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageCantBeDeleted, \
    MessageToDeleteNotFound

from app.modules.base.handlers import cmd_start


async def invalid_msg(message: types.Message, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        # Delete old markups
        await message.answer(
            text=".",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await cmd_start(message, state)
        return
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


async def invalid_clb_data(query: types.CallbackQuery, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        # Delete old markups
        await query.message.answer(
            text=".",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await cmd_start(query.message, state)
        return
    try:
        await query.message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
