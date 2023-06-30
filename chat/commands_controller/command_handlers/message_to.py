import hashlib
from datetime import datetime

from django.conf import settings

from chat.data import LoggedInUser
from chat.exceptions import SecurityException
from chat.models import UserSecret
from chat.utils import connection
from chat.utils.defi_helman import DH_decrypt, DH_encrypt
from chat.utils.hash import sha1


def create_session_with_user(luser: LoggedInUser, other_username: str):
    # 1
    KA = settings.DH_PUBLIC_KEY
    connection.send_encrypted(
        path='start_session',
        data=dict(
            to=other_username,
            T=datetime.now().timestamp(),
            KA=KA,
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        public_key=settings.SERVER_PUB,
    )
    # 8
    message = connection.recieve_sym_decrypted(luser.encode_symmetric_key)
    data = message.body
    if data['from'] != other_username:
        raise SecurityException()
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    KB = data['KB']
    encrypted_m = data['M']

    # 9
    M = DH_decrypt(encrypted_m, KA, KB)
    hash_m = sha1(M)
    encrypted_hash_m = DH_encrypt(hash_m, KA, KB)
    M_Prim = 'M_PRIM'
    encrypted_m_prim = DH_encrypt(M_Prim, KA, KB)
    connection.send_sym_encrypted(
        path='resume_session',
        data=dict(
            to=other_username,
            encrypted_hash_m=encrypted_hash_m,
            encrypted_m_prim=encrypted_m_prim,
            T=datetime.now().timestamp()
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ),
        symmetric_key=luser.encode_symmetric_key,
    )

    # 16
    message_16 = connection.recieve_sym_decrypted(symmetric_key=luser.encode_symmetric_key)
    data_16 = message_16.body
    if data_16['from'] != other_username:
        raise SecurityException()
    if data_16['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    encrypted_hash_m_prim = data_16['encrypted_hash_m_prim']
    hash_m_prim = DH_decrypt(encrypted_hash_m_prim, KA=KA, KB=KB)
    if hash_m_prim != sha1(M_Prim):
        raise SecurityException()
    return KA, KB


def message_to_user(other_username: str, message: str):
    luser = LoggedInUser.get_logged_in_user()
    try:
        user_secret = UserSecret.objects.get(other_user=other_username)
    except UserSecret.DoesNotExist:
        create_session_with_user(luser, other_username)

    # TODO: message to user
