from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import rsa


def generate_DH():
    params_numbers = dh.DHParameterNumbers(
        0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF,
        2,
    )
    parameters = params_numbers.parameters(default_backend())

    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    with open("_base/client_keys/private.dh.key.pem", "wb") as private_key_file:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_file.write(private_key_pem)

    with open("_base/client_keys/public.dh.key.pem", "wb") as public_key_file:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_file.write(public_key_pem)


def generate_rsa():
    (pubkey, privkey) = rsa.newkeys(8192, poolsize=4)

    PRIV_KEY_DST = '_base/client_keys/private.key'
    with open(PRIV_KEY_DST, 'wb+') as f:
        pk = rsa.PrivateKey.save_pkcs1(privkey, format='PEM')
        f.write(pk)

    PUB_KEY_DST = '_base/client_keys/public.key'
    with open(PUB_KEY_DST, 'wb+') as f:
        pk = rsa.PublicKey.save_pkcs1(pubkey, format='PEM')
        f.write(pk)


if __name__ == '__main__':
    generate_DH()
    generate_rsa()
