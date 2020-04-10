import os

import pytz

TOKEN = os.environ.get("TOKEN", None)
SKIP_UPDATES = int(os.environ.get("SKIP_UPDATES", 0))

WEBHOOK_ENABLE = int(os.environ.get("WEBHOOK_ENABLE", 0))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)
WEBHOOK_SERVER = {
    "host": os.environ.get("WEBHOOK_HOST", "0.0.0.0"),
    "port": int(os.environ.get("WEBHOOK_PORT", 80)),
    "webhook_path": os.environ.get("WEBHOOK_PATH", f"/{TOKEN}")
}

CACHE_TIME = int(os.environ.get("CACHE_TIME", 6 * 3600))
REDIS_URL = os.environ.get("REDIS_URL", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_URI = os.getenv("REDIS_URI")

API_URL = os.environ.get("API_URL", "http://api.pnu-bot.pp.ua")

BASE_APP = __package__.split('.')[0]

MONGO_URL = os.environ.get("MONGO_URL", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PSWD = os.getenv("MONGO_PSWD")
MONGO_DB = os.getenv("MONGO_DB", "aiogram_fsm")

ADMIN_IDS = [int(i) for i in os.environ.get("ADMIN_IDS", "").split()]

TIME_ZONE = pytz.timezone('Europe/Kiev')

modules = [
    "base",
    "admin",
    "schedule",
    "tail"
]
