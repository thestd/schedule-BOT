from aiogram import types
from aiogram.dispatcher import FSMContext

from app.core.misc import dp, bot
from app.modules.base.views import start_view

__all__ = ["cmd_start"]


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message, state: FSMContext, **kwargs):
    """
    Start conversation
    """
    print(kwargs)
    text, markup = start_view()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(chat_id=message.chat.id, text=text,
                           reply_markup=markup, parse_mode='HTML')
    await state.set_state("wait_query_type_register")
