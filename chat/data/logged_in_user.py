from enum import Enum
from typing import Optional


class LoggedInUser:
    _logged_in_user: Optional['LoggedInUser'] = None

    class Exceptions(Enum):
        ALREADY_LOGGED_IN = type('ALREADY_LOGGED_IN', bases=(Exception,))
        NOT_LOGGED_IN = type('NOT_LOGGED_IN', bases=(Exception,))

    @classmethod
    def login(cls, username: str, password: str):
        if cls._logged_in_user is not None:
            raise cls.Exceptions.ALREADY_LOGGED_IN
        cls._logged_in_user = cls(username, password)

    @classmethod
    def get_logged_in_user(cls) -> 'LoggedInUser':
        if cls._logged_in_user is None:
            raise cls.Exceptions.NOT_LOGGED_IN
        return cls._logged_in_user

    @classmethod
    def log_out(cls):
        if cls._logged_in_user is None:
            raise cls.Exceptions.NOT_LOGGED_IN
        cls._logged_in_user = None

    def __init__(self, username: str, password: str):
        self.username, self.password = username, password
