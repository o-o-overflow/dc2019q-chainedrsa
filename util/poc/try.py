import time, random, math
from Crypto.PublicKey import RSA

MAX_G = 100

def lower_half(d):
    half_bit_length = d.bit_length() / 2
    return d & ((1 << half_bit_length) - 1)


def upper_half(n):
    half_bit_length = n.bit_length() / 2
    return n >> half_bit_length


def gcd(a, b):
    while b:
       a, b = b, a % b
    return a


def lcm(a, b):
    return a * b / gcd(a, b)


class Key(object):
    def __init__(self, library=False, hard=False, input=None):
        if input is not None:
            with open(input, 'r') as f:
                line = f.readline()
                words = line.strip().split(',')
                [p, q, e, d] = map(int, words[:4])
                self.p = p
                self.q = q
                self.n = p * q
                self.e = e
                self.d = d
        elif library:
            if hard:
                k = RSA.generate(1024, e=65537)
                g = gcd(k.p-1, k.q-1)
                while g < 10 or g > MAX_G:
                    k = RSA.generate(1024, e=65537)
                self.p = k.p
                self.q = k.q
                self.n = k.n
                self.e = k.e
                self.d = k.d
            else:
                k = RSA.generate(1024, e=65537)
                self.p = k.p
                self.q = k.q
                self.n = k.n
                self.e = k.e
                self.d = k.d
        else:
            self.p = 61
            self.q = 53
            self.n = self.p * self.q
            self.e = 17
            self.d = 413
        self.g = gcd(self.p-1, self.q-1)
        self.k = (self.e * self.d - 1) / lcm(self.p-1, self.q-1)
        self.ld = lower_half(self.d)

    def __str__(self):
        p = 'p: %d' % self.p
        q = 'q: %d' % self.q
        e = 'e: %d' % self.e
        d = 'd: %s' % bin(self.d)
        g = 'g: %d' % self.g
        k = 'k: %d' % self.k

        return '\n'.join([p, q, e, d, g, k])

    def check_d0(self):
        d0 = (self.k * (self.n + 1) + self.g) / (self.e * self.g)
        print d0 - self.d
        print "k: ", self.k
        print "e: ", self.e
        print "g: ", self.g
        print "lcm: ", lcm(self.p-1, self.q-1)
        print "d0: ", bin(d0)
        print "d : ", bin(self.d)
        if d0 - self.d < 2 ** (self.d.bit_length() / 2):
            print "warning: the difference is greater than 2 ** (self.d.bit_length() / 2)"
        assert d0 - self.d < 2 ** (self.d.bit_length() / 2 + 1)

    def is_sqrt(self, n):
        # This is an efficient sqrt
        x = n
        y = (x + 1) // 2
        while y < x:
            x = y
            y = (x + n // x) // 2
        return x ** 2 == n

    def test(self, d, e, n, g, k):
        # One way is to test with a msg. But it can be very slow
        # due to exponentiation. So we use sqrt trick with a filter.
        # This improves performance by avoiding sqrt
        if (d * e - 1) % k != 0:
        # if (d * e - 1) % g != 0 or (d * e - 1) % k != 0:
            return False
        phi = (d * e - 1) * g / k
        sum_pq = n + 1 - phi
        if sum_pq != n+1 and self.is_sqrt(sum_pq ** 2 - 4 * n):
            return True
        else:
            return False

    def guess(self):
        g = 1
        while True:
            # This improves performance
            if (self.n - 1) % g > 0:
                g += 1
                continue
            print "Guessing g =", g
            for k in xrange(1, g * self.e):
                # This improves performance
                if gcd(k, g) > 1 : continue
                d0 = (k * (self.n+1) + g) / (self.e * g)
                dd0 = upper_half(d0)
                bits = self.d.bit_length() / 2
                d = (dd0 << bits) + self.ld
                d_minus = (dd0 - 1 << bits) + self.ld
                # d0 may carry 1, e.g. n = 61 * 53, e = 17, d = 413
                if self.test(d, self.e, self.n, g, k):
                    return d
                if self.test(d_minus, self.e, self.n, g, k):
                    return d_minus
            g += 1
            if g > MAX_G:
                return None


def work():
    key = Key(library=True, hard=True, input='case4')
    # key = Key(library=True, hard=True)
    print key
    t_start = time.time()
    res = key.guess()
    t_end = time.time()
    if res == key.d:
        print "Succeed, time: %f" % (t_end - t_start)
        with open('finished', 'a') as f:
            f.write('%d, %d, %d, %d, %d, %f\n' %\
                    (key.p, key.q, key.e, key.d, key.g,\
                     t_end - t_start))
    else:
        with open('error', 'a') as f:
            f.write('%d, %d, %d, %d, %d\n' %(key.p, key.q, key.e,\
                                           key.d, key.g))


def batch():
    for _ in xrange(100):
        work()

if __name__ == '__main__':
    # batch()
    work()
