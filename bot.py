import os
import ujson as json
from aiohttp import ClientSession
from typing import Union
from aioredis import RedisConnection, create_connection
from aiogram import Bot, types
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageNotModified, MessageCantBeDeleted
from aiogram.utils.callback_data import CallbackData
import asyncio
import uvloop
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import Executor
from aiogram.utils.emoji import emojize
from aiogram.utils import emoji
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from datetime import datetime, timedelta
# TOKEN = os.environ.get("TOKEN", None)
TOKEN='337899850:AAE1zz39Kp3XJVTXeYNg1CHu_Eqeojjcqfo'
SKIP_UPDATES = int(os.environ.get("SKIP_UPDATES", 1))
WEBHOOK_ENABLE = 0
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)
WEBHOOK_SERVER = {"host": os.environ.get("WEBHOOK_HOST", "0.0.0.0"),"port": int(os.environ.get("WEBHOOK_PORT", 80)),"webhook_path": os.environ.get("WEBHOOK_PATH", f"/{TOKEN}")}
CACHE_TIME = int(os.environ.get("CACHE_TIME", 6 * 3600))
REDIS_URL = os.environ.get("REDIS_URL", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
API_URL = os.environ.get("API_URL", "http://api.pnu-bot.pp.ua")
MONGO_URL = os.environ.get("MONGO_URL", "mongo")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
storage = MongoStorage(host=MONGO_URL, port=MONGO_PORT)
welcome_text = f"Привіт! {emojize(':wave:')}\nЯ — твоя права рука під час навчального року, адже в мене ти завжди можеш дізнатись, які в тебе пари протягом тижня {emojize(':smiling_imp:')}\n\nПотрібна допомога з командами? Просто відправ мені /help\n\nХочеш більше дізнатися про бота? Знаєш як його покращити? Щось пішло не так?\nВсю потрібну інформацію ти знайдеш натиснувши /about\n\nДля початку, скажи мені хто ти{emojize(':smirk_cat:')}:"
about_text = (
    f"Бот, який створений, щоб спростити життя студентам і не тільки {emojize(':wink:')}\n\nБільше не потрібно використовувати застарілий і незрозумілий сайт, "
    f"щоб дізнатись, чи є завтра пари, доки можна поспати, а, можливо, й прогуляти {emojize(':see_no_evil:')}\n\nЩось не працює, або знаєш як покращити мене?{emojize(':sunglasses:')}\nНе соромся, пиши їм [@skhortiuk, @SchlafenderFox]."
    f"\nВони точно знають що з цим робити{emojize(':smiling_imp:')}\nАле якщо ти впевнений в своїх силах{emojize(':muscle:')}, то ти завжди можеш зробити це сам {emojize(':computer:')} https://github.com/thestd/schedule-BOT"
    f"\n\nНе забудь поставити свічку за здоров`я моїх розробників{emojize(':innocent:')}")
student_welcome = f"Студент{emojize(':sunglasses:')}\n\nНапиши мені шифр твоєї групи (або ж його частину)."
teacher_welcome = f"Викладач{emojize(':sunglasses:')}\n\nВідправ мені своє прізвище, цього буде достатньо"
error_text = f"Виникла помилка, спробуй пізніше,або звернись в підтримку [@skhortiuk, @SchlafenderFox]"
today_text = "Сьогодні"
next_week_text = "Наступний тиждень"
previous_week_text = "Попередній тиждень"
manual_date_entry = "Ввести дату вручну"
enter_date_text = "Просто відправ мені дату в форматі `день.місяць.рік` (01.01.2019)"
error_date_text = "Схоже формат дати не зовсім вірний, спробуй ще раз\n\nПросто відправ мені дату в форматі `день.місяць.рік` (01.01.2019)"
no_lessons_text = "Вітаю, в тебе сьогодні відсутні пари!"
find_query = "Ось що вдалося знайти:"
cant_find_query = "Нічого не вдалось знайти, спробуй ще раз"
flood_text = f"Ну нічого собі, можеш натиснути дві кнопки менже ніж за 0.5 секунди. Ну молодець{emojize(':wink:')}"
choice_student_text,choice_teacher_text="Студент","Викладач"
change_query_text = "Вибери для кого шукати розклад цього разу:"
help_text = "Допомога по командам:\n/start - Для початку спілкування з ботом\n/change_query - Змінити запит\n/about - Інформація про бота\n/help - Допомога по командам бота"
query_type = CallbackData("q_type", "type")
query_for_search = CallbackData("search", "week_date", "day_number")
query_predict = CallbackData("predict", "query")
week_days_btn = {"Пн": 0, "Вт": 1, "Ср": 2, "Чт": 3, "Пт": 4, "Сб": 5, "Нд": 6}
week_days_full_name = {0: "Понеділок",1: "Вівторок",2: "Середа",3: "Четвер",4: "П'ятниця",5: "Субота",6: "Неділя",}
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)
        return cls._instances[cls]
