from datetime import datetime

from connection_utils.socket_message import SocketMessage

from .signature import verify_data
from chat.exceptions import SecurityException


def validate_base_security_items(message: SocketMessage):
    is_verified = verify_data(message.headers['signature_value'], message.headers['signature'])

    if not is_verified:
        raise SecurityException

    if message.headers['T'] - datetime.now().timestamp() > 10:
        raise SecurityException
