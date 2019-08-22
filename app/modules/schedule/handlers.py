from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from app.core.misc import bot, api_client
from app.modules.schedule.views import query_type_view, \
    generate_search_view, generate_predict_view

__all__ = ["query_register", "query_type_register", "search_query",
           "confirm_predicted_query"]


async def query_type_register(query: types.CallbackQuery, callback_data: dict,
                              state: FSMContext):
    """
    Save query type (teacher, group)
    """
    text = query_type_view(callback_data["type"])
    await bot.edit_message_text(text=text,
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id)
    await state.update_data(query_type=callback_data["type"])
    await state.set_state("query_register")


async def query_register(message: types.Message, state: FSMContext):
    """
    Save query (e.g. `ІПЗ-3`, `КН-41`)
    """
    usr_data = await state.get_data()
    if usr_data["query_type"] == "teacher":
        values = await api_client.teacher_predict(message.text)
    else:
        values = await api_client.group_predict(message.text)

    await bot.delete_message(message.chat.id, message.message_id)
    if values:
        txt, markup = generate_predict_view(values)
        await bot.send_message(text=txt,
                               chat_id=message.chat.id,
                               reply_markup=markup,
                               parse_mode='HTML')
        await state.set_state("confirm_predicted_query")
    else:
        await bot.send_message(text="Нічого не вдалось знайти, спробуй ще "
                                    "раз",
                               chat_id=message.chat.id,
                               parse_mode='HTML')


async def confirm_predicted_query(query: types.CallbackQuery,
                                  callback_data: dict, state: FSMContext):
    await state.update_data(query=callback_data["name"])
    usr_data = await state.get_data()
    today = datetime.now()
    week_start_date = today - timedelta(days=today.weekday())
    text, markup = await generate_search_view(usr_data["query"],
                                              usr_data["query_type"],
                                              week_start_date.strftime(
                                                  "%d.%m.%Y"),
                                              f"{today.weekday()}")
    await bot.edit_message_text(text=text,
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                reply_markup=markup,
                                parse_mode='HTML')
    await state.set_state("search_query")


async def search_query(query: types.CallbackQuery, callback_data: dict,
                       state: FSMContext):
    usr_data = await state.get_data()
    text, markup = await generate_search_view(usr_data["query"],
                                              usr_data["query_type"],
                                              callback_data["week_date"],
                                              callback_data["day_number"])
    try:
        await bot.edit_message_text(text=text,
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=markup)
    except MessageNotModified:
        pass
    finally:
        await query.answer()
