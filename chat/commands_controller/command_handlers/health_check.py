import rsa
from django.conf import settings

from ...utils import connection


def health_check():
    connection.send_encrypted(
        path='health_check', data='health check encrypted request', public_key=settings.SERVER_PUB,
    )
    return connection.receive()
