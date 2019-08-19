import os

bot_token = os.environ.get("TOKEN", None)
skip_updates = os.environ.get("SKIP_UPDATES", True)
base_app = __package__.split('.')[0]
modules = [
    'base',
    'schedule'
]
