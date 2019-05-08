import serial
import string
import binascii
import threading
import time
import binascii

def temperture_process(k):
    i = 1
    IN = {}
    x = {}
    for i in range(17):
        IN[i] = k[4 * i + 4:4 * i + 8]
        x[i] = int(IN[i], 16)
        if x[i] == 64536:
            x[i] = 0
        x[i] = x[i] / 10
    return x

'''
将温度模块返回的数据处理成实际温度  
k="b'020320fc18fc18fc18fc18fc18fc18fc18fc18fc18fc18fc18fc18fc18fc18fc1801090e24'"
'''
def moni_process(k):
    i = 1
    MO = {}
    x = {}
    for i in range(9):
        MO[i] = k[4*i+4:4*i+8]
        x[i] = int(MO[i],16)
        if i<=4:
            x[i] = x[i]/204.75
        else:
            x[i] = x[i]/819
    return x
'''
将模拟量采集模块返回的数据处理成实际电流电压值
k = "b'0304100001000100010001009b008000b200946ce6'"
'''



s = serial.Serial('COM4',9600)   #设置串口
temperture = bytes.fromhex('02 03 00 20 00 10 45 FF')    #温度采集模块的16进制代码
# temperture = bytes.fromhex('02 03 00 20 00 01 85 F3')
moni = bytes.fromhex('03 04 00 00 00 08 F0 2E')      #模拟量采集模块的16进制代码
x = 0
f = open('temperture.txt','a')
while x<10:             #采集次数
    # t0 = time.perf_counter()
    s.write(temperture)
    temperture_get = s.read(37)
    str_temperture_get = str(binascii.b2a_hex(temperture_get))
    real_temperture = temperture_process(str_temperture_get)
    # str_ordata = str(ordata,'utf-8')
    # str_ordata = str(ordata,encoding='gbk')
    # print(type(temperture_get))
    #     # print(type(str_temperture_get))
    #     # print(temperture_get)
    #     # print(str_temperture_get)
    for i in range(1,17):
        f.write(str(real_temperture[i]))
        f.write('\t')
    # t1 = time.perf_counter()
    # print(str(t1-t0))

    # time.sleep(0.01)
###采集温度


    s.write(moni)
    moni_get = s.read(21)
    str_moni_get = str(binascii.b2a_hex(moni_get))
    print(str_moni_get)
    real_moni = moni_process(str_moni_get)
    for i in range(1,9):
        f.write(str(real_moni[i])[0:5])
        f.write('\t')
    f.write(str(time.time()))
    f.write('\n')
    # t2 = time.perf_counter()
    # if (t1-t0)<0.1:
    #     time.sleep(t1-t0)
    x += 1
    # t3 = time.perf_counter()
    # delet_t = t3-t0
    # print(delet_t)
    #     # ordata = s.read(21)
    #     # # str_ordata = ordata.decode("utf-8")
    #     # print(type(ordata))
    #     # # print(type(str_ordata))
    #     # print(ordata)
    #     # # print(str_ordata)
    #     # # f.write(str_ordata)
    #     # time.sleep(1)
###采集模拟量

s.close()
f.close()


