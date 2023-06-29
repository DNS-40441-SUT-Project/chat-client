from typing import Optional

from django.conf import settings

from chat.utils import poll_connection


class LoggedInUser:
    _logged_in_user: Optional['LoggedInUser'] = None

    class Exceptions:
        class AlreadyLoggedIn(Exception):
            def __init__(self):
                super().__init__('Already logged in')

        class NotLoggedIn(Exception):
            def __init__(self):
                super().__init__('Not logged in')

        class ServerError(Exception):
            def __init__(self):
                super().__init__('Server Error')

    @classmethod
    def login(cls, username: str, password: str):
        if cls._logged_in_user is not None:
            raise cls.Exceptions.AlreadyLoggedIn
        poll_connection.send_encrypted(path='login', data=dict(
            username=username,
            password=password,
        ), public_key=settings.SERVER_PUB)
        response = poll_connection.receive()
        if response.body['status'] == '200':
            cls._logged_in_user = cls(username, password)
        else:
            raise cls.Exceptions.ServerError
        return response

    @classmethod
    def get_logged_in_user(cls) -> 'LoggedInUser':
        if cls._logged_in_user is None:
            raise cls.Exceptions.NotLoggedIn
        return cls._logged_in_user

    @classmethod
    def log_out(cls):
        if cls._logged_in_user is None:
            raise cls.Exceptions.NotLoggedIn
        cls._logged_in_user = None

    def __init__(self, username: str, password: str):
        self.username, self.password = username, password
