from aiogram import types

from app.modules.base.templates import choice_student_text, choice_teacher_text
from app.modules.schedule.consts import query_type


def query_type_markup() -> types.InlineKeyboardMarkup:
    line_markup = types.InlineKeyboardMarkup()
    line_markup.add(
        types.InlineKeyboardButton(
            choice_student_text,
            callback_data=query_type.new("group")
        )
    )
    line_markup.add(
        types.InlineKeyboardButton(
            choice_teacher_text,
            callback_data=query_type.new("teacher")
        )
    )
    return line_markup
