from cryptography.fernet import Fernet
from django.conf import settings
import base64


def get_shared_key_bytes(received_public_key):
    shared_key = settings.DH_PRIVATE_KEY.exchange(received_public_key)[:32]
    return base64.urlsafe_b64encode(shared_key)


def DH_decrypt(cipher_txt: str, received_public_key):
    shared_key_bytes = get_shared_key_bytes(received_public_key)
    cipher = Fernet(shared_key_bytes)
    return cipher.decrypt(cipher_txt).decode()


def DH_encrypt(message: str, received_public_key):
    shared_key_bytes = get_shared_key_bytes(received_public_key)
    cipher = Fernet(shared_key_bytes)
    return cipher.encrypt(message.encode())
