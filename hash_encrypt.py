import struct
import sys
from collections import deque
import numpy as np


""" PRESENT block cipher implementation

USAGE EXAMPLE:
---------------
Importing:
-----------
>>> from pypresent import Present

Encrypting with a 80-bit key:
------------------------------
>>>key = b'10 bytes--'
>>>plain = b'minhquan'
>>>cipher = Present(key)
>>>encrypted = cipher.encrypt(plain)
b'8K\xf0\x80\xe4\x0e\xf8G'

>>>decrypted = cipher.decrypt(encrypted)
b'minhquan'

Encrypting with a 128-bit key:
-------------------------------
>>> key = b'16 bytes length.'
>>> plain = b'minhquan'
>>> cipher = Present(key)
>>> encrypted = cipher.encrypt(plain)
b'\xf4\x8a\xfdQ\xca\xd7Up'

>>> decrypted = cipher.decrypt(encrypted)
b'minhquan'

"""
class Present:
        def __init__(self,key,rounds=32):
                """Create a PRESENT cipher object

                key:    the key as a 128-bit or 80-bit rawstring
                rounds: the number of rounds as an integer, 32 by default
                """
                self.rounds = rounds
                if len(key) * 8 == 80:
                        self.roundkeys = generateRoundkeys80(bytes_to_long(key),self.rounds)
                elif len(key) * 8 == 128:
                        self.roundkeys = generateRoundkeys128(bytes_to_long(key),self.rounds)
                else:
                        raise ValueError /'Key must be a 128-bit or 80-bit rawstring'

        def encrypt(self,block):
                """Encrypt 1 block (8 bytes)

                Input:  plaintext block as raw string
                Output: ciphertext block as raw string
                """
                state = bytes_to_long(block)
                for i in range(self.rounds - 1):
                        state = addRoundKey(state,self.roundkeys[i])
                        state = sBoxLayer(state)
                        state = pLayer(state)
                cipher = addRoundKey(state,self.roundkeys[-1])
                return long_to_bytes(cipher,8)

        def decrypt(self,block):
                """Decrypt 1 block (8 bytes)

                Input:  ciphertext block as raw string
                Output: plaintext block as raw string
                """
                state = bytes_to_long(block)
                for i in range(self.rounds - 1):
                        state = addRoundKey(state,self.roundkeys[-i-1])
                        state = pLayer_dec(state)
                        state = sBoxLayer_dec(state)
                decipher = addRoundKey(state,self.roundkeys[0])
                return long_to_bytes(decipher,8)

        def get_block_size(self):
                return 8

