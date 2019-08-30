from app.core.config import MIX_PANEL_TOKEN
from app.core.misc import dp
from app.modules.base.handlers import cmd_start, cmd_about, cmd_help, \
    cmd_change_query
from app.modules.base.middlewares import StatisticMiddleware

dp.register_message_handler(cmd_start, commands=["start"], state="*")
dp.register_message_handler(cmd_change_query, commands=["change_query"],
                            state="*")
dp.register_message_handler(cmd_about, commands=["about"], state="*")
dp.register_message_handler(cmd_help, commands=["help"], state="*")

if MIX_PANEL_TOKEN:
    dp.middleware.setup(StatisticMiddleware())
