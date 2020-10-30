import cryptomath
import itertools
def good_random():
    q_ = cryptomath.choose_random_prime()
    p_ = cryptomath.choose_random_prime()
    q = 0
    p = 0
    for i in itertools.count(start=1):
        q = 2*i*q_+1
        p = 2*i*p_+1
        if cryptomath.miller_rabin(q) and cryptomath.miller_rabin(p):
            return (q,p)


def gen_p_q():
    q,p = good_random()
    while True:
        q1,p1 = good_random()
        if q*p <= q1*p1:
            return (q, p, q1, p1)

