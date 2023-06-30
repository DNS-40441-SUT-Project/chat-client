from .handle_logout import handle_logout
from chat.utils import poll_connection, connection


def exit_handler():
    handle_logout()
    connection.close()
    poll_connection.close()
    exit(0)
