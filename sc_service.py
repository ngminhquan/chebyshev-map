import math
import random

'''
import uuid

def get_mac_address():
    mac = uuid.getnode()
    mac_address = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_address

mac_address = get_mac_address()
print("Địa chỉ MAC của máy là:", mac_address)
'''

'''
import netifaces

def get_mac_address(ip):
    for interface in netifaces.interfaces():
        try:
            addrs = netifaces.ifaddresses(interface)
            mac = addrs[netifaces.AF_LINK][0]['addr']
            ip_list = addrs[netifaces.AF_INET]
            for entry in ip_list:
                if entry['addr'] == ip:
                    return mac
        except KeyError:
            pass
    
    return None

ip_address = "192.168.153.254"  # Địa chỉ IP của máy cần đọc địa chỉ MAC
mac_address = get_mac_address(ip_address)

if mac_address:
    print("Địa chỉ MAC của máy là:", mac_address)
else:
    print("Không tìm thấy địa chỉ MAC cho máy với địa chỉ IP đã cho.")
'''


#get random prime number 
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
        
#example use
#binary_length = 40  # Specify the length in binary
#p = generate_random_prime(binary_length)
