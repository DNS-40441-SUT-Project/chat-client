from datetime import datetime

from django.conf import settings

from chat.commands_controller.command_handlers.message_to import create_session_with_user
from chat.data import LoggedInUser
from chat.models import GroupSecret, UserSecret
from chat.utils import connection, validate_base_security_items
from chat.utils.defi_helman import DH_encrypt


def add_user_to_group(other_username, group_id):
    luser = LoggedInUser.get_logged_in_user()

    if UserSecret.objects.filter(other_user=other_username).exists():
        user_secret = UserSecret.objects.get(other_user=other_username)
    else:
        user_secret = create_session_with_user(luser, other_username)

    connection.send_encrypted(
        path='add_user_to_group',
        data=dict(
            other_username=other_username,
            group_id=group_id,
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            ),
        ),
        public_key=settings.SERVER_PUB,
    )
    message = connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)
    validate_base_security_items(message)
    if message.path == '200':
        secret = GroupSecret.objects.get(group=group_id)
        connection.send_sym_encrypted(
            path='group_secret',
            headers=dict(
                authentication=dict(
                    username=luser.username,
                    password=luser.password
                ),
                T=datetime.now().timestamp(),
            ),
            data=dict(
                M=DH_encrypt(secret.secret_key, user_secret.pub_key),
            ),
            symmetric_key=luser.encoded_symmetric_key,
        )
        message = connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)
        validate_base_security_items(message)
        if message.path == '200':
            return 'user has been add successfully!'

    return 'can not add member to group!'
