from connection_utils.socket_message import SocketMessage

from chat.utils import connection


def handle_start_session_request(message: SocketMessage):
    data = message.body
    connection.send_encrypted(
        path='resume_session', data=dict(
            to=data['from'],
            KB='KB',
            T=data['T'],
            M='M',
        )
    )
    connection.recieve_decrypted()