class RedisCache:
    def __init__(self, url: str = REDIS_URL, port: int = REDIS_PORT,db: int = REDIS_DB):
        self._url = url
        self._port = port
        self._db_id = db
        self._redis: Union[RedisConnection, None] = None
    async def _get_redis(self) -> RedisConnection:
        if not isinstance(self._redis, RedisConnection):
            self._redis = await create_connection((self._url, self._port), db=self._db_id)
        return self._redis
    async def get_value(self, key: str) -> Union[None, str]:
        db = await self._get_redis()
        return await db.execute("get", key, encoding="utf-8")
    async def set_value(self, key: str, value: str, ex_time: int) -> None:
        db = await self._get_redis()
        await db.execute("set", key, value, "EX", ex_time)
class ServiceNotResponse(ConnectionError):
    pass
class ApiClient(metaclass=Singleton):
    def __init__(self, storage: RedisCache, url: str = API_URL):
        self._cache = storage
        self._api_url = url
        self._c = ClientSession()
    async def _make_request(self, pred_type: str, params: dict) -> dict:
        res = await self._cache.get_value(f"pred_type:{json.dumps(params)}")
        if not res:
            async with self._c.get(f"{self._api_url}/api/{pred_type}",params=params) as resp:
                if resp.status == 200:
                    res = await resp.json()
                else:
                    raise ServiceNotResponse(f"Code: {resp.status}")
            await self._cache.set_value(f"pred_type:{json.dumps(params)}",json.dumps(res), CACHE_TIME)
            return res
        else:
            return json.loads(res)
    async def name_predict(self, q_type: str, name: str) -> dict:
        return await self._make_request(f"{q_type}s", {"query": name})
    async def get_schedule(self, params: dict) -> dict:
        return await self._make_request("schedule", params)
class ClearBot(Bot):
    async def send_message(self, chat_id, *args,**kwargs) -> types.Message:
        res = await super(ClearBot, self).send_message(chat_id, *args,**kwargs)
        usr_data = await storage.get_data(chat=chat_id,user=chat_id)
        if "msg_to_delete" not in usr_data or not usr_data["msg_to_delete"]:
            await storage.update_data(chat=chat_id,user=chat_id,data={"msg_to_delete": [res.message_id]})
            return res
        for msg in usr_data["msg_to_delete"]:
            try:
                await self.delete_message(chat_id,msg)
            except MessageToDeleteNotFound:
                pass
        await storage.update_data(chat=chat_id,user=chat_id,data={"msg_to_delete": [res.message_id]})
        return res
uvloop.install()
loop = asyncio.get_event_loop()
api_client = ApiClient(RedisCache())
bot = ClearBot(token=TOKEN, loop=loop)
dp = Dispatcher(bot, storage=storage)
class ScheduleState(StatesGroup):
    query_type_register = State()
    query_register = State()
    confirm_predicted_query = State()
    schedule_search = State()
    manual_date = State()
def query_type_request(query_type: str) -> str:
    return student_welcome if query_type == "group" else teacher_welcome
def _generate_single_key(text: str, week_start_date: str,day_number: str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text,callback_data=query_for_search.new(week_start_date, day_number))
def generate_predict_view(values: list) -> (str, types.InlineKeyboardMarkup):
    markup = types.InlineKeyboardMarkup()
    for elem in values:
        markup.add(types.InlineKeyboardButton(elem,callback_data=query_predict.new(elem)))
    return find_query, markup
