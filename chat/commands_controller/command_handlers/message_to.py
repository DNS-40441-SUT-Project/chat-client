import hashlib
from datetime import datetime

from django.conf import settings

from chat.data import LoggedInUser
from chat.exceptions import SecurityException
from chat.models import UserSecret
from chat.utils import connection
from chat.utils.defi_helman import DH_decrypt, DH_encrypt
from chat.utils.hash import sha1


def create_session_with_user(luser: LoggedInUser, other_user: str):
    # 1
    KA = 'KA'
    connection.send_sym_encrypted(
        path='start_session', data=dict(
            to=other_user,
            T=datetime.now().timestamp(),
            KA=KA,
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ), symmetric_key=LoggedInUser.get_logged_in_user().encode_symmetric_key
    )
    # 8
    message = connection.recieve_sym_decrypted(LoggedInUser.get_logged_in_user().encode_symmetric_key)
    data = message.body
    if data['from'] != other_user:
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
        path='resume_session', data=dict(
            to=other_user,
            encrypted_hash_m=encrypted_hash_m,
            encrypted_m_prim=encrypted_m_prim,
            T=datetime.now().timestamp()
        ),
        headers=dict(
            authentication=dict(
                username=luser.username,
                password=luser.password
            )
        ), symmetric_key=LoggedInUser.get_logged_in_user().encode_symmetric_key
    )


def message_to_user(other_user: str, message: str):
    luser = LoggedInUser.get_logged_in_user()
    try:
        user_secret = UserSecret.objects.get(other_user=other_user)
    except UserSecret.DoesNotExist:
        create_session_with_user(luser, other_user)

    # TODO: message to user
