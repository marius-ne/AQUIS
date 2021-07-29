from mpu_6050 import MPU
from analogue import Analogue_Device
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from analogio import AnalogIn
from hd44780 import HD44780

ow_bus = OneWireBus(board.A5)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
while not busio.I2C.try_lock(i2c):
    pass

lcd = HD44780(i2c=i2c,address=0x27,trans_map={"°":223})

mpu = MPU(i2c)
phototrans = Analogue_Device(board.A3)

POWER = 500

def mpu_6050():
    return mpu.gyro

def stc_3100():
    global POWER
    POWER -= 1
    return POWER

def ds18b20():
    return ds18.temperature

def light():
    return phototrans.value

# def antenna():
#     """search for groundstation"""
#     return random.choice([True, False])

SENSORS = [mpu_6050, stc_3100, ds18b20, light]

def read_all():
    vals = {}
    for f in SENSORS:
        vals[f.__name__] = f()
    return vals

