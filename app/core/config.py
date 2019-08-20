import os

bot_token = os.environ.get("TOKEN", None)
skip_updates = os.environ.get("SKIP_UPDATES", True)
api_url = os.environ.get("API_URL", "http://api.pnu-bot.pp.ua")
base_app = __package__.split('.')[0]
mongo_url = "mongodb://root:example@localhost:27017"
modules = [
    "base",
    "schedule",
    "tail"
]
