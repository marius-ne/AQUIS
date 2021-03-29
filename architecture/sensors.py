import random
import time
from analogue import Analogue_Device, Pin

MPU_PIN = 1
STC_PIN = 2
PHOTO_PIN = 3
mpu = Analogue_Device(Pin(MPU_PIN))
stc = Analogue_Device(Pin(STC_PIN))
phototrans = Analogue_Device(Pin(PHOTO_PIN))

POWER = 500

def mpu_6050():
    return [mpu.value for i in range(3)]

def stc_3100():
    global POWER
    POWER -= 1
    return POWER

def photo():
    return [phototrans.value for i in range(3)] 

def antenna():
    """search for groundstation"""
    return random.choice([True, False])



SENSORS = [mpu_6050, stc_3100, photo, antenna]

def read_all():
    vals = {}
    for f in SENSORS:
        vals[f.__name__] = f()
    return vals



if __name__ == '__main__':
    while True:
        print(read_all())
        time.sleep(1)

