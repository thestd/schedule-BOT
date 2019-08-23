import os

TOKEN = os.environ.get("TOKEN", None)
SKIP_UPDATES = os.environ.get("SKIP_UPDATES", True)

CACHE_TIME = os.environ.get("CACHE_TIME", 6 * 3600)
REDIS_URL = os.environ.get("REDIS_URL", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

API_URL = os.environ.get("API_URL", "http://api.pnu-bot.pp.ua")

BASE_APP = __package__.split('.')[0]

MONGO_URL = "mongodb://root:example@localhost:27017"

modules = [
    "base",
    "schedule",
    "tail"
]
