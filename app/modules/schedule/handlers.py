from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from app.core.misc import bot, api_client, dp
from app.modules.schedule.state import ScheduleState
from app.modules.schedule.views import query_type_request, \
    generate_search_view, generate_predict_view

__all__ = ["query_register", "query_type_register", "search_query",
           "confirm_predicted_query"]


async def query_type_register(query: types.CallbackQuery, callback_data: dict,
                              state: FSMContext):
    """
    Save query type (teacher, group)
    """
    q_type = callback_data["type"]
    await bot.edit_message_text(
        text=query_type_request(q_type),
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    await state.update_data(query_type=q_type)
    await ScheduleState.query_register.set()


async def query_register(message: types.Message, state: FSMContext):
    """
    Save query (e.g. `ІПЗ-3`, `КН-41`)
    """
    usr_data = await state.get_data()

    values = await api_client.name_predict(
        usr_data["query_type"],
        message.text
    )

    await bot.delete_message(message.chat.id, message.message_id)
    if values:
        text, markup = generate_predict_view(values)
        await bot.send_message(
            text=text,
            chat_id=message.chat.id,
            reply_markup=markup,
            parse_mode='HTML'
        )
        await ScheduleState.confirm_predicted_query.set()
    else:
        await bot.send_message(
            text="Нічого не вдалось знайти, спробуй ще раз",
            chat_id=message.chat.id,
            parse_mode='HTML'
        )


async def confirm_predicted_query(query: types.CallbackQuery,
                                  callback_data: dict, state: FSMContext):
    await state.update_data(query=callback_data["query"])
    usr_data = await state.get_data()
    curr_day = datetime.now()
    week_start_date = curr_day - timedelta(days=curr_day.weekday())
    text, markup = await generate_search_view(
        usr_data["query"],
        usr_data["query_type"],
        week_start_date.strftime("%d.%m.%Y"),
        str(curr_day.weekday())
    )
    await bot.edit_message_text(
        text=text,
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )
    await ScheduleState.schedule_search.set()


async def handler_throttled(message: types.CallbackQuery, **kwargs):
    await message.answer("Wow. Easy easy)", show_alert=True)


@dp.throttled(handler_throttled, rate=.5)
async def search_query(query: types.CallbackQuery, callback_data: dict,
                       state: FSMContext):
    usr_data = await state.get_data()
    text, markup = await generate_search_view(
        usr_data["query"],
        usr_data["query_type"],
        callback_data["week_date"],
        callback_data["day_number"]
    )
    try:
        await bot.edit_message_text(
            text=text,
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=markup,
            parse_mode="HTML"
        )
    except MessageNotModified:
        pass
    finally:
        await query.answer()
