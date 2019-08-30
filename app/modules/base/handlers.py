from aiogram import types
from aiogram.dispatcher import FSMContext

from app.core.misc import bot
from app.modules.base.templates import about_text, help_text, \
    change_query_text, welcome_text
from app.modules.base.views import query_type_markup
from app.modules.schedule.state import ScheduleState

__all__ = ["cmd_start", "cmd_change_query", "cmd_about", "cmd_help"]


async def cmd_start(message: types.Message, state: FSMContext):
    """
    Start conversation
    """
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=".",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        reply_markup=query_type_markup(),
        parse_mode='HTML'
    )
    await state.update_data(
        message.from_user.to_python()
    )
    await ScheduleState.query_type_register.set()


async def cmd_change_query(message: types.Message):
    """
    Change query type
    """
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=change_query_text,
        reply_markup=query_type_markup(),
        parse_mode='HTML'
    )
    await ScheduleState.query_type_register.set()


async def cmd_about(message: types.Message):
    """
    Info about bot
    """
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=about_text,
        parse_mode='HTML'
    )


async def cmd_help(message: types.Message):
    """
    Help with commands
    """
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=help_text,
        parse_mode='HTML'
    )
