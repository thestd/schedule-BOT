from aiogram.utils.emoji import emojize

student_welcome = (
    f"Студент{emojize(':sunglasses:')}"
    "\n\nНапиши мені шифр твоєї групи (або ж його частину)."
)

teacher_welcome = (
    f"Викладач{emojize(':sunglasses:')}"
    "\n\nВідправ мені своє прізвище, цього буде достатньо"
)

error_text = (
    f"Виникла помилка, спробуй пізніше,"
    # Todo: get admins of bot from environment
    f"або звернись в підтримку [@skhortiuk, @SchlafenderFox]"
)

today_text = "Сьогодні"
next_week_text = "Наступний тиждень"
previous_week_text = "Попередній тиждень"
manual_date_btn_entry = "Ввести дату вручну"
change_query_btn_text = "Змінити запит"
help_btn_text = "Допомога"
about_btn_text = "Про бота"

enter_date_text = (
    "Просто відправ мені дату в форматі"
    " `день.місяць.рік` (01.01.2019)"
)
error_date_text = (
    "Схоже формат дати не зовсім вірний, спробуй ще раз"
    "\n\nПросто відправ мені дату в форматі"
    " `день.місяць.рік` (01.01.2019)"
)

no_lessons_text = "Вітаю, в тебе сьогодні вихідний!"
find_query = "Ось що вдалося знайти:"
to_many_query_find = (
    "Мені довелось обмежити кількість результатів до 100.\n"
)
cant_find_query = "Нічого не вдалось знайти, спробуй ще раз"

flood_text = (
    f"Ну нічого собі, можеш натиснути на кнопку двічі за 0.5 секунди. "
    f"В тебе, напевно, найшвидша рука на Дикому Заході{emojize(':smirk:')}"
)
