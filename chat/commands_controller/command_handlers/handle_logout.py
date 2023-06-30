from django.conf import settings

from chat.data import LoggedInUser
from chat.utils import connection, validate_base_security_items


def handle_logout():
    luser = LoggedInUser.get_logged_in_user()
    headers = dict()
    headers['authentication'] = dict(
        username=luser.username,
        password=luser.password
    )
    connection.send_encrypted('logout', public_key=settings.SERVER_PUB, headers=headers)
    message = connection.recieve_sym_decrypted(symmetric_key=luser.encoded_symmetric_key)
    validate_base_security_items(message)
    LoggedInUser.log_out()
    return 'logout was successful'
