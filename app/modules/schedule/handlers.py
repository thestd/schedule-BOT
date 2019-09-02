from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, \
    MessageCantBeDeleted, MessageToDeleteNotFound, ButtonDataInvalid

from app.api_client.exceptions import ServiceNotResponse
from app.core.misc import bot, api_client, dp, logger
from app.modules.schedule.templates import error_text, flood_text, \
    cant_find_query, enter_date_text, error_date_text
from app.modules.schedule.state import ScheduleState
from app.modules.schedule.views import query_type_request, \
    generate_search_view, generate_predict_view

__all__ = ["query_register", "query_type_register", "search_query",
           "confirm_predicted_query", "manual_date_request",
           "manual_date_response"]


async def handler_throttled(message, **kwargs):
    if isinstance(message, types.Message):
        await bot.delete_message(message.chat.id, message.message_id)
    elif isinstance(message, types.CallbackQuery):
        await message.answer(flood_text, show_alert=True)


@dp.throttled(handler_throttled, rate=.5)
async def query_type_register(query: types.CallbackQuery, callback_data: dict,
                              state: FSMContext):
    """
    Save query type (teacher, group)
    """
    try:
        await bot.send_message(
            text=query_type_request(callback_data["type"]),
            chat_id=query.message.chat.id,
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)
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
            await bot.delete_message(message.chat.id, message.message_id)
        except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
            logger.error(e, exc_info=True)
        try:
            await bot.send_message(
                text=error_text,
                chat_id=message.chat.id,
                parse_mode='HTML'
            )
        except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
            logger.error(e, exc_info=True)
        return

    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)
    if values:
        text, markup = generate_predict_view(values)
        try:
            await bot.send_message(
                text=text,
                chat_id=message.chat.id,
                reply_markup=markup,
                parse_mode='HTML'
            )
        except ButtonDataInvalid as e:
            logger.error(e, exc_info=True)
        await ScheduleState.confirm_predicted_query.set()
    else:
        try:
            await bot.send_message(
                text=cant_find_query,
                chat_id=message.chat.id,
                parse_mode='HTML'
            )
        except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
            logger.error(e, exc_info=True)
        return


@dp.throttled(handler_throttled, rate=.5)
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
    try:
        await bot.send_message(
            text=text,
            chat_id=query.message.chat.id,
            reply_markup=markup,
            parse_mode='HTML'
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)
    await ScheduleState.schedule_search.set()


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
        await query.answer()
    except MessageToEditNotFound:
        try:
            await bot.send_message(
                text=text,
                chat_id=query.message.chat.id,
                reply_markup=markup,
                parse_mode="HTML"
            )
        except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
            logger.error(e, exc_info=True)
    except MessageNotModified:
        await query.answer()


@dp.throttled(handler_throttled, rate=.5)
async def manual_date_request(callback_data: dict):
    try:
        await bot.send_message(
            chat_id=callback_data["message"]["chat"]["id"],
            text=enter_date_text,
            parse_mode="Markdown"
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)
    await ScheduleState.manual_date.set()


@dp.throttled(handler_throttled, rate=.5)
async def manual_date_response(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(
            message.chat.id,
            message.message_id
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=error_date_text,
                parse_mode="Markdown"
            )
        except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
            logger.error(e, exc_info=True)
        return

    curr_day = date
    week_start_date = curr_day - timedelta(days=curr_day.weekday())
    usr_data = await state.get_data()
    text, markup = await generate_search_view(
        usr_data["query"],
        usr_data["query_type"],
        week_start_date.strftime("%d.%m.%Y"),
        str(curr_day.weekday())
    )
    try:
        await bot.send_message(
            text=text,
            chat_id=message.chat.id,
            reply_markup=markup,
            parse_mode='HTML'
        )
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.error(e, exc_info=True)
    await ScheduleState.schedule_search.set()