#        0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox= [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]
Sbox_inv = [Sbox.index(x) for x in range(16)]
PBox = [0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
        4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
        8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
        12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
PBox_inv = [PBox.index(x) for x in range(64)]

def generateRoundkeys80(key,rounds):
        """Generate the roundkeys for a 80-bit key

        Input:
                key:    the key as a 80-bit integer
                rounds: the number of rounds as an integer
        Output: list of 64-bit roundkeys as integers"""
        roundkeys = []
        for i in range(1, rounds + 1): # (K1 ... K32)
                # rawkey: used in comments to show what happens at bitlevel
                # rawKey[0:64]
                roundkeys.append(key >>16)
                #1. Shift
                #rawKey[19:len(rawKey)]+rawKey[0:19]
                key = ((key & (2**19-1)) << 61) + (key >> 19)
                #2. SBox
                #rawKey[76:80] = S(rawKey[76:80])
                key = (Sbox[key >> 76] << 76)+(key & (2**76-1))
                #3. Salt
                #rawKey[15:20] ^ i
                key ^= i << 15
        return roundkeys

def generateRoundkeys128(key,rounds):
        """Generate the roundkeys for a 128-bit key

        Input:
                key:    the key as a 128-bit integer
                rounds: the number of rounds as an integer
        Output: list of 64-bit roundkeys as integers"""
        roundkeys = []
        for i in range(1, rounds + 1): # (K1 ... K32)
                # rawkey: used in comments to show what happens at bitlevel
                roundkeys.append(key >>64)
                #1. Shift
                key = ((key & (2**67-1)) << 61) + (key >> 67)
                #2. SBox
                key = (Sbox[key >> 124] << 124)+(Sbox[(key >> 120) & 0xF] << 120)+(key & (2**120-1))
                #3. Salt
                #rawKey[62:67] ^ i
                key ^= i << 62
        return roundkeys

def addRoundKey(state,roundkey):
        return state ^ roundkey

def sBoxLayer(state):
        """SBox function for encryption

        Input:  64-bit integer
        Output: 64-bit integer"""

        output = 0
        for i in range(16):
                output += Sbox[( state >> (i*4)) & 0xF] << (i*4)
        return output

def sBoxLayer_dec(state):
        """Inverse SBox function for decryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in range(16):
                output += Sbox_inv[( state >> (i*4)) & 0xF] << (i*4)
        return output

def pLayer(state):
        """Permutation layer for encryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in range(64):
                output += ((state >> i) & 0x01) << PBox[i]
        return output

def pLayer_dec(state):
        """Permutation layer for decryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in range(64):
                output += ((state >> i) & 0x01) << PBox_inv[i]
        return output

#convert bytes -> long and long -> bytes
def long_to_bytes(n, blocksize=0):

    if n < 0 or blocksize < 0:
        raise ValueError("Values must be non-negative")

    result = []
    pack = struct.pack

    # Fill the first block independently from the value of n
    bsr = blocksize
    while bsr >= 8:
        result.insert(0, pack('>Q', n & 0xFFFFFFFFFFFFFFFF))
        n = n >> 64
        bsr -= 8

    while bsr >= 4:
        result.insert(0, pack('>I', n & 0xFFFFFFFF))
        n = n >> 32
        bsr -= 4

    while bsr > 0:
        result.insert(0, pack('>B', n & 0xFF))
        n = n >> 8
        bsr -= 1

    if n == 0:
        if len(result) == 0:
            bresult = b'\x00'
        else:
            bresult = b''.join(result)
    else:
        # The encoded number exceeds the block size
        while n > 0:
            result.insert(0, pack('>Q', n & 0xFFFFFFFFFFFFFFFF))
            n = n >> 64
        result[0] = result[0].lstrip(b'\x00')
        bresult = b''.join(result)
        # bresult has minimum length here
        if blocksize > 0:
            target_len = ((len(bresult) - 1) // blocksize + 1) * blocksize
            bresult = b'\x00' * (target_len - len(bresult)) + bresult

    return bresult


def bytes_to_long(s):
    """Convert a byte string to a long integer (big endian).

    In Python 3.2+, use the native method instead::

        >>> int.from_bytes(s, 'big')

    For instance::

        >>> int.from_bytes(b'\x00P', 'big')
        80

    This is (essentially) the inverse of :func:`long_to_bytes`.
    """
    acc = 0

    unpack = struct.unpack

    # Up to Python 2.7.4, struct.unpack can't work with bytearrays nor
    # memoryviews
    if sys.version_info[0:3] < (2, 7, 4):
        if isinstance(s, bytearray):
            s = bytes(s)
        elif isinstance(s, memoryview):
            s = s.tobytes()

    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = b'\x00' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc

#photon lightweight hash function
'''
#AES-Permutation algorithm 

fieldmult2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
              [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
              [0, 3, 6, 5, 12, 15, 10, 9, 11, 8, 13, 14, 7, 4, 1, 2],
              [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
              [0, 5, 10, 15, 7, 2, 13, 8, 14, 11, 4, 1, 9, 12, 3, 6],
              [0, 6, 12, 10, 11, 13, 7, 1, 5, 3, 9, 15, 14, 8, 2, 4],
              [0, 7, 14, 9, 15, 8, 1, 6, 13, 10, 3, 4, 2, 5, 12, 11],
              [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1],
              [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
              [0, 10, 7, 13, 14, 4, 9, 3, 15, 5, 8, 2, 1, 11, 6, 12],
              [0, 11, 5, 14, 10, 1, 15, 4, 7, 12, 2, 9, 13, 6, 8, 3],
              [0, 12, 11, 7, 5, 9, 14, 2, 10, 6, 1, 13, 15, 3, 4, 8],
              [0, 13, 9, 4, 1, 12, 8, 5, 2, 15, 11, 6, 3, 14, 10, 7],
              [0, 14, 15, 1, 13, 3, 2, 12, 9, 7, 6, 8, 4, 10, 11, 5],
              [0, 15, 13, 2, 9, 6, 4, 11, 1, 14, 12, 3, 8, 7, 5, 10]]

class permutation:
    
    def __init__(self, input_hash,round_num=12):
        
        self.input = input_hash
        self.input_len = len(input_hash)
        self.round_num = round_num
        self.each_round_value = []
    
    def rc(self,v):
        if v == 1:
            return [1, 0, 2, 7, 5]
        elif v == 2:
            return [3, 2, 0, 5, 7]
        elif v == 3:
            return [7, 6, 4, 1, 3]
        elif v == 4:
            return [14, 15, 13, 8, 10]
        elif v == 5:
            return [13, 12, 14, 11, 9]
        elif v == 6:
            return [11, 10, 8, 13, 15]
        elif v == 7:
            return [6, 7, 5, 0, 2]
        elif v == 8:
            return [12, 13, 15, 10, 8]
        elif v == 9:
            return [9, 8, 10, 15, 13]
        elif v == 10:
            return [2, 3, 1, 4, 6]
        elif v == 11:
            return [5, 4, 6, 3, 1]
        elif v == 12:
            return [10, 11, 9, 12, 14]
    
    def shift_row(self):
        
        result_shiftrow = []
        for row in range(self.input_len):
            item = deque(self.input[row])
            item.rotate(-row)
            result_shiftrow.append(list(item))
        
        self.input = result_shiftrow
        
        return result_shiftrow
        
    def subcell(self):

        sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
        result_subcell = self.input
        for i in range(0, self.input_len):
            for j in range(0, self.input_len):
                result_subcell[i][j] = sbox[int(self.input[i][j])]
        
        self.input = result_subcell
        
        return result_subcell
                
    def addconstant(self,v):
   
        result_addconstant = self.input

        for i in range(0, self.input_len):
            result_addconstant[i][0] = self.input[i][0] ^ self.rc(v)[i]
        
        self.input = result_addconstant
        
        return result_addconstant
        
    
    def mixcolumn(self):

        A_t = [[1, 2, 9, 9, 2],
               [2, 5, 3, 8, 13],
               [13, 11, 10, 12, 1],
               [1, 15, 2, 3, 14],
               [14, 14, 8, 5, 12]]

        #irreducible polynomial  = x^4+x+1 : 10011

        result_mixcolumn = [[0 for x in range(self.input_len)] for x in range(self.input_len)]
        xor_sum = 0
        for i in range(0, self.input_len):
            for j in range(0, self.input_len):
                for k in range(0, self.input_len):
                    xor_sum = xor_sum ^ fieldmult2[A_t[i][k]][self.input[k][j]]
                result_mixcolumn[i][j] = xor_sum
                xor_sum = 0
        
        self.input = result_mixcolumn
        
        return result_mixcolumn
    
    def get_each_round(self):
        
        return self.each_round_value
               
            
    def permutation_result(self):
        
        for i in range(self.round_num):
            
            self.addconstant(i+1)
            self.subcell()
            self.shift_row()
            self.mixcolumn()
            self.each_round_value.append(self.input)
            
        return self.input
    


class absorb:
    
    def __init__(self,input_hash):
        
        self.State= [[0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,1],
                     [4,1,4,1,0]] 
        
        self.input_hash = input_hash
        self.input_len = len(input_hash)
        
        
    def xor_message(self):
        
        current_state = np.array(self.State[0])
        message = np.array(self.input_hash[0])
        self.State[0] = list(current_state^message)
        self.input_hash.pop(0)
        
    def result_absorb(self):
        
        for message in range(self.input_len):
            
            self.xor_message()
            print("Message {}".format(self.State[0]))
            permutation_ = permutation(self.State)
            self.State = permutation_.permutation_result()
            print("Permutation {} \n:".format(message))
            print(self.State)
            print("---------------------------------")
            
        return self.State
    


a = absorb(data)
_hash = a.result_absorb()

'''

def hash_func(a, k):
      a = a + k
      return a[:2]