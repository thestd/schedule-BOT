import os

TOKEN = os.environ.get("TOKEN", None)
SKIP_UPDATES = int(os.environ.get("SKIP_UPDATES", 1))

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

API_URL = os.environ.get("API_URL", "http://api.pnu-bot.pp.ua")

BASE_APP = __package__.split('.')[0]

MONGO_URL = os.environ.get("MONGO_URL", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))

MIX_PANEL_TOKEN = os.environ.get("MIX_PANEL_TOKEN", None)

modules = [
    "base",
    "schedule",
    "tail"
]
