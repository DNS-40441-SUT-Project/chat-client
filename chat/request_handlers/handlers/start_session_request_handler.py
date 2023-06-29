from datetime import datetime

from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.exceptions import SecurityException
from chat.utils import poll_connection
from chat.utils.defi_helman import DH_decrypt, DH_encrypt
from chat.utils.hash import sha1


def handle_start_session_request(message: SocketMessage):
    data = message.body
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    KA = data['KA']
    # 5
    M = 'M'
    KB = 'KB'
    poll_connection.send_encrypted(
        path='resume_session', data=dict(
            to=data['from'],
            KB=KB,
            T=datetime.now().timestamp(),
            M=M,
        ), public_key=settings.SERVER_PUB,
    )

    # 12
    message: SocketMessage = poll_connection.recieve_decrypted(settings.PRIVATE_KEY)
    data_12 = message.body
    if data_12['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    if data_12['from'] != data['from']:
        raise SecurityException()
    hash_m = DH_decrypt(data_12['encrypted_hash_m'], KA, KB)
    if sha1(M) != hash_m:
        raise SecurityException()

    # 13
    encrypted_m_prim = data_12['encrypted_m_prim']
    m_prim = DH_decrypt(encrypted_m_prim, KA, KB)
    hash_m_prim = sha1(m_prim)
    encrypted_hash_m_prim = DH_encrypt(hash_m_prim, KA, KB)

    print(vars(message))
    poll_connection.send_encrypted(
        path='resume_session', data=dict(
            to=data['from'],
            T=datetime.now().timestamp(),
            encrypted_hash_m_prim=encrypted_hash_m_prim,
        ), public_key=settings.SERVER_PUB,
    )
