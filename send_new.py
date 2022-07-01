import serial
import time
import struct
import numpy as np

# bytes = bytearray([0xAA, 0xBB, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x0, 0x0, 0x9, 0x0, 0x0, 0x0])
sp = serial.Serial(port="COM4")

nsamples = 1024
Fs = 1024
F = 1
A = 32768
index = 0

ttt = np.arange(nsamples, dtype=np.float64) / Fs
data = A*np.sin(2*np.pi*F*ttt)
data += np.random.normal(size=data.shape)

oldTime = time.perf_counter()
while 1:
    curTime = time.perf_counter()
    timeDelta = curTime - oldTime
    if (timeDelta > 0.001):
        oldTime = curTime
        
        bytes = struct.pack('<BBlll', 0xAA,0xBB, 1, 20, int(data[index]))
        sp.write(bytes)
        
        index += 1
        if index == 1024:
            index = 0
