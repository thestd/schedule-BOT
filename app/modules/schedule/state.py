from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ["ScheduleState"]


class ScheduleState(StatesGroup):
    query_type_register = State()
    query_register = State()
    confirm_predicted_query = State()
    schedule_search = State()
