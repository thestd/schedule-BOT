from aiogram.utils.callback_data import CallbackData

query_type = CallbackData("q_type", "type")
query_for_search = CallbackData("search", "week_date", "day_number")
query_predict = CallbackData("predict", "name")

week_days = {"Пн": 0, "Вт": 1, "Ср": 2, "Чт": 3, "Пт": 4, "Сб": 5, "Нд": 6}
