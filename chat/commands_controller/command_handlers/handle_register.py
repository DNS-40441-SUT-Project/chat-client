import pickle
from datetime import datetime

import rsa
from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.exceptions import SecurityException
from chat.utils import connection
from chat.utils.hash import sha1


def handle_register(username, password):
    connection.send_encrypted(path='register', data=dict(
        username=username,
        password=password,
        T=datetime.now().timestamp(),
    ), public_key=settings.SERVER_PUB)
    response: SocketMessage = connection.receive()
    sign = response.headers['sign']
    try:
        rsa.verify(pickle.dumps(response.body), sign, settings.SERVER_PUB)
    except rsa.pkcs1.VerificationError:
        return 'Verification failed'

    if response.body['status'] != '200':
        raise Exception("Invalid Register")
    if response.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    connection.send_encrypted(path='set_public_key', data=dict(username=username, T=datetime.now().timestamp(), ),
                              public_key=settings.SERVER_PUB)
    connection.receive()
    connection.send(path='set_public_key', data=dict(public_key=settings.PUBLIC_KEY))

    message: SocketMessage = connection.recieve_decrypted(settings.PRIVATE_KEY)
    if message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    M = message.body['M']
    hash_M = sha1(M)
    connection.send_encrypted(path='set_public_key', data=dict(hash_M=hash_M, T=datetime.now().timestamp()),
                              public_key=settings.SERVER_PUB)
    message: SocketMessage = connection.recieve_decrypted(settings.PRIVATE_KEY)
    if message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    if message.body['status'] != '200':
        raise Exception("Invalid Set Public Key")
    return "register completed"
