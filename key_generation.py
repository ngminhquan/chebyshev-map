import numpy as np
import random
from math import gcd
from hash_encrypt import long_to_bytes, bytes_to_long
import random
import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def generate_random_prime(length):
    while True:
        num = random.getrandbits(length)
        if is_prime(num):
            return num

# Example usage
binary_length = 16  # Specify the length in binary
p = generate_random_prime(binary_length)


#find g: Integer in[1, ..., p−1]with order p−1 modulo p
g = 2

#Chebyshev map
def chebyshev(g, x):
    A = np.array([[0, 1], [-1, 2*x]])
    T0_1 = np.array([1, x])
    A_g = np.linalg.matrix_power(A, g - 1)
    T = A_g@T0_1
    T_g = T[1]

    return T_g

#key generation
'''
alpha_a and alpha_b: two large integer
x: random x
'''
def key_gen(alpha_a, alpha_b, x):
    pu_a = chebyshev_plus(alpha_a, x, p)
    pu_b = chebyshev_plus(alpha_b, x, p)
    return np.array([[alpha_a, pu_a], [alpha_b, pu_b]])

def chebyshev_plus(s, x, p) -> int:        #chebyshev for g^s(x) modulo p
    val = x
    for i in range(s):
        val = chebyshev(2, val) % p
    return int(val)

alpha_a = random.randint(10**(4-1), 10**4-1)
alpha_b = random.randint(10**(4-1), 10**4-1)
alpha_a = 5678
alpha_b = 5555

x = random.randint(10**(3-1), 10**3-1)
#print('p: ', p)
#print('x: ', x)
#print(key_gen(alpha_a, alpha_b, x))

def cbs_plus(s, x, p):
    A = np.array([[0, 1], [-1, 2*x]])
    T0_1 = np.array([1, x])
    r = 1
    A = np.mod(A, p)
    A2 = np.mod(A@A, p)
    e = g ** s - 1
    while e > 0:
        if e % 2 == 1:
            r = np.mod(r * A, p)
        e >>= 1
        A = np.mod(A@A, p)
    T = np.mod(r@T0_1, p)
    T_g = T[1]
    
    return T_g



a = cbs_plus(3, 5, 137)
b = chebyshev_plus(3, 5, 137)
c = chebyshev(8, 5)
print('a',a)
print('b',b)
print(c % 137)