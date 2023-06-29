from datetime import datetime

import rsa
from django.conf import settings

from chat.data import LoggedInUser
from chat.exceptions import SecurityException
from chat.models import UserSecret
from chat.utils import connection


def create_session_with_user(luser: LoggedInUser, other_user: str):
    # 1
    connection.send_encrypted(
        path='start_session', data=dict(
            to=other_user,
            T=datetime.now().timestamp(),
            KA='KA',
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ), public_key=settings.SERVER_PUB
    )
    # 8
    message = connection.recieve_decrypted(settings.PRIVATE_KEY)
    data = message.body
    if data['from'] != other_user:
        raise SecurityException()
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    KB = data['KB']
    print('Bye')

    # 9
    connection.send_encrypted()


def message_to_user(other_user: str, message: str):
    luser = LoggedInUser.get_logged_in_user()
    try:
        user_secret = UserSecret.objects.get(other_user=other_user)
    except UserSecret.DoesNotExist:
        create_session_with_user(luser, other_user)

    # TODO: message to user
