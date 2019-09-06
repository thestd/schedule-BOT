from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageCantBeDeleted, MessageToDeleteNotFound
)

from app.modules.base.templates import (
    about_text, help_text, change_query_text, welcome_text
)
from app.modules.base.views import query_type_markup
from app.modules.schedule.state import ScheduleState

__all__ = ["cmd_start", "cmd_change_query", "cmd_about", "cmd_help"]


async def cmd_start(message: types.Message, state: FSMContext):
    """
    Start conversation
    """
    await message.answer(
        text=welcome_text,
        reply_markup=query_type_markup(),
        parse_mode='HTML'
    )
    await state.update_data(
        message.from_user.to_python()
    )
    await ScheduleState.query_type_register.set()
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


async def cmd_change_query(message: types.Message):
    """
    Change query type
    """
    await message.answer(
        text=change_query_text,
        reply_markup=query_type_markup(),
        parse_mode='HTML'
    )
    await ScheduleState.query_type_register.set()
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


async def cmd_about(message: types.Message, state: FSMContext):
    """
    Info about bot
    """
    if await state.get_state() == ScheduleState.schedule_search.state:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))
    else:
        markup = None

    await message.answer(
        text=about_text,
        reply_markup=markup,
        parse_mode='HTML'
    )
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass


async def cmd_help(message: types.Message, state: FSMContext):
    """
    Help with commands
    """
    if await state.get_state() == ScheduleState.schedule_search.state:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))
    else:
        markup = None

    await message.answer(
        text=help_text,
        reply_markup=markup,
        parse_mode='HTML'
    )
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
