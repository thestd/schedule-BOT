from aiogram import types
from aiogram.utils import emoji

from app.api_client.exceptions import ServiceNotResponse
from app.core.misc import api_client
from app.core.utils import Date
from app.modules.schedule.consts import week_days_btn, query_predict, \
    week_days_full_name
from app.modules.schedule.templates import student_welcome, teacher_welcome, \
    error_text, today_text, next_week_text, previous_week_text, \
    no_lessons_text, find_query, manual_date_entry, to_many_query_find


def query_type_request(query_type: str) -> str:
    return student_welcome if query_type == "group" else teacher_welcome


def generate_predict_view(values: list) -> (str, types.ReplyKeyboardMarkup):
    markup = types.ReplyKeyboardMarkup()
    text = find_query
    if len(values) > 15:
        values = values[:15]
        text = to_many_query_find + find_query
    for idx, elem in enumerate(values):
        markup.add(types.InlineKeyboardButton(
            elem,
            callback_data=query_predict.new(idx))
        )
    return text, markup


async def _get_schedule_text(query: str,
                             schedule_data: dict,
                             date: Date) -> str:
    header = (
        f"<strong>Розклад на {date.as_string}"
        f" ({week_days_full_name[date.day]})\n"
        f"{query}</strong>\n"
    )
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


async def _get_schedule_markup(week_day: int) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=7)
    # Search keys
    days_markup = []
    for day in week_days_btn:
        day_name = day
        if week_days_btn[day] == week_day:
            day_name = emoji.emojize(":black_circle:")

        days_markup.append(types.KeyboardButton(day_name))

    markup.add(*days_markup)
    markup.add(
        types.KeyboardButton(previous_week_text),
        types.KeyboardButton(today_text),
        types.KeyboardButton(next_week_text),
    )
    markup.add(
        types.KeyboardButton(manual_date_entry),
    )
    markup.add(
        types.KeyboardButton("Змінити запит"),
        types.KeyboardButton("Про бота"),
        types.KeyboardButton("Допомога"),
    )
    return markup


async def schedule_view(query: str,
                        query_type: str,
                        date: Date) -> (str, types.ReplyKeyboardMarkup):
    try:
        # Make API call
        schedule_data = await api_client.get_schedule(
            {
                query_type: query,
                "date_from": date.as_string
            }
        )
    except ServiceNotResponse:
        return error_text, None

    text = await _get_schedule_text(
        query,
        schedule_data,
        date
    )
    markup = await _get_schedule_markup(date.day)
    return text, markup
