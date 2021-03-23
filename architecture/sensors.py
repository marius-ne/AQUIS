import random
from analogue import Analogue_Device, Pin

MPU_PIN = 1
STC_PIN = 2
mpu = Analogue_Device(Pin(MPU_PIN))
stc = Analogue_Device(Pin(STC_PIN))



def mpu_6050():
    return [mpu.value for i in range(3)]

def stc_3100():
    return [stc.value for i in range(3)]

def antenna():
    """search for groundstation"""
    return random.choice([True, False])



SENSORS = [mpu_6050, stc_3100, antenna]

def read_all():
    vals = {}
    for f in SENSORS:
        vals[f.__name__] = f()
    return vals



if __name__ == '__main__':
    print(read_all())

