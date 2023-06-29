import re
from connection_utils.socket_message import SocketMessage


def handle_poll_input(message: SocketMessage):
    print('kossher')
    print(message)
    if re.search('^start_session_request$', message.path):
        print('sag')
        return None
