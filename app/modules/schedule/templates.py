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
manual_date_entry = "Ввести дату вручну"

enter_date_text = (
    "Просто відправ мені дату в форматі"
    " `день.місяць.рік` (01.01.2019)"
)
error_date_text = (
    "Схоже формат дати не зовсім вірний, спробуй ще раз"
    "\n\nПросто відправ мені дату в форматі"
    " `день.місяць.рік` (01.01.2019)"
)

no_lessons_text = "Вітаю, в тебе сьогодні вихідний!!"
find_query = "Ось що вдалося знайти:"
cant_find_query = "Нічого не вдалось знайти, спробуй ще раз"

flood_text = "Wow. Easy easy)"
