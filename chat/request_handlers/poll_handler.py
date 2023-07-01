import re
from connection_utils.socket_message import SocketMessage

from .handlers import *


def handle_poll_input(message: SocketMessage):
    if re.search('^start_session_request$', message.path):
        return handle_start_session_request(message)
    if re.search('^message_from_user$', message.path):
        return handle_message_from_user(message)
    if re.search('^group_secret$', message.path):
        return handle_store_group_secret(message)
