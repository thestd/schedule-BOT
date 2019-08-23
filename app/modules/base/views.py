from aiogram import types
from aiogram.utils.emoji import emojize

from app.modules.schedule.consts import query_type
from app.core.misc import bot


def query_type_markup() -> types.InlineKeyboardMarkup:
    line_markup = types.InlineKeyboardMarkup(row_width=2)
    line_markup.add(
        types.InlineKeyboardButton(
            "Студент",
            callback_data=query_type.new("groups")
        )
    )
    line_markup.add(
        types.InlineKeyboardButton(
            "Викладач",
            callback_data=query_type.new("teachers")
        )
    )
    return line_markup


def start_view() -> (str, types.InlineKeyboardMarkup):
    text = (
        "Привіт, я оновлена версія бота для розкладу. Для початку скажи "
        "мені хто ти:"
    )

    return text, query_type_markup()


def change_view() -> (str, types.InlineKeyboardMarkup):
    text = "Вибери для кого шукати розклад цього разу:"
    return text, query_type_markup()


async def about_view() -> str:
    bot_info = await bot.get_me()
    txt = (
        f"Бот для розкладу: @{bot_info.username}"
        f"\nGitHub:"
        f"https://github.com/thestd/schedule-BOT\nТехнічна підтримка:"
        f"[@skhortiuk] {emojize(':smiling_imp:')}"
    )
    return txt


def help_view() -> str:
    txt = "Допомога по командам:\n/start - \n/about - Інформація про " \
          "бота\n/help - " \
          "Допомога по " \
          "командам бота"
    return txt
