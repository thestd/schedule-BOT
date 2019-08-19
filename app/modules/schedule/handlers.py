from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from app.core.misc import dp, bot
from app.modules.schedule.consts import query_type, search_query
from app.modules.schedule.views import query_type_view, query_view, \
    generate_search_view

__all__ = ["query_register", "query_type_register"]


@dp.callback_query_handler(query_type.filter(),
                           state="wait_query_type_register")
async def query_type_register(query: types.CallbackQuery, callback_data: dict,
                              state: FSMContext):
    """
    Save query type (teacher, group)
    """
    text = query_type_view()
    await bot.edit_message_text(text=text,
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id)
    async with state.proxy() as data:
        data['query_type'] = callback_data["type"]
        data["msg"] = query.message.message_id

    await state.set_state("wait_query_register")


@dp.message_handler(state='*')
async def query_register(message: types.Message, state: FSMContext):
    """
    Save query (e.g. `ІПЗ-3`, `КН-41`)
    """
    async with state.proxy() as data:
        data["query"] = message.text
        text, markup = query_view(data["query"], data['query'])
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.edit_message_text(text,
                                    chat_id=message.chat.id,
                                    reply_markup=markup,
                                    message_id=data["msg"],
                                    parse_mode='HTML')
        await state.set_state("wait_search_query")


@dp.callback_query_handler(search_query.filter(), state="wait_search_query")
async def search_query(query: types.CallbackQuery, callback_data: dict,
                       state: FSMContext):
    async with state.proxy() as data:
        markup = generate_search_view(data["query_type"], data["query"],
                                      callback_data["week_date"],
                                      callback_data["day_number"])
    try:
        await bot.edit_message_text(text=f"{callback_data}",
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=markup)
        await query.answer()
    except MessageNotModified:
        pass
