from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import rsa


def generate_DH():

    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    with open("private.dh.key.pem", "wb") as private_key_file:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_file.write(private_key_pem)

    with open("public.dh.key.pem", "wb") as public_key_file:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_file.write(public_key_pem)


def generate_rsa():
    (pubkey, privkey) = rsa.newkeys(2048, poolsize=4)

    PRIV_KEY_DST = 'private.key'
    with open(PRIV_KEY_DST, 'wb+') as f:
        pk = rsa.PrivateKey.save_pkcs1(privkey, format='PEM')
        f.write(pk)

    PUB_KEY_DST = 'public.key'
    with open(PUB_KEY_DST, 'wb+') as f:
        pk = rsa.PublicKey.save_pkcs1(pubkey, format='PEM')
        f.write(pk)


if __name__ == '__main__':
    generate_DH()
    generate_rsa()
