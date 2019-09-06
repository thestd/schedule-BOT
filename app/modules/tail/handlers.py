from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from app.modules.base.handlers import cmd_start
from app.modules.base.views import query_type_markup
from app.modules.schedule.state import ScheduleState
from app.modules.tail.templates import update_info_text


async def invalid_msg(message: types.Message, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        await cmd_start(message, state)
        return
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


async def old_callback(query: types.CallbackQuery, state: FSMContext):
    await ScheduleState.query_type_register.set()
    await query.message.answer(
        update_info_text,
        reply_markup=query_type_markup()
    )


async def invalid_clb_data(query: types.CallbackQuery, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        await cmd_start(query.message, state)
        return
    try:
        await query.message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
