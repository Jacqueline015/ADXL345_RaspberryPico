from machine import Pin
from machine import I2C
import time
import ustruct

DATA_FORMAT         = 0x31
BW_RATE             = 0x2c
POWER_CTL           = 0x2d
INT_ENABLE          = 0x2E

BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09

RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03

OFSX = 0x1e
OFSY =0x1f
OFSZ =0x20

class adxl345:
    def __init__(self, scl, sda):
        self.scl = scl
        self.sda = sda
        self.i2c = I2C(0,scl = self.scl, sda = self.sda, freq = 100000)
        slv = self.i2c.scan()
        for s in slv:
            buf = self.i2c.readfrom_mem(s, 0, 1)
            if(buf[0] == 0xe5):
                self.slvAddr = s
                print('adxl345 found')
            break
        #self.writeByte(POWER_CTL,0x00)  #sleep
        #time.sleep(0.001)
        self.writeByte(DATA_FORMAT,0x2B)
        self.writeByte(BW_RATE,0x0A)
        self.writeByte(INT_ENABLE,0x00)

        self.writeByte(OFSX,0x00)
        self.writeByte(OFSY,0x00)
        self.writeByte(OFSZ,0x00)

        self.writeByte(POWER_CTL,0x28)
        time.sleep(1)

    def readXYZ(self):
        fmt = '<h' #little-endian
        buf1 = self.readByte(0x32)
        buf2 = self.readByte(0x33)
        buf = bytearray([buf1[0], buf2[0]])
        x, = ustruct.unpack(fmt, buf)
        x = x*3.9

        buf1 = self.readByte(0x34)
        buf2 = self.readByte(0x35)
        buf = bytearray([buf1[0], buf2[0]])
        y, = ustruct.unpack(fmt, buf)
        y = y*3.9

        buf1 = self.readByte(0x36)
        buf2 = self.readByte(0x37)
        buf = bytearray([buf1[0], buf2[0]])
        z, = ustruct.unpack(fmt, buf)
        z = z*3.9
        return (x,y,z)

    def writeByte(self, addr, data):
        d = bytearray([data])
        self.i2c.writeto_mem(self.slvAddr, addr, d)

    def readByte(self, addr):
        return self.i2c.readfrom_mem(self.slvAddr, addr, 1)



    
    
    
scl = Pin(17)
sda = Pin(16)
snsr = adxl345(scl, sda)

LED = Pin(13, Pin.OUT)
LED.off()

valores = 10
sumax = 0.0
sumay = 0.0
sumaz = 0.0 
#i = 0
#promediox = 0.0
#promedioy = 0.0
#promedioz = 0.0
#promedioxa = 0.0
#promedioya = 0.0
#promedioza = 0.0

for i in range(10):
        x,y,z = snsr.readXYZ()
         
        sumax += x
        sumay += y
        sumaz += z
        time.sleep(0.1)

promedioxa = sumax / valores
promedioya = sumay /valores
promedioza = sumaz / valores

while True:
    sumax = 0.0
    sumay = 0.0
    sumaz = 0.0
    
    for i in range(10):
        x,y,z = snsr.readXYZ()
         
        sumax += x
        sumay += y
        sumaz += z
        time.sleep(0.1)

    promediox = sumax / valores
    promedioy = sumay /valores
    promedioz = sumaz / valores
    diferencia = promedioz - promedioza
    #if (promediox - promedioxa) >=100 or (promedioy - promedioya) >=100 or (promedioz - promedioza) >= 100:
    if diferencia >= 100:
        LED.on()
    
    promedioxa = promediox
    promedioya = promedioy
    promedioza = promedioz
    
    print("promedio actual")
    #print('x:',promediox,'y:',promedioy,'z:',promedioz)
    print('z:',promedioz)
    print("promedio anterior")
    #print('x:',promedioxa,'y:',promedioya,'z:',promedioza)
    print('z:',promedioza)
    #print('x:',x,'y:',y,'z:',z,'uint:mg')
    print(diferencia)

    