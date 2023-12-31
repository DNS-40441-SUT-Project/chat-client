import threading
from typing import Optional

from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.utils import poll_connection, connection, validate_base_security_items


def handle_poll_connections():
    while True:
        # 4
        from chat.request_handlers import handle_poll_input
        message = poll_connection.recieve_decrypted(private_key=settings.PRIVATE_KEY)
        if not LoggedInUser.has_logged_in():
            break
        handler_result = handle_poll_input(message)
        if handler_result:
            print(handler_result)


class LoggedInUser:
    _logged_in_user: Optional['LoggedInUser'] = None
    _current_thread: threading.Thread

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
        validate_base_security_items(response)
        if response.body['status'] == '200':
            connection.send_encrypted(path='symmetric_key', headers=dict(authentication=dict(
                username=username,
                password=password
            )), public_key=settings.SERVER_PUB)
            message: SocketMessage = connection.recieve_decrypted(settings.PRIVATE_KEY)
            # validate_base_security_items(message)
            cls._logged_in_user = cls(username, password, message.body['symmetric_key'])
            cls._current_thread = threading.Thread(target=handle_poll_connections)
            cls._current_thread.start()
        else:
            raise cls.Exceptions.ServerError
        return response.body

    @classmethod
    def has_logged_in(cls):
        if cls._logged_in_user is None:
            return False
        return True

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
        cls._current_thread.join()

    @property
    def encoded_symmetric_key(self):
        return self._symmetric_key.encode('utf-8')

    def __init__(self, username: str, password: str, symmetric_key: str):
        self.username, self.password, self._symmetric_key = username, password, symmetric_key
