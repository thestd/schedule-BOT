from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils import emoji

from app.core.misc import api_client
from app.modules.schedule.consts import query_for_search, week_days, \
    query_predict


def query_type_view(query_type: str) -> str:
    if query_type == "group":
        return "Готово. Тепер відправ мені шфир (або частину шифру) своєї " \
               "групи:"
    else:
        return "Готово. Тепер відправ мені своє прізвище:"


def query_view(query: str, query_type: str) -> (str,
                                                types.InlineKeyboardMarkup):
    text = f"<i>Розклад для {query}</i>"
    today = datetime.now()
    week_start_date = today - timedelta(days=today.weekday())
    return text, generate_search_view(query, query_type,
                                      week_start_date.strftime("%d.%m.%Y"),
                                      f"{today.weekday()}")


def _generate_single_key(txt: str, week_start_date: str,
                         day_number: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        txt,
        callback_data=query_for_search.new(week_start_date, day_number)
    )


def generate_predict_view(values: list) -> (str, types.InlineKeyboardMarkup):
    text = "Ось що вдалося знайти:"
    markup = types.InlineKeyboardMarkup()
    for elem in values:
        markup.add(types.InlineKeyboardButton(
            elem,
            callback_data=query_predict.new(elem))
        )
    return text, markup


async def generate_search_view(query: str, query_type: str, week_date: str,
                               day_number: str) -> (
        str, types.InlineKeyboardMarkup):
    week_date = datetime.strptime(week_date, '%d.%m.%Y')
    today = datetime.now()
    today_week = today - timedelta(days=today.weekday())
    prev_week = (week_date - timedelta(days=7)).strftime("%d.%m.%Y")
    next_week = (week_date + timedelta(days=7)).strftime("%d.%m.%Y")
    requested_day = (week_date + timedelta(days=int(day_number))).strftime(
        "%d.%m.%Y")
    res = await api_client.get_schedule({query_type: query,
                                         "date_from": requested_day})
    text = f"{query} to {requested_day}\n{res}"

    days_markup = []
    for day in week_days:
        day_name = day
        if week_days[day] == int(day_number):
            day_name = emoji.emojize(":black_circle:")

        days_markup.append(
            _generate_single_key(day_name, week_date.strftime("%d.%m.%Y"),
                                 week_days[day])
        )

    markup = types.InlineKeyboardMarkup(row_width=7)
    markup.add(*days_markup)
    markup.add(
        _generate_single_key("return to today",
                             today_week.strftime("%d.%m.%Y"),
                             f"{today.weekday()}")
    )
    markup.add(
        _generate_single_key("Previous week", prev_week, day_number),
        _generate_single_key("Next week", next_week, day_number),
    )

    return text, markup
