from app.core.misc import dp
from app.modules.admin.handlers import users_count, flush_cache

dp.register_message_handler(users_count, commands=["users_count"], state="*")
dp.register_message_handler(flush_cache, commands=["flush_cache"], state="*")
