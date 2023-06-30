import pickle

import rsa
from django.conf import settings


def verify_data(data, signature):
    try:
        rsa.verify(pickle.dumps(data), signature, settings.SERVER_PUB)
        return True
    except rsa.pkcs1.VerificationError:
        return False
