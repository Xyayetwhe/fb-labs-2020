import cryptomath
import itertools
dict_of_users = {}
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

def GenerateKeyPair(name_of_first_user,name_of_second_user):
    q, p, q1, p1 = gen_p_q()
    n = p*q
    euler_n = (p-1)*(q-1)
    e = pow(2,16)+1
    d = cryptomath.findModInverse(e,euler_n)
    data_of_first_user = {'public_key':(n,e),'private_key':d,'p_and_q':(p,q)}
    dict_of_users[name_of_first_user] = data_of_first_user

    n1 = p1*q1
    euler_n1 = (p1-1)*(q1-1)
    e1 = pow(2,16)+1
    d1 = cryptomath.findModInverse(e1,euler_n1)
    data_of_second_user = {'public_key':(n1,e1),'private_key':d1,'p_and_q':(p1,q1)}
    dict_of_users[name_of_second_user] = data_of_second_user



if __name__ == '__main__':
    GenerateKeyPair('tolik', 'yulya')
    message = 'attack at down'
    p,q = dict_of_users['tolik']['p_and_q']
    n,e = dict_of_users['tolik']['public_key']
    d = dict_of_users['tolik']['private_key']
    p1,q1 = dict_of_users['yulya']['p_and_q']
    n1,e1 = dict_of_users['yulya']['public_key']
    d1 = dict_of_users['yulya']['private_key']
    print("p пользователя A: {}".format(hex(p)))
    print("q пользователя A: {}".format(hex(q)))
    print("n пользователя A: {}".format(hex(n)))
    print("e пользователя A: {}".format(hex(e)))
    print("d пользователя A: {}".format(hex(d)))
    print("\n")
    print("p пользователя B: {}".format(hex(p1)))
    print("q пользователя B: {}".format(hex(q1)))
    print("n пользователя B: {}".format(hex(n1)))
    print("e пользователя B: {}".format(hex(e1)))
    print("d пользователя B: {}".format(hex(d1)))