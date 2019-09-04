from app.core.misc import dp
from app.modules.base.handlers import cmd_change_query, cmd_help, cmd_about
from app.modules.schedule.handlers import query_type_register, \
    query_register, search_query, confirm_predicted_query, \
    manual_date_request, manual_date_response, shift_date
from app.modules.schedule.consts import query_type, query_for_search, \
    query_predict, week_days_btn, date_navigate_btn
from app.modules.schedule.state import ScheduleState

dp.register_callback_query_handler(
    query_type_register,
    query_type.filter(),
    state=ScheduleState.query_type_register
)
dp.register_message_handler(
    query_register,
    state=ScheduleState.query_register
)
dp.register_message_handler(
    confirm_predicted_query,
    state=ScheduleState.confirm_predicted_query
)
dp.register_message_handler(
    manual_date_request,
    lambda c: c.text == "Ввести дату вручну",
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    shift_date,
    lambda m: m.text in date_navigate_btn,
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    search_query,
    lambda m: m.text in week_days_btn,
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    cmd_change_query,
    lambda m: m.text == "Змінити запит",
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    cmd_help,
    lambda m: m.text == "Допомога",
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    cmd_about,
    lambda m: m.text == "Про бота",
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    manual_date_response,
    state=ScheduleState.manual_date
)
