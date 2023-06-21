import matplotlib.pyplot as plt
import random
from hash_encrypt import hash_function, bytes_to_long, long_to_bytes
from collections import Counter
import math

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Generate ECC key pairs for Alice and Bob
alice_key = ec.generate_private_key(ec.SECP256R1())
bob_key = ec.generate_private_key(ec.SECP256R1())

# Alice's public key
alice_public_key = alice_key.public_key()
print(alice_key)
print(alice_public_key)

# Bob's public key
bob_public_key = bob_key.public_key()

# Alice computes the shared secret
alice_shared_secret = alice_key.exchange(ec.ECDH(), bob_public_key)

# Bob computes the shared secret
bob_shared_secret = bob_key.exchange(ec.ECDH(), alice_public_key)
alice_shared_secret = alice_key.exchange(ec.ECDH(), bob_public_key)
bob_shared_secret = bob_key.exchange(ec.ECDH(), alice_public_key)
        

        


'''
g = 2
x = 857
binary_length = 128  # Specify the length in binary
p = 340282366920938463463374607431768211507

id_a = b'user_a'
id_b = b'user_b'
nonce_i = b'nonce'

k_m = hash_function(id_b + id_a + nonce_i)[:1]
k_m = bytes_to_long(k_m)

ctr1 = 0
ctr2 = 0
alpha_a = random.randint(10**5, 10**6)
alpha_b = random.randint(10**5, 10**6)
alpha_b2 = alpha_b - 1
#print(len(bin(alpha_a+alpha_b-k_m)[2:]))
ssk1 = Chebyshev(p, x, g**(alpha_a + alpha_b - k_m))
print(hex(ssk1), len(hex(ssk1)[2:]))

'''






'''
# Dữ liệu của 2 biến
x = []
y = []
for i in range(2*10**(4-1), 2*(10**3 + 100)):
    x.append(i)
    val = Chebyshev(p, x_0, g**(i-k_m))
    y.append(val)


# Danh sách ban đầu
my_list = y

# Đếm số lần xuất hiện của mỗi phần tử
counter = Counter(my_list)
# Lọc các phần tử có số lần xuất hiện lớn hơn 1
result = {element: count for element, count in counter.items() if count > 1}

# Hiển thị số lần xuất hiện của các phần tử
for element, count in result.items():
    print(f"{element}: {count} lần")


# Vẽ đồ thị
plt.plot(x, y)

# Đặt tên cho trục x và trục y
plt.xlabel('alpha')
plt.ylabel('session key')

# Đặt tiêu đề cho đồ thị
plt.title('Sự phụ thuộc giữa 2 biến')

# Hiển thị đồ thị
#plt.show()
'''