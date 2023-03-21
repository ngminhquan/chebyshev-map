import numpy as np
import random


def miller_rabin(n, a): # odd number only
#find k and q
    q = n-1	
    k = 0
    while(q%2 == 0):
        k += 1
        q //= 2
#testing
    v = pow(a, q, n)
    if v == 1 or v == n-1:
        return True
    for i in range(k-1):
        v = pow(v,2, n)
        if v == n-1:
            return True
    return False

def primetest(n):

    low_primes = [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
        211,
        223,
        227,
        229,
        233,
        239,
        241,
        251,
        257,
        263,
        269,
        271,
        277,
        281,
        283,
        293,
        307,
        311,
        313,
        317,
        331,
        337,
        347,
        349,
        353,
        359,
        367,
        373,
        379,
        383,
        389,
        397,
        401,
        409,
        419,
        421,
        431,
        433,
        439,
        443,
        449,
        457,
        461,
        463,
        467,
        479,
        487,
        491,
        499,
        503,
        509,
        521,
        523,
        541,
        547,
        557,
        563,
        569,
        571,
        577,
        587,
        593,
        599,
        601,
        607,
        613,
        617,
        619,
        631,
        641,
        643,
        647,
        653,
        659,
        661,
        673,
        677,
        683,
        691,
        701,
        709,
        719,
        727,
        733,
        739,
        743,
        751,
        757,
        761,
        769,
        773,
        787,
        797,
        809,
        811,
        821,
        823,
        827,
        829,
        839,
        853,
        857,
        859,
        863,
        877,
        881,
        883,
        887,
        907,
        911,
        919,
        929,
        937,
        941,
        947,
        953,
        967,
        971,
        977,
        983,
        991,
        997,
    ]
    if n in low_primes:
        return True
    if n %2 == 0:
        return False
    # very large number
    for i in range(100):
        a = random.randrange(2,n-1)
        if miller_rabin(n,a) == False:
            return False
        else:
            continue
    return True
inp = int(input("Nhap so bit cua so prime can tao: "))
# Tìm số nguyên tố lớn p
while(1):
    p = random.randrange(pow(2,inp),pow(2,inp+1))
    if primetest(p) == True:
        break
    else:
        continue

print(primetest(p))
#p = str(hex(p))
print(p)
print("Done!")

    #find g: Integer in[1, ..., p−1]with order p−1 modulo p

from math import gcd

# find the prime factors of p-1
factors = []
q = p - 1
for i in range(2, int(q**0.5)+1):
    if q % i == 0:
        factors.append(i)
        while q % i == 0:
            q //= i
if q > 1:
    factors.append(q)

# find a generator of the group of units modulo p
k = 2
while pow(k, (p-1)//2, p) == 1 or any(pow(k, (p-1)//factor, p) == 1 for factor in factors):
    k = random.randint(2, p-2)

# find an integer with order p-1 modulo p
g = pow(k, (p-1)//2, p)
for factor in factors:
    h = pow(k, (p-1)//factor, p)
    while h != 1:
        g = (g*h) % p
        h = pow(h, factor, p)
        
# print the integer with order p-1 modulo p
print("Integer with order p-1 modulo p:", g)


    #Chebyshev map
def chebyshev(g, x):           #x in the value of [-1;1]
    A = np.array([[0, 1], [-1, 2*x]])
    T0_1 = [1, x]
    A_g = np.linalg.matrix_power(A, g - 1)
    T = A_g@T0_1
    T_g = T[1]

    return T_g



#key generation
'''
alpha_a and alpha_b: two large integer
x: random x
'''
def key_gen(alpha_a, alpha_b, x, g):
    Tg_a = chebyshev(pow(g, alpha_a), x)
    Tg_b = chebyshev(pow(g, alpha_b), x)
    pu_a = Tg_a % p
    pu_b = Tg_b % p
    return np.array([[alpha_a, pu_a], [alpha_b, pu_b]])


alpha_a = random.randint(10**(3-1), 10**3-1)
alpha_b = random.randint(10**(3-1), 10**3-1)

x = random.randint(10**(3-1), 10**3-1)

print(key_gen(alpha_a, alpha_b, x, g))


