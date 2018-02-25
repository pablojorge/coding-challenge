from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_OAEP

import requests


# See https://www.random.org/clients/http/
def fetch_random_ints(num, min, max):
    if max > 1000000000:
        raise Exception("max too large")

    print "Fetching %s integers in [%s, %s] from random.org" % (
        num,
        min,
        max
    )

    resp = requests.get(
        "https://www.random.org/integers/",
        params=dict(
            num=num,
            min=min,
            max=max,
            col=1,
            base=10,
            format="plain",
            rnd="new"
        )
    )

    if resp.status_code != 200:
        raise Exception("Unexpected status code: %s (%s)" % (
            resp.status_code,
            resp.text
        ))

    return [int(x)
            for x in resp.text.split('\n')
            if x]


def pooled_random_gen(pool_size):
    while True:
        pool = fetch_random_ints(pool_size, 0, 255)
        for byte in pool:
            yield chr(byte)


def reader(gen):
    def func(n):
        ret = reduce(lambda a, b: a + b, (gen.next() for x in range(n)))
        print "myrandom(%s): -> %s '%s'" % (n, len(ret), map(ord, ret))
        return ret
    return func


def gen_rsa_keypair(key_size):
    random_generator = reader(pooled_random_gen(128))
    priv = RSA.generate(key_size, random_generator)

    return priv, priv.publickey()


def rsa_encrypt(message, pub):
    cipher = PKCS1_OAEP.new(pub, SHA)
    return cipher.encrypt(message)


def rsa_decrypt(ciphertext, priv):
    cipher = PKCS1_OAEP.new(priv, SHA)
    return cipher.decrypt(ciphertext)


def main():
    priv, pub = gen_rsa_keypair(1024)

    message = "test message"
    ciphertext = rsa_encrypt(message, pub)
    decrypted = rsa_decrypt(ciphertext, priv)

    print "ciphertext:", map(ord, ciphertext)
    print "decrypted:", decrypted

    assert message == decrypted


if __name__ == '__main__':
    main()
