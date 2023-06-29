from datetime import datetime

from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.exceptions import SecurityException
from chat.utils import poll_connection


def handle_start_session_request(message: SocketMessage):
    data = message.body
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    # 5
    poll_connection.send_encrypted(
        path='resume_session', data=dict(
            to=data['from'],
            KB='KB',
            T=datetime.now().timestamp(),
            M='M',
        ), public_key=settings.SERVER_PUB,
    )

    # 12
    poll_connection.recieve_decrypted()
