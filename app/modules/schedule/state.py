from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ["ScheduleState"]


class ScheduleState(StatesGroup):
    query_type_register = State()
    query_register = State()
    schedule_search = State()
    manual_date = State()
