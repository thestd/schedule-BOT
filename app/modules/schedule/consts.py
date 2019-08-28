from aiogram.utils.callback_data import CallbackData

query_type = CallbackData("q_type", "type")
query_for_search = CallbackData("search", "week_date", "day_number")
query_predict = CallbackData("predict", "query")

week_days_btn = {"Пн": 0, "Вт": 1, "Ср": 2, "Чт": 3, "Пт": 4, "Сб": 5, "Нд": 6}
week_days_full_name = {
    0: "Понеділок",
    1: "Вівторок",
    2: "Середа",
    3: "Четвер",
    4: "П'ятниця",
    5: "Субота",
    6: "Неділя",
}
