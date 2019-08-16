from app.bot.handlers import cmd_start, register_user, Schedule, \
    query_init


def add_handlers(dp):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_callback_query_handler(
        register_user, lambda c: c.data in ["group", "teacher"],
        state=Schedule.query_type
    )
    dp.register_message_handler(query_init, state=Schedule.query)
