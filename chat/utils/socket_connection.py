import rsa
from connection_utils.socket_connections import ClientSocketConnection
from django.conf import settings


class ClientNormalSocket(ClientSocketConnection):
    _server_port = settings.SERVER_PORT
    my_private_key: rsa.PrivateKey = settings.PRIVATE_KEY
    your_public_key: rsa.PublicKey = settings.SERVER_PUB


class ClientPollSocket(ClientSocketConnection):
    _server_port = settings.POLL_PORT
    my_private_key: rsa.PrivateKey = settings.PRIVATE_KEY
    your_public_key: rsa.PublicKey = settings.SERVER_PUB


def create_connection(sender='anonymous'):
    conn = ClientNormalSocket.create_connection()
    conn.set_sender(sender)
    return conn


def create_poll_connection(sender='anonymous'):
    conn = ClientPollSocket.create_connection()
    conn.set_sender(sender)
    return conn


poll_connection = create_poll_connection()
connection = create_connection()
