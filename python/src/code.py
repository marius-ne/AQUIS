import board
import time
import busio
import struct
from rtc import RTC
from mpu_6050 import MPU #driver for MPU-6050 gyro & accelerometer

#time in 01-01-2000 epoch, starts at power-on
clock = RTC()
now = clock.datetime

#initialize i2c bus
i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
while not busio.I2C.try_lock(i2c):
    pass



if __name__ == '__main__':
    try:
        mpu = MPU(i2c)

        mpu.sleep = 0                       #wake up
        time.sleep(0.1)

        mpu.accel_range = 3                 #set range to +-16g, 2048LSB/g
        time.sleep(0.1)

        mpu.gyro_range = 3                  #set range to +-2000°/s, 16.4LSB/°/s
        time.sleep(0.1)

        while True:
            #plot gyro readout of mpu
            print(mpu.gyro)

            time.sleep(0.1)
    finally:
        i2c.unlock()