from app.core.misc import dp
from app.modules.base.handlers import cmd_change_query, cmd_help, cmd_about
from app.modules.schedule.handlers import (
    query_type_register, query_register, search_query,
    manual_date_request, manual_date_response, shift_date, back_handler,
    confirm_predicted_query)
from app.modules.schedule.consts import (
    query_type, week_days_btn, date_navigate_btn,
    query_predict)
from app.modules.schedule.state import ScheduleState
from app.modules.schedule.templates import (
    manual_date_btn_entry, change_query_btn_text, help_btn_text, about_btn_text
)

dp.register_callback_query_handler(
    query_type_register,
    query_type.filter(),
    state=ScheduleState.query_type_register
)
dp.register_message_handler(
    query_register,
    state=ScheduleState.query_register
)
dp.register_callback_query_handler(
    confirm_predicted_query,
    query_predict.filter(),
    state=ScheduleState.confirm_predicted_query
)
dp.register_message_handler(
    manual_date_request,
    lambda c: c.text == manual_date_btn_entry,
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
    lambda m: m.text == change_query_btn_text,
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    cmd_help,
    lambda m: m.text == help_btn_text,
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    cmd_about,
    lambda m: m.text == about_btn_text,
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    manual_date_response,
    state=ScheduleState.manual_date
)
dp.register_callback_query_handler(
    back_handler,
    lambda c: c.data == "back",
    state="*"
)
