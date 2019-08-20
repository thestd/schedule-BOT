from app.core.config import modules, base_app


def load_modules():
    for module in modules:
        __import__(f"{base_app}.modules.{module}.dispatcher")
