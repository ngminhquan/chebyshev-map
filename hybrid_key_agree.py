import random
import numpy as np
from key_generation import chebyshev_plus, Chebyshev
from hash_encrypt import Present, long_to_bytes, bytes_to_long, hash_function
import time


#user A send to user B to request:
'''
id_a = 
nonce_i =                      #time stamp to identify transaction
'''
#user B send to KDC:
'''
id_b = 
id_a||nonce_i = 
'''
#output of KDC:
'''
x = 
p = 
g = 2
k_m = 
'''

class key_agreement(object):
    def __init__(self, id_a: bytes, id_b: bytes, nonce_i: bytes, alpha_a: int, alpha_b: int, pu_b: int, x: int, p: int, k_m: int) -> None:
        self._id_a = id_a
        self._id_b = id_b
        self.nonce = nonce_i
        self._alpha_a:int = alpha_a
        self._alpha_b:int = alpha_b
        self._pu_b:int = pu_b
        self._x = x
        self._p = p
        self._k_m = k_m

    #encrypt & decrypt, use in cmac
    def present_encrypt(self, block: bytes) -> bytes:
        key = Present(long_to_bytes(self.ssk, 10))
        return key.encrypt(block)

    def present_decrypt(self, block: bytes) -> bytes:
        key = Present(long_to_bytes(self.ssk, 10    ))
        return key.decrypt(block)

    def verify_user_A(self):        #run at user B
        digest = hash_function(self._id_b + self._id_a + self.nonce)[:2]
        k_m_new = bytes_to_long(digest)
        if k_m_new != self._k_m:
            return 'INVALID'
        else:
            return self._pu_b
        
    def gen_ssk(self):      #run at user A
        #ssk = chebyshev(alpha_a+alpha_b-k_m, x) mod p
        self.ssk = chebyshev_plus(self._alpha_a - self._k_m, self._pu_b, self._p)
        #encrypt session key and send to B
        cp = self.present_encrypt(long_to_bytes(self._k_m, 8))
        self._cp = bytes_to_long(cp)
        self._cp_s = bytes_to_long(cp[:1])

        #find s = chebyshev(alpha_a - k_m - cp, x) mod p
        self._s = chebyshev_plus(self._alpha_a - self._k_m - self._cp_s, self._x, self._p)
        #return self._s, self._cp
        return 0

    def recover_ssk(self):
        #find ssk' from s and cp
        ssk_new = chebyshev_plus(self._alpha_b + self._cp_s, self._s, self._p)
        #decrypt to receive k_m'
        _cp = long_to_bytes(self._cp, 8)
        k_m_test = self.present_decrypt(_cp)
        k_m_test = bytes_to_long(k_m_test)

        #verify
        return ssk_new
        '''
        if k_m_test == self._k_m:
            print('VALID k_m')
            if ssk_new == self.ssk:
                print("VALID ssk")
                return ssk_new
            else:
                return 'INVALID ssk'
        else:
            return 'INVALID k_m'
        '''
'''
id_a = b'user_a'
id_b = b'user_b'
nonce_i = b'nonce'
alpha_a = 5678
alpha_b = 5555
pu_b = 5340
x = 857
p = 7873
k_m = hash_function(id_b + id_a + nonce_i)[:1]
k_m = bytes_to_long(k_m)

hybrid_key = key_agreement(id_a, id_b, nonce_i, alpha_a, alpha_b, pu_b, x, p, k_m)

count = 100
avg = 0
for i in range(count):
    start_time = time.time()

    # Đoạn code cần đo thời gian thực thi

    #a = hybrid_key.verify_user_A()
    b = hybrid_key.gen_ssk()
    c = hybrid_key.recover_ssk()

    #print(c)

    end_time = time.time()

    duration = end_time - start_time
    avg += duration

avg /= count
print(avg)
print("Thời gian chạy: {:.5f} giây".format(avg))

'''
import sys
import time
import random
import string
from Crypto.Util import number
import secrets


def gen_number(lenght):
    # Generate a random 128-bit number
    random_number = secrets.randbits(lenght)
    return random_number

# Generate a 128-bit number


def generate_random_string(length):
    # Choose from all uppercase letters, lowercase letters, and digits
    characters = string.ascii_letters + string.digits
    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Generate a random string of length 10

a = input("nhap id A : ")
b = input("nhap id B : ")

#verify valid id of user
with open('id.txt','r',encoding='utf-8') as id_file:
    line = id_file.readlines()
    temp = 0
    for i in line:
        if str(a) == str(b) :
            temp = 1
        elif str(a) == str(i[:6]) or str(b) == str(i[:6]):
            temp += 1

    #user invalid: stop program
    #user valid: continue        
    if temp != 2:
        print("denied acesss!")
        exit()
    else :
        print("accepted !")
a = long_to_bytes(int(a))
b = long_to_bytes(int(b))
print("User A send request ")
time.sleep(2)
userA = []
userB = []
KDC = []

#generate nonce
with open('nonce.txt','w',encoding='utf-8') as nonce_map:
    nonce = generate_random_string(6)
    nonce_map.write(nonce+'\n')
nonce = nonce.encode('utf-8')

#
userB.append(a+nonce)
print('user B trans to KDC')
time.sleep(2)


#KDC generate x, p, g and send to valid user
KDC.append(b+a+nonce)
k_m = hash_function(KDC[0])[:1]
p = number.getPrime(64)
x = gen_number(128)
g = [2,3,11,14]
g = random.choice(g)
k2_m = hash_function(b+userB[0])[:1]


#verify user
if k_m == k2_m:
    print('Km is true!')
else:
    print('Invalid')
    sys.exit
k_m = bytes_to_long(k_m)

#secret key and public key of two user
print("choose secret key B")
time.sleep(2)
alpha_b = gen_number(20)
n = g**alpha_b
pk_b = Chebyshev(p,x,n)
print("choose secret key A")
alpha_a = gen_number(20)

#user b 
hybrid_key = key_agreement(a, b, nonce, alpha_a, alpha_b, pk_b, x, p, k_m)
hybrid_key.gen_ssk()
print("recover ssk")
print(hybrid_key.recover_ssk())

