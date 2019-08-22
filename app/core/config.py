import os

bot_token = os.environ.get("TOKEN", None)
skip_updates = os.environ.get("SKIP_UPDATES", True)
api_url = os.environ.get("API_URL", "http://api.pnu-bot.pp.ua")
base_app = __package__.split('.')[0]
cached_time = os.environ.get("CACHE_TIME", 6 * 3600)
redis_url = os.environ.get("REDIS_URL", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_db = int(os.environ.get("REDIS_DB", 0))
mongo_url = "mongodb://root:example@localhost:27017"
modules = [
    "base",
    "schedule",
    "tail"
]
