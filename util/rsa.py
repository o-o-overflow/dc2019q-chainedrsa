from Crypto.PublicKey import RSA
import math

def verify(n, e, d, m):
    # print e, d n
    if (e * d) % n != 1:
        return False
    else:
        guessed_rsa = RSA.construct((n, e, d))
        encrypted = guessed_rsa.encrypt(m)
        guessed_m = guessed_rsa.decrypt(encrypted)
        return guessed_m == m


def guess_d(n, e, lower_half_d, d, g):
    for k in xrange(0, e * g):
        # kk = k / g
        if (k * (n + 1) + 1) % (e * g) == 0:
            d0 = (k * (n + 1) + 1) / (e * g)
        else:
            d0 = (k * (n + 1) + 1) / (e * g) + 1
        # print bin(abs(d0 - d))
        # print d0.bit_length(), lower_half_d.bit_length()
        guessed_d = top_half(d0) + lower_half_d
        # print "l: ", bin(lower_half_d)
        # print "t: ", bin(top_half(d0))
        # print "g: ", bin(guessed_d)
        if verify(n, e, guessed_d, 'hello'):
            print "success"
            break
    print "fail"


def guess_d1(n, e, lower_half_d, d, key):
    # k = (key.e * key.d - 1) / ((key.p - 1) * (key.q - 1) * g)
    d0 = ((key.e * key.d - 1) * (n + 1) / ((key.p - 1) * (key.q - 1) * g)+ 1) / e
    print "bit length of delta: ", abs(d0 - d).bit_length()
    # if abs(d0 - d).bit_length() > 1000:
    #    import ipdb; ipdb.set_trace()
    print "bit length of n: ", n.bit_length()
    print "bit length of d: ", d.bit_length()
    print "bit length of d0: ", d0.bit_length()
    # assert(abs(d0 - d) < 2 ** (n.bit_length() / 2))
    print d0.bit_length(), lower_half_d.bit_length()
    guessed_d = top_half(d0) + lower_half_d
    # print "l: ", bin(lower_half_d)
    # print "t: ", bin(top_half(d0))
    # print "g: ", bin(guessed_d)

def lower_half(d):
    bit_length = d.bit_length()
    return d & (2 ** (bit_length / 2) - 1)

def top_half(d):
    bit_length = d.bit_length()
    half_bit_length = bit_length / 2
    return d >> half_bit_length << half_bit_length


def gcd(a, b):
    while b:
       a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)

if __name__ == '__main__':
    key = RSA.generate(1024, e=65537)
    g = gcd(key.p - 1, key.q - 1)
    print "g: ", g
    # guess_d(key.n, key.e, lower_half(key.d), key.d, g)
    guess_d1(key.n, key.e, lower_half(key.d), key.d, key)
