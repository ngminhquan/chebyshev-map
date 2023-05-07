import matplotlib.pyplot as plt
from key_generation import chebyshev_plus
import random
from hash_encrypt import hash_function, bytes_to_long, long_to_bytes
from collections import Counter


x_0 = 857
p = 7856

id_a = b'user_a'
id_b = b'user_b'
nonce_i = b'nonce'

k_m = hash_function(id_b + id_a + nonce_i)[:1]
k_m = bytes_to_long(k_m)

# Dữ liệu của 2 biến
x = []
y = []
for i in range(2*10**(4-1), 2*(10**3 + 100)):
    x.append(i)
    val = chebyshev_plus(i - k_m, x_0, p)
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