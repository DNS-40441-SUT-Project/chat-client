from django.conf import settings

from chat.data import LoggedInUser
from chat.utils import connection, validate_base_security_items


def get_online_users():
    luser = LoggedInUser.get_logged_in_user()
    connection.send_encrypted(
        path='get_online_users',
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        public_key=settings.SERVER_PUB,)
    message = connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)
    validate_base_security_items(message)
    return f'''
---all users:
{message.body['results']}
---
    '''
