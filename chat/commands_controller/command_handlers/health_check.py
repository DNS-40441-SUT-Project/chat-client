import rsa
from django.conf import settings

from ...utils import connection, poll_connection


def health_check():
    connection.send(
        path='health_check', data='health check request'
    )
    return connection.receive()


def health_check_enc():
    connection.send(
        path='health_check_enc', data=rsa.encrypt(
            'health check encrypted request'.encode(), pub_key=settings.SERVER_PUB
        )
    )
    return connection.receive()
