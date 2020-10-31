import cryptomath
import itertools
import random
dict_of_users = {}
def good_random(info_for_report=False):
    q_ = cryptomath.choose_random_prime(info_for_report="q'")
    p_ = cryptomath.choose_random_prime(info_for_report="p'")
    q = 0
    p = 0
    for i in itertools.count(start=1):
        q = 2*i*q_+1
        p = 2*i*p_+1
        if cryptomath.miller_rabin(q) and cryptomath.miller_rabin(p):
            return (q,p)
        if info_for_report: print("кандидати на ролі {} {} {} не пройшли через те,що завалили тест Міллера–Рабіна".format(info_for_report,hex(q),hex(p)))



def gen_p_q(info_for_report=False):
    q,p = good_random("q и p")
    while True:
        q1,p1 = good_random("q1 и p1")
        if q*p <= q1*p1:
            return (q, p, q1, p1)
        if info_for_report:
            print("q1 и p1 {} {} не пройшли так як q*p>q1*pi".format(hex(q1),hex(p1)))

def GenerateKeyPair(name_of_first_user,name_of_second_user):
    q, p, q1, p1 = gen_p_q(info_for_report=True)
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
    dict_of_users[name_of_second_user] = data_of_second_user
    dict_of_users[name_of_first_user]['reviced_keys'] = {}
    dict_of_users[name_of_second_user]['reviced_keys'] = {}
    dict_of_users[name_of_first_user]['verified_keys'] = {}
    dict_of_users[name_of_second_user]['varified_keys'] = {}


def Encrypt(m,e,n):
    m = list(bytes(m.encode('ascii')))
    m = '0x'+''.join(list(map(lambda x: hex(x)[2:],m)))
    print("чисельне значення ВТ {}".format(m))
    m = int(m,16)
    if m > n:
        return None
    return hex(pow(m,e,n))


def Decrypt(c,d,n):
    print("чисельне значення ШТ {}".format(c))
    c = int(c,16)
    m = pow(c,d,n)
    m = hex(m)[2:]
    m = [m[i:i+2] for i in range(0,len(m),2)]
    m = ''.join(list(map(lambda x: chr(int(x,16)),m)))
    return m


def Sign(m,d,n):
    orig_msg = m
    s = Encrypt(m,d,n)
    return (orig_msg,s)

def Verify(m,s,e,n):
    m = list(bytes(m.encode('ascii')))
    m = '0x'+''.join(list(map(lambda x: hex(x)[2:],m)))
    return m == hex(pow(int(s,16),e,n))

def SendKey(sender,reciver):
    print("Процедура SendKey")
    n,e = dict_of_users[sender]['public_key']
    print("n={}".format(hex(n)))
    print("e={}".format(hex(e)))
    k = random.randint(1,n-1)
    print("k={}".format(k))
    n1,e1 = dict_of_users[reciver]['public_key']
    print("n1={}".format(hex(n1)))
    print("e1={}".format(hex(e1)))
    k1 = pow(k,e1,n1)
    print("k1={}".format(hex(k1)))
    d = dict_of_users[sender]['private_key']
    print("d={}".format(hex(d)))
    s = pow(k,d,n)
    print("s={}".format(hex(s)))
    s1 = pow(s,e1,n1)
    print("s1={}".format(hex(s1)))
    dict_of_users[reciver]['reviced_keys'][sender] = [k1,s1]


def ReceiveKey(sender,reciver):
    print("процедура ReciveKey")
    k1,s1 = dict_of_users[reciver]['reviced_keys'][sender]
    print("k1={}".format(hex(k1)))
    print("s1={}".format(hex(s1)))
    n1 = dict_of_users[reciver]['public_key'][0]
    print("n1={}".format(hex(n1)))
    d1 = dict_of_users[reciver]['private_key']
    print("d1={}".format(hex(d1)))
    n,e = dict_of_users[sender]['public_key']
    print("n={}".format(hex(n)))
    print("e={}".format(hex(e)))
    k = pow(k1,d1,n1)
    print("k={}".format(hex(k)))
    s = pow(s1,d1,n1)
    print("s={}".format(hex(s)))
    print("s^e modn={}".format(hex(pow(s,e,n))))
    if k == pow(s,e,n):
        dict_of_users[reciver]['varified_keys'][sender] = [k1, s1]
        return True





if __name__ == '__main__':
    GenerateKeyPair('tolik', 'yulya')
    message = 'attack at dawn'
    message2 = 'meet near the fountain'
    p,q = dict_of_users['tolik']['p_and_q']
    n,e = dict_of_users['tolik']['public_key']
    d = dict_of_users['tolik']['private_key']
    p1,q1 = dict_of_users['yulya']['p_and_q']
    n1,e1 = dict_of_users['yulya']['public_key']
    d1 = dict_of_users['yulya']['private_key']
    print("p користувача A: {}".format(hex(p)))
    print("q користувача A: {}".format(hex(q)))
    print("n користувача A: {}".format(hex(n)))
    print("e користувача A: {}".format(hex(e)))
    print("d користувача A: {}".format(hex(d)))
    print("\n")
    print("p користувача B: {}".format(hex(p1)))
    print("q користувача B: {}".format(hex(q1)))
    print("n користувача B: {}".format(hex(n1)))
    print("e користувача B: {}".format(hex(e1)))
    print("d користувача B: {}".format(hex(d1)))
    print("")
    crypt = Encrypt(message, e, n)
    print(Decrypt(crypt, d, n))
    m, s = Sign(message, d, n)
    m1, s1 = Sign(message2, d1, n1)
    print("підпис користувача A ({},{})".format(m,s))
    print("підпис користувача  B ({},{})".format(m1,s1))
    print(Verify(m, s, e, n))
    print(Verify(m1, s1, e1, n1))
    SendKey('tolik','yulya')
    print(ReceiveKey('tolik','yulya'))


