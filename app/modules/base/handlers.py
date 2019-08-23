from aiogram import types
from aiogram.dispatcher import FSMContext

from app.core.misc import bot
from app.modules.base.views import start_view, about_view, help_view, \
    change_view
from app.modules.schedule.state import ScheduleState

__all__ = ["cmd_start", "cmd_change_query", "cmd_about", "cmd_help"]


async def cmd_start(message: types.Message, state: FSMContext):
    """
    Start conversation
    """
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=await about_view(),
        parse_mode='HTML'
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=help_view(),
        parse_mode='HTML'
    )
    text, markup = start_view()
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup,
        parse_mode='HTML'
    )
    await state.update_data(
        message.from_user.to_python(),
        msg_to_edit=message.message_id
    )
    await ScheduleState.query_type_register.set()


async def cmd_change_query(message: types.Message):
    """
    Change query type
    """
    text, markup = change_view()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup,
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
        text=await about_view(),
        parse_mode='HTML'
    )


async def cmd_help(message: types.Message):
    """
    Help with commands
    """
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=help_view(),
        parse_mode='HTML'
    )
