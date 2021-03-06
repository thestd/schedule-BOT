from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from app.api_client.exceptions import ServiceNotResponse
from app.core.misc import bot, api_client, dp, logger
from app.core.utils import Date
from app.modules.base.handlers import cmd_start
from app.modules.schedule.consts import week_days_btn
from app.modules.schedule.templates import error_text, flood_text, \
    cant_find_query, enter_date_text, error_date_text, next_week_text, \
    previous_week_text
from app.modules.schedule.state import ScheduleState
from app.modules.schedule.views import (
    query_type_request, schedule_view, generate_predict_view
)

__all__ = ["query_register", "query_type_register", "search_query",
           "manual_date_request", "manual_date_response", "shift_date",
           "back_handler"]


async def handler_throttled(message, **kwargs):
    if isinstance(message, types.Message):
        await message.delete()
    elif isinstance(message, types.CallbackQuery):
        await message.answer(flood_text, show_alert=True)


@dp.throttled(handler_throttled, rate=.5)
async def query_type_register(query: types.CallbackQuery, callback_data: dict,
                              state: FSMContext):
    """
    Save query type (teacher, group)
    """
    await query.message.answer(
        text=query_type_request(callback_data["type"]),
    )
    await state.update_data(query_type=callback_data["type"])
    await ScheduleState.query_register.set()


@dp.throttled(handler_throttled, rate=.5)
async def query_register(message: types.Message, state: FSMContext):
    """
    Save query (e.g. `ІПЗ-3`, `КН-41`)
    """
    usr_data = await state.get_data()

    try:
        values = await api_client.name_predict(
            usr_data["query_type"],
            message.text
        )
    except ServiceNotResponse:
        try:
            await message.delete()
        except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
            logger.error(e, exc_info=True)
        await message.answer(
            text=error_text,
            parse_mode='HTML'
        )
        return

    if values:
        if message.text in values:
            date = Date()
            await state.update_data(
                query=message.text,
                search_date=date.as_db_str
            )
            usr_data = await state.get_data()
            values = await api_client.name_predict(
                usr_data["query_type"],
                message.text
            )
            if message.text not in values:
                await query_register(message, state)
                return
            text, markup = await schedule_view(
                usr_data["query"],
                usr_data["query_type"],
                date
            )
            await message.answer(
                text=text,
                reply_markup=markup,
                parse_mode='HTML'
            )
            await ScheduleState.schedule_search.set()
        else:
            text, markup = generate_predict_view(values)
            await message.answer(
                text=text,
                reply_markup=markup,
                parse_mode='HTML'
            )
    else:
        await message.answer(
            text=cant_find_query,
            parse_mode='HTML'
        )

    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)


@dp.throttled(handler_throttled, rate=.5)
async def shift_date(message: types.Message, state: FSMContext):
    usr_data = await state.get_data()
    if "query" not in usr_data or "query_type" not in usr_data:
        await cmd_start(message, state)
        return

    date = Date(usr_data.get("search_date", None))
    if message.text == next_week_text:
        date.shift_week(7)
    elif message.text == previous_week_text:
        date.shift_week(-7)
    else:
        date = Date()
    await state.update_data(
        search_date=date.as_db_str
    )
    text, markup = await schedule_view(
        usr_data["query"],
        usr_data["query_type"],
        date
    )
    await message.answer(
        text=text,
        reply_markup=markup,
        parse_mode="HTML"
    )
    try:
        await message.delete()
    except MessageToDeleteNotFound:
        pass


@dp.throttled(handler_throttled, rate=.5)
async def search_query(message: types.Message, state: FSMContext):
    usr_data = await state.get_data()
    if "query" not in usr_data or "query_type" not in usr_data:
        await cmd_start(message, state)
        return

    date = Date(usr_data.get("search_date", None))
    date.day = week_days_btn[message.text]
    text, markup = await schedule_view(
        usr_data["query"],
        usr_data["query_type"],
        date
    )
    await message.answer(
        text=text,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await state.update_data(search_date=date.as_db_str)
    try:
        await message.delete()
    except MessageToDeleteNotFound:
        pass


@dp.throttled(handler_throttled, rate=.5)
async def manual_date_request(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))
    await message.answer(
        text=enter_date_text,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    await ScheduleState.manual_date.set()
    try:
        await message.delete()
    except MessageToDeleteNotFound:
        pass


@dp.throttled(handler_throttled, rate=.5)
async def manual_date_response(message: types.Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            text=error_date_text,
            parse_mode="Markdown"
        )
        return

    usr_data = await state.get_data()
    s_date = Date(date)
    text, markup = await schedule_view(
        usr_data["query"],
        usr_data["query_type"],
        s_date
    )
    await message.answer(
        text=text,
        reply_markup=markup,
        parse_mode='HTML'
    )
    await state.update_data(search_date=s_date.as_db_str)
    await ScheduleState.schedule_search.set()
    try:
        await message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)


async def back_handler(query: types.CallbackQuery, state: FSMContext):
    usr_data = await state.get_data()
    date = Date(usr_data.get("search_date", None))
    text, markup = await schedule_view(
        usr_data["query"],
        usr_data["query_type"],
        date
    )
    await query.message.answer(
        text=text,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await ScheduleState.schedule_search.set()
    await state.update_data(search_date=date.as_db_str)
    try:
        await query.message.delete()
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
