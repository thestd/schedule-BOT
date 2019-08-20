from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from app.core.misc import bot, db, api_client
from app.modules.base.handlers import cmd_change_query
from app.modules.schedule.views import query_type_view, query_view, \
    generate_search_view, generate_predict_view

__all__ = ["query_register", "query_type_register", "search_query",
           "confirm_predicted_query"]


async def query_type_register(query: types.CallbackQuery, callback_data: dict,
                              state: FSMContext, user: dict):
    """
    Save query type (teacher, group)
    """
    text = query_type_view()
    await bot.edit_message_text(text=text,
                                chat_id=query.message.chat.id,
                                message_id=query.message.message_id)
    await db.update_user(user["id"], query_type=callback_data["type"])
    await state.set_state("query_register")


async def query_register(message: types.Message, state: FSMContext,
                         user: dict):
    """
    Save query (e.g. `ІПЗ-3`, `КН-41`)
    """
    if not user["query_type"]:
        await cmd_change_query(message)
        return
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
                                  callback_data: dict, state: FSMContext,
                                  user: dict):
    await db.update_user(user["id"], query=callback_data["name"])
    text, markup = query_view(user["query_type"], callback_data["name"])
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(text=text,
                           chat_id=query.message.chat.id,
                           reply_markup=markup,
                           parse_mode='HTML')
    await state.set_state("search_query")


async def search_query(query: types.CallbackQuery, callback_data: dict,
                       user: dict):
    if not user["query_type"] or not user["query"]:
        await cmd_change_query(query.message)
        return

    markup = generate_search_view(user["query_type"], user["query"],
                                  callback_data["week_date"],
                                  callback_data["day_number"])
    try:
        await bot.edit_message_text(text=f"User: {user}"
                                         f"data: {callback_data}",
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=markup)
    except MessageNotModified:
        pass
    finally:
        await query.answer()
