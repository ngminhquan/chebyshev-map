import numpy as np
import random
from math import gcd
from hash_encrypt import long_to_bytes, bytes_to_long
import random
import math
import time
import sys
import os
#sys.set_int_max_str_digits(100000)
g =2
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



#Chebyshev map
def chebyshev(g, x):
    A = np.array([[0, 1], [-1, 2*x]])
    T0_1 = np.array([1, x])
    A_g = np.linalg.matrix_power(A, g - 1)
    T = A_g@T0_1
    T_g = T[1]

    return T_g# % p


def cbs(g, x, p):
    A = np.array([[0, 1], [-1, 2*x]])
    T0_1 = np.array([1, x])
    A_g = A
    for i in range(g):
        A_g = np.mod(A_g@A, p)
    T = np.mod(A_g@T0_1, p)
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
        val = chebyshev(g, val) % p
    return int(val)



def Tnm2(n, x, m):
    if n == 0:
        return 1
    elif n == 1:
        return x % m
    else:
        e = n - 1
        a11, a12, a21, a22 = 1, 0, 0, 1
        s11, s12, s21, s22 = 0, 1, -1, (2 * x)
        
        while e > 1:
            
            
            if e % 2 == 1:
                t1 = (a11 * s11 + a12 * s21) % m
                a12 = (a11 * s12 + a12 * s22) % m
                a11 = t1
                t2 = (a21 * s11 + a22 * s21) % m
                a22 = (a21 * s12 + a22 * s22) % m
                a21 = t2
                
            t1 = s11 + s22
            t2 = s12 * s21
            s11 = (s11 ** 2 + t2) % m
            s12 = (s12 * t1) % m
            s21 = (s21 * t1) % m
            s22 = (s22 ** 2 + t2) % m
            e //=2
        
        t1 = (a21 * s11 + a22 * s21) % m
        t2 = (a21 * s12 + a22 * s22) % m
        return (t1 + t2 * x) % m



def cbs2(n, x, p):
    if n == 0:
        return 1
    elif n == 1:
        return x % p
    elif n % 2 == 0:

        return (2 * cbs2(n // 2, x, p) ** 2 - 1) % p
    else:
        return (2 * cbs2((n - 1) // 2, x, p) * cbs2((n + 1) // 2, x, p) - x) %p
    
def MyPowerMod(b,c,q):
    a = 1
    str = bin(c)[2:]
    for i in range(len(str)-1):
        if str[i] == '1':
            a = a*b
        a = (a**2) % q
        
    if str[-1] == '1' :
        a = a*b

    a = a % q
    return a
def Chebyshev(p,x,n):
    if(p%4 != 3):
        sys.exit
    if MyPowerMod(x**2 -1,(p-1)//2,p) != 1:
        sys.exit
    k = (p+1)//4
    a = (x  + MyPowerMod(x**2-1,k,p)) % p
    r0 = pow(2,-1,p) 
    r1 = MyPowerMod(a,n,p)
    r2 = pow(r1,-1,p)
    r = (r0*(r1+r2)) %p
    return r  




alpha_a = random.randint(2**(6-1), 2**6-1)

x = random.randint(2**(4-1), 2**4-1)
#print('p: ', p)
#print('x: ', x)
#print(key_gen(alpha_a, alpha_b, x))



# Example usage
binary_length = 20  # Specify the length in binary
p = generate_random_prime(binary_length)
p = 2**521 - 1
x = 1234567890987654320
n = 10000000000000000000000000000000000001


x = 7**233
n = 13**178
p = 97**100 + 528

count = 100
'''

for i in range(100):
    avg = 0
    for i in range(count):
        start_time = time.time()

        # Đoạn code cần đo thời gian thực thi
        
        k2 = cbs3(p, x, n)
        #k2 = 1

        end_time = time.time()

        duration = end_time - start_time
        avg += duration

    avg /= count
    print("Thời gian chạy mới 3: {:.5f} giây".format(avg))



avg = 0
for i in range(count):
    start_time = time.time()

    # Đoạn code cần đo thời gian thực thi
    
    k2 = Tnm2(n, x, p)
    #k2 = 1

    end_time = time.time()

    duration = end_time - start_time
    avg += duration

avg /= count
print("Thời gian chạy mới 2: {:.5f} giây".format(avg))
'''
'''
avg = 0
for i in range(count):
    start_time = time.time()

    # Đoạn code cần đo thời gian thực thi
    
    k2 = cbs2(p, x, n)
    #k2 = 1

    end_time = time.time()

    duration = end_time - start_time
    avg += duration

avg /= count
print("Thời gian chạy mới 1: {:.5f} giây".format(avg))
'''
