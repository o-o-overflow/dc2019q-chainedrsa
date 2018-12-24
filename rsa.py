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


def guess_d(n, e, lower_half_d, d, true_k):
    print "k, ", true_k
    for k in xrange(0, 2 * e):
        if (k * (n + 1) + 1) % e == 0:
            d0 = (k * (n + 1) + 1) / e
        else:
            d0 = (k * (n + 1) + 1) / e + 1
        print bin(abs(d0 - d))
        assert(abs(d0 - d) < 2 ** (n.bit_length() / 2))
        print d0.bit_length(), lower_half_d.bit_length()
        guessed_d = top_half(d0) + lower_half_d
        # print "l: ", bin(lower_half_d)
        # print "t: ", bin(top_half(d0))
        # print "g: ", bin(guessed_d)
        if verify(n, e, guessed_d, 'hello'):
            print "success"
            break
    print "fail"

def guess_d1(n, e, lower_half_d, d, true_k):
    k = true_k
    if (k * (n + 1) + 1) % e == 0:
        d0 = (k * (n + 1) + 1) / e
    else:
        d0 = (k * (n + 1) + 1) / e + 1
    print "bit length of delta: ", abs(d0 - d).bit_length()
    # if abs(d0 - d).bit_length() > 1000:
    #    import ipdb; ipdb.set_trace()
    print "bit length of n: ", n.bit_length()
    print "bit length of d: ", d.bit_length()
    assert(abs(d0 - d) < 2 ** (n.bit_length() / 2))
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
    print "d: ", bin(key.d)
    print "length of p: ", key.p.bit_length()
    print "length of q: ", key.q.bit_length()
    print "length of d: ", key.d.bit_length()
    e = key.e
    d = key.d
    kp = key.p
    kq = key.q
    k = (key.e * key.d - 1) / ((key.p - 1) * (key.q - 1))
    print "E: ", key.e
    print "MOD: ", (key.e * key.d - 1) % ((key.p - 1) * (key.q -
                                                            1))

    print "ERROR: ", (key.e * key.d - 1) - ((key.p - 1) * (key.q -
                                                         1)) * k

    import ipdb; ipdb.set_trace()
    d0 = (k * (key.n+1) + 1) / key.e
    delta = k * (key.p + key.q) / key.e
    print "error: ", key.d - d0 + delta
    print "length of delta: ", (abs(d0 - key.d)).bit_length()
    print "length of real delta: ", delta.bit_length()
    print "length of k: ", k.bit_length()
    print "length of e: ", key.e.bit_length()
    guess_d1(key.n, key.e, lower_half(key.d), key.d, k)

