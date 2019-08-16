__all__ = ["ItemError", "InvalidCode"]


class ItemError(Exception):
    pass


class InvalidCode(ItemError):
    pass
