import random
import numpy as np
from key_generation import chebyshev_plus
from hash_encrypt import Present, long_to_bytes, bytes_to_long, hash_function
import time

start_time = time.time()

# Đoạn code cần đo thời gian thực thi


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
        return self._s, self._cp

    def recover_ssk(self):
        #find ssk' from s and cp
        ssk_new = chebyshev_plus(self._alpha_b + self._cp_s, self._s, self._p)
        #decrypt to receive k_m'
        _cp = long_to_bytes(self._cp, 8)
        k_m_test = self.present_decrypt(_cp)
        k_m_test = bytes_to_long(k_m_test)

        #verify
        if k_m_test == self._k_m:
            print('VALID k_m')
            if ssk_new == self.ssk:
                print("VALID ssk")
                return ssk_new
            else:
                return 'INVALID ssk'
        else:
            return 'INVALID k_m'

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

a = hybrid_key.verify_user_A()
b = hybrid_key.gen_ssk()
c = hybrid_key.recover_ssk()

print(c)

end_time = time.time()

duration = end_time - start_time
print("Thời gian chạy: {:.3f} giây".format(duration))

