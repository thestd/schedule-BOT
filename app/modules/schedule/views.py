from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import emoji

from app.api_client.exceptions import ServiceNotResponse
from app.core.misc import api_client
from app.modules.schedule.consts import query_for_search, week_days_btn, \
    query_predict, week_days_full_name
from app.modules.schedule.templates import student_welcome, teacher_welcome, \
    error_text, today_text, next_week_text, previous_week_text, \
    no_lessons_text, find_query, manual_date_entry


def query_type_request(query_type: str) -> str:
    return student_welcome if query_type == "group" else teacher_welcome


def _generate_single_key(text: str, week_start_date: str,
                         day_number: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text,
        callback_data=query_for_search.new(week_start_date, day_number)
    )


def generate_predict_view(values: list) -> (str, types.InlineKeyboardMarkup):
    markup = types.InlineKeyboardMarkup()
    for elem in values:
        markup.add(types.InlineKeyboardButton(
            elem,
            callback_data=query_predict.new(elem))
        )
    return find_query, markup


async def _generate_schedule_text(query: str,
                                  requested_day: str,
                                  schedule_data: dict,
                                  day_number: str) -> str:
    header = (f"<strong>Розклад на {requested_day}"
              f" ({week_days_full_name[int(day_number)]})\n"
              f"{query}</strong>\n")
    lessons = schedule_data["schedule"]
    if not lessons:
        body = no_lessons_text
    else:
        stack = []
        for lesson in lessons:
            for detail in lesson["items"]:
                stack.append(
                    (
                        f"<i>{detail['number']} пара "
                        f"({detail['time_bounds']})</i>\n"
                        f"{detail['info']}"
                    )
                )
        body = "\n\n".join(stack)
    return f"{header}\n{body}"


async def generate_search_view(
        query: str,
        query_type: str,
        requested_week: str,
        day_number: str) -> (str, types.InlineKeyboardMarkup):
    # Data for keys
    requested_week = datetime.strptime(requested_week, '%d.%m.%Y')
    curr_day = datetime.now()
    curr_first_week_day = curr_day - timedelta(days=curr_day.weekday())
    prev_week = (requested_week - timedelta(days=7)).strftime("%d.%m.%Y")
    next_week = (requested_week + timedelta(days=7)).strftime("%d.%m.%Y")
    requested_day = (
            requested_week + timedelta(days=int(day_number))
    ).strftime("%d.%m.%Y")

    try:
        # Make API call
        schedule_data = await api_client.get_schedule(
            {
                query_type: query,
                "date_from": requested_day
            }
        )
    except ServiceNotResponse:
        return error_text, None
    text = await _generate_schedule_text(query, requested_day, schedule_data,
                                         day_number)

    # Search keys
    days_markup = []
    for day in week_days_btn:
        day_name = day
        if week_days_btn[day] == int(day_number):
            day_name = emoji.emojize(":black_circle:")

        days_markup.append(
            _generate_single_key(
                day_name,
                requested_week.strftime("%d.%m.%Y"),
                week_days_btn[day]
            )
        )

    markup = types.InlineKeyboardMarkup(row_width=7)
    markup.add(*days_markup)
    markup.add(
        _generate_single_key(
            today_text,
            curr_first_week_day.strftime("%d.%m.%Y"),
            f"{curr_day.weekday()}"
        )
    )
    markup.add(
        _generate_single_key(previous_week_text, prev_week, day_number),
        _generate_single_key(next_week_text, next_week, day_number),
    )
    markup.add(
        types.InlineKeyboardButton(
            manual_date_entry,
            callback_data="manual_data"
        )
    )

    return text, markup
