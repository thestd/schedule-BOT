from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils import emoji

from app.modules.schedule.consts import query_for_search, week_days, \
    query_predict


def query_type_view() -> str:
    return "Готово. Тепер відправ мені запит:"


def query_view(q_type: str, query: str) -> (str, types.InlineKeyboardMarkup):
    text = f"<i>Розклад для {query}</i>"
    today = datetime.now()
    week_start_date = today - timedelta(days=today.weekday())
    return text, generate_search_view(q_type, query,
                                      week_start_date.strftime("%d.%m.%Y"),
                                      f"{today.weekday()}")


def _generate_single_key(txt: str, q_type: str, query: str,
                         week_start_date: str,
                         day_number: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        txt,
        callback_data=query_for_search.new(q_type, query, week_start_date,
                                           day_number)
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


def generate_search_view(q_type: str, query: str, week_date: str,
                         day_number: str) -> types.InlineKeyboardMarkup:
    week_date = datetime.strptime(week_date, '%d.%m.%Y')
    today = datetime.now()
    today_week = today - timedelta(days=today.weekday())
    prev_week = (week_date - timedelta(days=7)).strftime("%d.%m.%Y")
    next_week = (week_date + timedelta(days=7)).strftime("%d.%m.%Y")

    days_markup = []
    for day in week_days:
        day_name = day
        if week_days[day] == int(day_number):
            day_name = emoji.emojize(":black_circle:")

        days_markup.append(
            _generate_single_key(day_name, q_type, query,
                                 week_date.strftime("%d.%m.%Y"),
                                 week_days[day])
        )

    markup = types.InlineKeyboardMarkup(row_width=7)
    markup.add(*days_markup)
    markup.add(
        _generate_single_key("return to today", q_type, query,
                             today_week.strftime("%d.%m.%Y"),
                             f"{today.weekday()}")
    )
    markup.add(
        _generate_single_key("Previous week", q_type, query, prev_week,
                             day_number),
        _generate_single_key("Next week", q_type, query, next_week,
                             day_number),
    )

    return markup
