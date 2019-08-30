from app.core.misc import dp
from app.modules.schedule.handlers import query_type_register, \
    query_register, search_query, confirm_predicted_query,\
    manual_date_request, manual_date_response
from app.modules.schedule.consts import query_type, query_for_search, \
    query_predict
from app.modules.schedule.state import ScheduleState

dp.register_callback_query_handler(
    query_type_register,
    query_type.filter(),
    state=ScheduleState.query_type_register
)
dp.register_message_handler(query_register, state=ScheduleState.query_register)
dp.register_message_handler(
    query_register,
    state=ScheduleState.confirm_predicted_query
)
dp.register_callback_query_handler(
    confirm_predicted_query,
    query_predict.filter(),
    state=ScheduleState.confirm_predicted_query
)
dp.register_callback_query_handler(
    manual_date_request,
    lambda c: c["data"] == "manual_data",
    state=ScheduleState.schedule_search
)
dp.register_message_handler(
    manual_date_response,
    state=ScheduleState.manual_date
)
dp.register_callback_query_handler(
    search_query,
    query_for_search.filter(),
    state=ScheduleState.schedule_search
)
