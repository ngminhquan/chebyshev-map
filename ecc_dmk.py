import field
from tinyec import registry
import time

# example key pairs
dA =b'81DB1EE100150FF2EA338D708271BE38300CB54241D79950F77B063039804F1D'

x_qA =b'44106E913F92BC02A1705D9953A8414DB95E1AAA49E81D9E85F929A8E3100BE5'
y_qA =b'8AB4846F11CACCB73CE49CBDD120F5A900A69FD32C272223F789EF10EB089BDC'

dB =b'55E40BC41E37E3E2AD25C3C6654511FFA8474A91A0032087593852D3E7D76BD3'

x_qB =b'8D2D688C6CF93E1160AD04CC4429117DC2C41825E1E9FCA0ADDD34E6F1B39F7B'
y_qB =b'990C57520812BE512641E47034832106BC7D3E8DD0E4C7F1136D7006547CEC6A'

x_Z =b'89AFC39D41D3B327814B80940B042590F96556EC91E6AE7939BCE31F3A18BF2B'
y_Z =b'49C27868F4ECA2179BFD7D59B1E3BF34C1DBDE61AE12931648F43E59632504DE'

# take sample parameters
samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

def calcPubKey(priKey: int):
    pubKey = priKey * curve.g
    return pubKey

def calculateMK(selfPriKey: int, receivedPubKey):
    mk = receivedPubKey * selfPriKey
    return mk

priKey1 = int(dA, 16)
priKey2 = int(dB, 16)




count = 10
avg = 0
for i in range(count):
    start_time = time.time()

    # Đoạn code cần đo thời gian thực thi
    pubKey1 = priKey1 * curve.g
    pubKey2 = priKey2 * curve.g


    end_time = time.time()

    duration = end_time - start_time
    avg += duration

avg /= count
print(avg)
print("Thời gian chạy: {:.5f} giây".format(avg))

