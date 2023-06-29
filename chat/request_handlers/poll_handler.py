import re
from connection_utils.socket_message import SocketMessage

from chat.request_handlers.handlers.start_session_request_handler import handle_start_session_request


def handle_poll_input(message: SocketMessage):
    print('kossher')
    print(message)
    if re.search('^start_session_request$', message.path):
        return handle_start_session_request(message)
