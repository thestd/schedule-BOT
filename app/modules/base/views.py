from aiogram import types

from app.modules.schedule.consts import query_type


def start_view() -> (str, types.InlineKeyboardMarkup):
    text = "Привіт, я оновлена версія бота для розкладу. Для початку скажи " \
           "мені хто ти:"
    line_markup = types.InlineKeyboardMarkup(row_width=2)
    line_markup.add(types.InlineKeyboardButton(
        "Студент",
        callback_data=query_type.new("student"))
    )
    line_markup.add(types.InlineKeyboardButton(
        "Викладач",
        callback_data=query_type.new("teacher"))
    )
    return text, line_markup

