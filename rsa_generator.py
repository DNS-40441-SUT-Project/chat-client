import rsa


def main():
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
    main()
