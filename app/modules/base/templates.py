from aiogram.utils.emoji import emojize

welcome_text = (
    f"Привіт! {emojize(':wave:')}"
    "\nЯ — твоя права рука під час навчального року,"
    " адже в мене ти завжди можеш дізнатись, які в тебе пари протягом тижня"
    f"{emojize(':smiling_imp:')}"

    f"\n\nДля початку, скажи мені хто ти{emojize(':smirk_cat:')}:"
)

about_text = (
    f"Бот, який створений, щоб спростити життя"
    f" студентам і не тільки {emojize(':wink:')}"

    f"\n\nБільше не потрібно використовувати застарілий і незрозумілий сайт, "
    f"щоб дізнатись, чи є завтра пари, доки можна поспати, а, можливо,"
    f" й прогуляти {emojize(':see_no_evil:')}"

    f"\n\nЩось не працює, "
    f"або знаєш як покращити мене?{emojize(':sunglasses:')}"
    # Todo: get admins of bot from environment
    f"\nНе соромся, пиши їм [@skhortiuk, @SchlafenderFox]."
    f"\nВони точно знають що з цим "
    f"робити{emojize(':smiling_imp:')}"

    f"\n\nНе забудь поставити свічку за здоров`я"
    f" моїх розробників{emojize(':innocent:')}"
)

choice_student_text = "Студент"
choice_teacher_text = "Викладач"

change_query_text = "Вибери для кого шукати розклад цього разу:"

help_text = (
    "Допомога по командам:\n/start - \n/about - Інформація про "
    "бота\n/help - "
    "Допомога по "
    "командам бота"
)
