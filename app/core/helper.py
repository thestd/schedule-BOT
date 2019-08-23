from app.core.config import modules, BASE_APP


def module_loader():
    """
    Loads dispatcher from each app module
    """
    for module in modules:
        __import__(f"{BASE_APP}.modules.{module}.dispatcher")
