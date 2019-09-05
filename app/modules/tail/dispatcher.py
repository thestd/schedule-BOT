from app.core.misc import dp
from app.modules.schedule.state import ScheduleState
from app.modules.tail.handlers import (
    invalid_msg, invalid_clb_data, old_callback
)

dp.register_message_handler(invalid_msg, state='*')
dp.register_callback_query_handler(
    old_callback,
    state=ScheduleState.schedule_search
)
dp.register_callback_query_handler(
    old_callback,
    state=ScheduleState.confirm_predicted_query
)
dp.register_callback_query_handler(invalid_clb_data, state='*')
