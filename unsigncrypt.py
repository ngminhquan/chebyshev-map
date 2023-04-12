import numpy as np
import random
from key_generation import chebyshev_plus
from hash_encrypt import Present, long_to_bytes, bytes_to_long, hash_func

#Input data:
'''
r
s
g = 2
p
alpha_b
cp
'''
g = 2

class unsigncrypt_scheme(object):
    def __init__(self, alpha_b:int, pu_a: int, pu_b: int, p: int, r: int, s: int):
        self._alpha_b = alpha_b
        self._pu_a = pu_a
        self._pu_b = pu_b
        self._p = p
        self._r = r
        self._s = s

    def _xor(self, a: bytes, b: bytes) -> bytes:
        return bytes([x ^ y for x, y in zip(a, b)])
    
    #encrypt & decrypt, use in cmac
    def present_encrypt(self, block: bytes) -> bytes:
        key = Present(self._k2)
        return key.encrypt(block)

    def present_decrypt(self, block: bytes) -> bytes:
        key = Present(self._k2)
        return key.decrypt(block)
    
    def compute_k(self):
        k = chebyshev_plus(self._alpha_b +self._r, self._s, self._p)
        k = long_to_bytes(k, 12)
        return k
    
    def unsigncrypt(self, cp: bytes):
        #split k into k1 and k2
        k = self.compute_k()
        
        self._k1 = k[:2]
        self._k2 = k[2:]

        #decrypt ciphertext
        msg = self.present_decrypt(cp)
        print(msg)
        #check hash
        digest = hash_func(msg, self._k1)
        r_new = bytes_to_long(digest)
        print(r, r_new)
        if r_new == self._r:
            return msg
        else:
            return 'INVALID'

cp = b'\xa2W\xaa\xb8\x86\xc3^}'
r, s = 27904, 39871

alpha_b = 230882
pu_a = 21066
pu_b = 35903
p = 46957

unsign = unsigncrypt_scheme(alpha_b, pu_a, pu_b, p, r, s)

msg = unsign.unsigncrypt(cp)

print(msg)
        