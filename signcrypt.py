import numpy as np
import random
from key_generation import chebyshev_plus
from hash_encrypt import Present, long_to_bytes, bytes_to_long, hash_func

#Các tham số phục vụ cho signcrypt
'''
alpha_a = 
pu_a = 

#lấy pu_b của Bob
pu_b = 

x =
p =  
'''

class signcryption_scheme(object):
    def __init__(self, alpha_a: int, pu_a: int, pu_b: int, x: int, p: int) -> None:
        self._alpha_a:int = alpha_a
        self._pu_a:int = pu_a
        self._pu_b:int = pu_b
        self._x:int = x
        self._p = p

    def _xor(self, a: bytes, b: bytes) -> bytes:
        return bytes([x ^ y for x, y in zip(a, b)])
    
    #encrypt & decrypt, use in cmac
    def present_encrypt(self, block: bytes) -> bytes:
        key = Present(self._k2)
        return key.encrypt(block)

    def present_decrypt(self, block: bytes) -> bytes:
        key = Present(self._k2)
        return key.decrypt(block)
    
    # Tính toán giá trị K
    def k_gen(self):
        while(1):
            self.alpha = random.randint(1, self._p - 1)
            if (self._p - 1) % self.alpha != 0:
                break
        k = chebyshev_plus(self._pu_b, self._x, self._p)
        k = long_to_bytes(k, 12)
        return k

    def signcrypt(self, message):
        k = self.k_gen()
        self._k1 = k[:2]
        self._k2 = k[2:]

        digest = hash_func(message, self._k1)
        print('dg:', digest)
        r = bytes_to_long(digest)

        s = chebyshev_plus(self._alpha_a - self.alpha - r, self._x, self._p)
        cp = self.present_encrypt(message)
        return r, s, cp


msg = b'minhquan_iotk65_'
alpha_a = 567040
pu_a =  21066
pu_b = 35903
x = 842
p = 46957

sign = signcryption_scheme(alpha_a, pu_a, pu_b, x, p)

print(sign.signcrypt(msg))