async def _generate_schedule_text(query: str,requested_day: str,schedule_data: dict,day_number: str) -> str:
    header = f"<strong>Розклад на {requested_day} ({week_days_full_name[int(day_number)]})\n{query}</strong>\n"
    lessons = schedule_data["schedule"]
    if not lessons:
        body = no_lessons_text
    else:
        stack = []
        for lesson in lessons:
            for detail in lesson["items"]:
                stack.append(f"<i>{detail['number']} пара ({detail['time_bounds']})</i>\n{detail['info']}")
        body = "\n\n".join(stack)
    return f"{header}\n{body}"
async def generate_search_view(query: str,query_type: str,requested_week: str,day_number: str) -> (str, types.InlineKeyboardMarkup):
    requested_week = datetime.strptime(requested_week, '%d.%m.%Y')
    curr_day = datetime.now()
    curr_first_week_day = curr_day - timedelta(days=curr_day.weekday())
    prev_week = (requested_week - timedelta(days=7)).strftime("%d.%m.%Y")
    next_week = (requested_week + timedelta(days=7)).strftime("%d.%m.%Y")
    requested_day = (requested_week + timedelta(days=int(day_number))).strftime("%d.%m.%Y")
    try:
        schedule_data = await api_client.get_schedule({query_type: query,"date_from": requested_day})
    except ServiceNotResponse:
        return error_text, None
    text = await _generate_schedule_text(query, requested_day, schedule_data,day_number)
    days_markup = []
    for day in week_days_btn:
        day_name = day
        if week_days_btn[day] == int(day_number):
            day_name = emoji.emojize(":black_circle:")
        days_markup.append(_generate_single_key(day_name,requested_week.strftime("%d.%m.%Y"),week_days_btn[day]))
    markup = types.InlineKeyboardMarkup(row_width=7)
    markup.add(*days_markup)
    markup.add(_generate_single_key(today_text,curr_first_week_day.strftime("%d.%m.%Y"),f"{curr_day.weekday()}"))
    markup.add(_generate_single_key(previous_week_text, prev_week, day_number),_generate_single_key(next_week_text, next_week, day_number),)
    markup.add(types.InlineKeyboardButton(manual_date_entry,callback_data="manual_data"))
    return text, markup
def query_type_markup() -> types.InlineKeyboardMarkup:
    line_markup = types.InlineKeyboardMarkup(row_width=2)
    line_markup.add(types.InlineKeyboardButton(choice_student_text,callback_data=query_type.new("group")))
    line_markup.add(types.InlineKeyboardButton(choice_teacher_text,callback_data=query_type.new("teacher")))
    return line_markup
