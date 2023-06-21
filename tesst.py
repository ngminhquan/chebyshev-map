p = 2**521 - 1
x = 1234567890987654320
n = 10000000000000000000000000000000000001
print('hello')

'''
import sys
import time
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


print(Chebyshev(p,x,n))

count = 10
avg = 0
for i in range(count):
    start_time = time.time()

    # Đoạn code cần đo thời gian thực thi

    #a = hybrid_key.verify_user_A()
    Chebyshev(p,x,n)
    

    #print(c)

    end_time = time.time()

    duration = end_time - start_time
    avg += duration

avg /= count
print(avg)
print("Thời gian chạy: {:.5f} giây".format(avg))

'''