import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import time

# Tạo cặp khóa elliptic curve với secret key là một số ngẫu nhiên 256-bit
def generate_ec_keypair():
    private_key = ec.generate_private_key(
        ec.SECP256R1(), default_backend()
    )

    # Tạo secret key ngẫu nhiên 256-bit
    secret_key = os.urandom(32)
    private_key = ec.derive_private_key(int.from_bytes(secret_key, byteorder='big'), ec.SECP256R1(), default_backend())

    public_key = private_key.public_key()

    return private_key, public_key

# Chạy ví dụ
private_key, public_key = generate_ec_keypair()

# In ra khóa bí mật dưới dạng số nguyên
private_key_int = private_key.private_numbers().private_value
print("Private key (integer):")
print(private_key_int)

# In ra khóa công khai dưới dạng số nguyên
public_key_int = public_key.public_numbers().y
print("Public key (integer):")
print(public_key_int)



count = 10
avg = 0
for i in range(count):
    start_time = time.time()

    # Đoạn code cần đo thời gian thực thi
    private_key, public_key = generate_ec_keypair()


    end_time = time.time()

    duration = end_time - start_time
    avg += duration

avg /= count
print(avg)
print("Thời gian chạy: {:.5f} giây".format(avg))