async def cmd_start(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(chat_id=message.chat.id,text=welcome_text,reply_markup=query_type_markup(),parse_mode='HTML')
    await state.update_data(message.from_user.to_python())
    await ScheduleState.query_type_register.set()
async def cmd_change_query(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(chat_id=message.chat.id,text=change_query_text,reply_markup=query_type_markup(),parse_mode='HTML')
    await ScheduleState.query_type_register.set()
async def cmd_about(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(chat_id=message.chat.id,text=about_text,parse_mode='HTML')
async def cmd_help(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(chat_id=message.chat.id,text=help_text,parse_mode='HTML')
async def query_type_register(query: types.CallbackQuery, callback_data: dict,state: FSMContext):
    q_type = callback_data["type"]
    await bot.edit_message_text(text=query_type_request(q_type),chat_id=query.message.chat.id,message_id=query.message.message_id)
    await state.update_data(query_type=q_type)
    await ScheduleState.query_register.set()
async def query_register(message: types.Message, state: FSMContext):
    usr_data = await state.get_data()
    try:
        values = await api_client.name_predict(usr_data["query_type"],message.text)
    except ServiceNotResponse:
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(text=error_text,chat_id=message.chat.id,parse_mode='HTML')
        return
    await bot.delete_message(message.chat.id, message.message_id)
    if values:
        text, markup = generate_predict_view(values)
        await bot.send_message(text=text,chat_id=message.chat.id,reply_markup=markup,parse_mode='HTML')
        await ScheduleState.confirm_predicted_query.set()
    else:
        await bot.send_message(text=cant_find_query,chat_id=message.chat.id,parse_mode='HTML')
async def confirm_predicted_query(query: types.CallbackQuery,callback_data: dict, state: FSMContext):
    await state.update_data(query=callback_data["query"])
    usr_data = await state.get_data()
    curr_day = datetime.now()
    week_start_date = curr_day - timedelta(days=curr_day.weekday())
    text, markup = await generate_search_view(usr_data["query"],usr_data["query_type"],week_start_date.strftime("%d.%m.%Y"),str(curr_day.weekday()))
    await bot.edit_message_text(text=text,chat_id=query.message.chat.id,message_id=query.message.message_id,reply_markup=markup,parse_mode='HTML')
    await ScheduleState.schedule_search.set()
async def handler_throttled(message: types.CallbackQuery, **kwargs):
    await message.answer(flood_text, show_alert=True)
@dp.throttled(handler_throttled, rate=.5)
async def search_query(query: types.CallbackQuery, callback_data: dict,state: FSMContext):
    usr_data = await state.get_data()
    text, markup = await generate_search_view(usr_data["query"],usr_data["query_type"],callback_data["week_date"],callback_data["day_number"])
    try:
        await bot.edit_message_text(text=text,chat_id=query.message.chat.id,message_id=query.message.message_id,reply_markup=markup,parse_mode="HTML")
    except MessageNotModified:
        pass
    finally:
        await query.answer()
async def manual_date_request(callback_data: dict):
    await bot.delete_message(callback_data["message"]["chat"]["id"],callback_data["message"]["message_id"])
    await bot.send_message(chat_id=callback_data["message"]["chat"]["id"],text=enter_date_text,parse_mode="Markdown")
    await ScheduleState.manual_date.set()
async def manual_date_response(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id,message.message_id)
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await bot.send_message(chat_id=message.chat.id,text=error_date_text,parse_mode="Markdown")
        return
    curr_day = date
    week_start_date = curr_day - timedelta(days=curr_day.weekday())
    usr_data = await state.get_data()
    text, markup = await generate_search_view(usr_data["query"],usr_data["query_type"],week_start_date.strftime("%d.%m.%Y"),str(curr_day.weekday()))
    await bot.send_message(text=text,chat_id=message.chat.id,reply_markup=markup,parse_mode='HTML')
    await ScheduleState.schedule_search.set()
async def invalid_msg(message: types.Message, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        await bot.send_message(chat_id=message.chat.id,text=".",reply_markup=types.ReplyKeyboardRemove())
        await cmd_start(message, state)
        return
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except MessageCantBeDeleted:
        pass
async def invalid_clb_data(query: types.CallbackQuery, state: FSMContext):
    usr_state = await state.get_state()
    usr_data = await state.get_data()
    if not usr_state or not usr_data:
        await bot.send_message(chat_id=query.message.chat.id,text=".",reply_markup=types.ReplyKeyboardRemove())
        await cmd_start(query.message, state)
        return
    try:
        await bot.delete_message(query.message.chat.id,query.message.message_id)
    except MessageCantBeDeleted:
        pass
dp.register_message_handler(cmd_start, commands=["start"], state="*")
dp.register_message_handler(cmd_change_query, commands=["change_query"],state="*")
dp.register_message_handler(cmd_about, commands=["about"], state="*")
dp.register_message_handler(cmd_help, commands=["help"], state="*")
dp.register_callback_query_handler(query_type_register,query_type.filter(),state=ScheduleState.query_type_register)
dp.register_message_handler(query_register, state=ScheduleState.query_register)
dp.register_message_handler(query_register,state=ScheduleState.confirm_predicted_query)
dp.register_callback_query_handler(confirm_predicted_query,query_predict.filter(),state=ScheduleState.confirm_predicted_query)
dp.register_callback_query_handler(manual_date_request,lambda c: c["data"] == "manual_data",state=ScheduleState.schedule_search)
dp.register_message_handler(manual_date_response,state=ScheduleState.manual_date)
dp.register_callback_query_handler(search_query,query_for_search.filter(),state=ScheduleState.schedule_search)
dp.register_message_handler(invalid_msg, state='*')
dp.register_callback_query_handler(invalid_clb_data, state='*')
Executor(dp, skip_updates=SKIP_UPDATES).start_polling()