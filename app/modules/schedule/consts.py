from aiogram.utils.callback_data import CallbackData

query_type = CallbackData("query_type", "type")
search_query = CallbackData("search_query", "query_type", "query",
                            "week_date", "day_number")

week_days = {"Пн": 0, "Вт": 1, "Ср": 2, "Чт": 3, "Пт": 4, "Сб": 5, "Нд": 6}
