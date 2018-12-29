# This script is to generate hard keys to directlry keys_bak/
from Crypto.PublicKey import RSA
FLAG_LENGTH = 30
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def work(i):
    key = None
    while True:
        key = RSA.generate(2048, e=65537)
        g = gcd(key.p - 1, key.q - 1)
        k = (key.e * key.d - 1) / lcm(key.p - 1, key.q - 1)
        # if g > 2 and gcd(g, k) == 1:
        if g > 10 and g < 30 and gcd(g, k) == 1:
            print('g: %d, k: %d' % (g, k))
            break
    # write private key
    priv = key.exportKey('PEM')
    pub = key.publickey().exportKey('PEM')
    with open('keys_bak1/%d.pub' % i, 'w') as f:
        f.write(pub)
    with open('keys_bak1/%d.pem' % i, 'w') as f:
        f.write(priv)


if __name__ == '__main__':
    for i in range(700):
        print("generating %d" % i)
        work(i)
