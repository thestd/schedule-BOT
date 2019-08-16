from aiogram import types, Bot

from app.dispatcher.state_machine import Schedule

__all__ = ["cmd_start", "register_user", "query_init", ]


async def cmd_start(message: types.Message):
    bot = Bot.get_current()
    line_markup = types.InlineKeyboardMarkup(row_width=2)
    line_markup.add(types.InlineKeyboardButton("Студент",
                                               callback_data="group"))
    line_markup.add(types.InlineKeyboardButton("Викладач",
                                               callback_data="teacher"))
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id,
                           "Привіт, я оновлена версія бота для розкладу. Для "
                           "початку скажи мені хто ти:",
                           reply_markup=line_markup,
                           parse_mode='HTML')
    await Schedule.query_type.set()


async def register_user(callback_query, state):
    bot = Bot.get_current()
    await bot.edit_message_text("Готово. Тепер відправ мені запит:",
                                callback_query.message.chat.id,
                                callback_query.message.message_id)
    async with state.proxy() as data:
        data['query_type'] = callback_query.data
        data["msg"] = callback_query.message.message_id

    await Schedule.query.set()


async def query_init(message: types.Message, state):
    bot = Bot.get_current()
    async with state.proxy() as data:
        data["query"] = message.text
        await bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=7)
        markup.add(
            types.InlineKeyboardButton("пн", callback_data='1'),
            types.InlineKeyboardButton("вт", callback_data='2'),
            types.InlineKeyboardButton("ср", callback_data='3'),
            types.InlineKeyboardButton("чт", callback_data='4'),
            types.InlineKeyboardButton("пт", callback_data='5'),
            types.InlineKeyboardButton("сб", callback_data='6'),
            types.InlineKeyboardButton("нд", callback_data='7'),
        )
        markup.add(types.InlineKeyboardButton("return to today",
                                              callback_data='today'))
        markup.add(
            types.InlineKeyboardButton("next week", callback_data='n_week'),
            types.InlineKeyboardButton("previous week",
                                       callback_data='p_week'),
        )
        await bot.edit_message_text(f"<i>Розклад для {data['query']}</i>",
                                    chat_id=message.chat.id,
                                    reply_markup=markup,
                                    message_id=data["msg"],
                                    parse_mode='HTML')
        await Schedule.search.set()
