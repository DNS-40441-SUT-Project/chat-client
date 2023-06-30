from datetime import datetime

from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.data import LoggedInUser
from chat.exceptions import SecurityException
from chat.utils import poll_connection
from chat.utils.defi_helman import DH_decrypt, DH_encrypt
from chat.utils.hash import sha1


def handle_start_session_request(message: SocketMessage):
    data = message.body
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    KA = data['KA']
    M = 'M'
    KB = 'KB'
    luser = LoggedInUser.get_logged_in_user()

    # 5
    poll_connection.send_sym_encrypted(
        path='resume_session',
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        data=dict(
            to=data['from'],
            KB=KB,
            T=datetime.now().timestamp(),
            M=M,
        ), symmetric_key=luser.encode_symmetric_key,
    )

    # 12
    message: SocketMessage = poll_connection.recieve_sym_decrypted(
        luser.encode_symmetric_key)
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

    poll_connection.send_sym_encrypted(
        path='resume_session',
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        data=dict(
            to=data['from'],
            T=datetime.now().timestamp(),
            encrypted_hash_m_prim=encrypted_hash_m_prim,
        ),
        symmetric_key=luser.encode_symmetric_key,
    )
