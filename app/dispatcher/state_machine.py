from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ["Schedule", ]


class Schedule(StatesGroup):
    user_reg = State()
    query_type = State()
    query = State()
    search = State()
