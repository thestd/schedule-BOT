from app.core.misc import dp
from app.modules.base.handlers import cmd_start, cmd_about, cmd_help, \
    cmd_change_query

from app.modules.base.middleware import UserStorageMiddleware

dp.register_message_handler(cmd_start, commands=["start"])
dp.register_message_handler(cmd_change_query, commands=["change_query"])
dp.register_message_handler(cmd_about, commands=["about"])
dp.register_message_handler(cmd_help, commands=["help"])

dp.middleware.setup(UserStorageMiddleware())
