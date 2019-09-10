from app.core.misc import dp
from app.modules.admin.handlers import (
    users_count, flush_cache, get_user, msg_to_users, delete_msg,
    cmd_msg_to_users
)

dp.register_message_handler(users_count, commands=["users_count"], state="*")
dp.register_message_handler(flush_cache, commands=["flush_cache"], state="*")
dp.register_message_handler(get_user, commands=["get_user"], state="*")
dp.register_message_handler(
    cmd_msg_to_users,
    commands=["msg_to_users"],
    state="*"
)
dp.register_message_handler(msg_to_users, state="msg_to_send")
dp.register_callback_query_handler(
    delete_msg,
    lambda c: c.data == "delete_me",
    state="*"
)
