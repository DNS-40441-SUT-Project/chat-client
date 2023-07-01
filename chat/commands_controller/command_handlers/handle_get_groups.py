from django.conf import settings

from chat.data import LoggedInUser
from chat.utils import connection, validate_base_security_items


def handle_get_groups():
    luser = LoggedInUser.get_logged_in_user()
    connection.send_encrypted(
        path='get_groups',
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
    return f'''
    ---groups:
    {message.body['results']}
    ---
        '''
