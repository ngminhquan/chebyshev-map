import numpy as np
import random
#from key_generation import chebyshev
from hash_encrypt import AES, long_to_bytes, bytes_to_long, hash_function

#Các tham số phục vụ cho signcrypt
'''
alpha_a = 
pu_a = 

#lấy pu_b của Bob
pu_b = 

x =
p =  
'''
g = 2

class signcryption_scheme(object):
    def __init__(self, alpha_a: int, pu_a: int, pu_b: int, x: int, p: int) -> None:
        self._alpha_a:int = alpha_a
        self._pu_a:int = pu_a
        self._pu_b:int = pu_b
        self._x:int = x
        self._p = p

    def _xor(self, a: bytes, b: bytes) -> bytes:
        return bytes([x ^ y for x, y in zip(a, b)])

    #pad/unpad bit '0' to full of block
    def _pad(self, data: bytes, block_size: int) -> bytes:
        padding_length: int = block_size - (len(data) % self._block_size)
        padding: bytes = b'\x00' * padding_length
        return data + padding

    def _unpad(self, data: bytes) -> bytes:
        padding_length: int = data[-1]
        return data[:-padding_length]
    
    #aes encrypt & decrypt, use in cmac
    def _aes_encrypt(self, block: bytes) -> bytes:
        key = AES(self._k2)
        return key.encrypt(block)

    def _aes_decrypt(self, block: bytes) -> bytes:
        key = AES(self._k2)
        return key.decrypt(block)
    
    # Tính toán giá trị K
    def k_gen(self):
        while(1):
            self.alpha = random.randint(1, self._p - 1)
            if (self._p - 1) % self.alpha != 0:
                break
        K = chebyshev(pow(g, self._alpha_a - self.alpha), self._pu_b) % self._p
        K = long_to_bytes(K, 48)
        return K

    def signcrypt(self, message):
        K = self.k_gen()
        self._k1 = K[:32]
        self._k2 = K[32:]


        digest = hash_function(message)
        r = self._xor(digest, self._k1)
        r = bytes_to_long(r)
        s = chebyshev(pow(g, self._alpha_a - self.alpha - r), self._x) % self._p
        C = self._aes_encrypt(message)
        return r, s, C


msg = b'minhquan_iotk65_'
alpha_a = 847
pu_a = 1
pu_b = 1
x = 911
p = 37

sign = signcryption_scheme(alpha_a, pu_a, pu_b, x, p)

#print(sign.signcrypt(msg))


