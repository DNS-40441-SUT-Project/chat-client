from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import LoggedInUser
from chat.exceptions import SecurityException
from chat.models import UserSecret, UserMessage
from chat.utils import poll_connection
from chat.utils.defi_helman import DH_decrypt


def handle_message_from_user(message: SocketMessage):
    luser = LoggedInUser.get_logged_in_user()

    if message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    poll_connection.send_sym_encrypted(
        path='establish_receive_message_connection',
        data=dict(
            T=datetime.now().timestamp(),
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        symmetric_key=luser.encoded_symmetric_key
    )

    new_message = poll_connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)

    if new_message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    poll_connection.send_sym_encrypted(
        path='receive_user_message_succeeded',
        data=dict(
            T=datetime.now().timestamp(),
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        symmetric_key=luser.encoded_symmetric_key
    )

    sender_username = new_message.body['from']
    user_secret = UserSecret.objects.get(other_user=sender_username)

    user_message = UserMessage.objects.create(
        sender=sender_username,
        receiver=luser.username,
        content=new_message.body['encrypted_M'],
    )
    decrypted_message = DH_decrypt(user_message.content, user_secret.pub_key)

    result = f'''
server: new received message from {sender_username}
start
---
{decrypted_message}
---
end
    '''

    return result
