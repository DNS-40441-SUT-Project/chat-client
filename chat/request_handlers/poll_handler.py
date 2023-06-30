import re
from connection_utils.socket_message import SocketMessage

from .handlers import handle_start_session_request, handle_message_from_user


def handle_poll_input(message: SocketMessage):
    if re.search('^start_session_request$', message.path):
        return handle_start_session_request(message)
    if re.search('^message_from_user$', message.path):
        return handle_message_from_user(message)
