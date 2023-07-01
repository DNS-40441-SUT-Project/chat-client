from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import LoggedInUser
from chat.models import UserSecret, GroupSecret
from chat.utils import poll_connection
from chat.utils.defi_helman import DH_decrypt


def handle_store_group_secret(message: SocketMessage):
    luser = LoggedInUser.get_logged_in_user()
    poll_connection.send_sym_encrypted(
        path='200',
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            ),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=luser.encoded_symmetric_key
    )
    new_message = poll_connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)
    user_secret = UserSecret.objects.get(other_user=new_message.body['sender_username'])
    group_secret_key = DH_decrypt(new_message.body['group_secret'], user_secret.pub_key)
    GroupSecret.unique_get_or_create(group=str(new_message.body['group']), secret=group_secret_key)
    print(f'you have been added to group {new_message.body["group"]}!')
