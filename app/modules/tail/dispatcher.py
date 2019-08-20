from app.core.misc import dp
from app.modules.schedule.consts import query_type
from app.modules.tail.handlers import invalid_msg, invalid_clb_data

dp.register_message_handler(invalid_msg, state='*')
dp.register_callback_query_handler(invalid_clb_data,
                                   query_type.filter(), state='*')
