from cryptography.fernet import Fernet
from django.conf import settings

from chat.data import LoggedInUser
from chat.models import GroupSecret
from chat.utils import connection, validate_base_security_items


def handle_create_group(group_name):
    luser = LoggedInUser.get_logged_in_user()
    connection.send_encrypted(
        path='create_group',
        data=dict(
            group_name=group_name,
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        public_key=settings.SERVER_PUB,
    )
    message = connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)
    validate_base_security_items(message)
    GroupSecret.objects.create(
        group=str(message.path),
        secret_key=Fernet.generate_key(),
    )
    return 'group created successfully'
