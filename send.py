import serial
import time
import struct

# pack('hhl', 1, 2, 3)
# bytes = [0xAA, 0xBB, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x0, 0x0, 0x9, 0x0, 0x0, 0x0]
# sentbytes = bytearray(bytes)
sp = serial.Serial(port="COM4")
i = 0
i32 = 0
while 1:
   bytes = struct.pack('<BBlll', 0xAA,0xBB, i32, i, 3)
   
   sp.write(bytes)
   time.sleep(0.001)
   # bytes[5] = i
   i += 1
   i32 += 1
   if i32 == 1024:
       i32 = 0
   if i == 255:
       i = 0
