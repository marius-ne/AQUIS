from i2c_api import get_bits, set_bits, byte_read, byte_write, byte_change
import struct

#see register-map under https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
MPU_ADDRESS = 0x68
WHO_AM_I =  0x75
PWR_MGMNT = 0x6b
GEN_CFG = 0x1a

ACCELX_H =  0x3b
ACCELX_L = 0x3c
ACCELY_H = 0x3d
ACCELY_L = 0x3e
ACCELZ_H = 0x3f
ACCELZ_L = 0x40

ACCEL_CFG = 0x1c

TEMP_H = 0x41
TEMP_L = 0x42

GYROX_H =  0x43
GYROX_L = 0x44
GYROY_H = 0x45
GYROY_L = 0x46
GYROZ_H = 0x47
GYROZ_L = 0x48

GYRO_CFG = 0x1b


class MPU(object):
    """
    driver class for MPU-6050 gyroscope & accelerometer
    
    returns gyro and accelerometer measurements with mpu.gyro and mpu.accel respectively
    
    initialize with busio.I2C object
    """

    def __init__(self,i2c):
        self.i2c = i2c

    @property
    def temperature(self):
        """
        returns current temperature of MPU-6050
        """
        temp_bytes = byte_read(self.i2c,MPU_ADDRESS,TEMP_H,TEMP_L,len_array=1) #read temperature registers
        temp = struct.unpack('>h',temp_bytes)[0]                               #first item because unpack returns tuple

        temp = (temp / 340) +36.53                                             #conversion according to sect. 4.18 register-map
        return temp

    @property
    def sleep(self):
        """
        returns current sleep state of MPU-6050
        """
        sleep_byte = byte_read(self.i2c,MPU_ADDRESS,PWR_MGMNT,len_array=1)     #read sleep register
        sleep = struct.unpack('>B',sleep_byte)[0]

        self.sleep_state = get_bits(sleep,6)                                   #sleep state in bit position 6 of register
        return self.sleep_state

    @sleep.setter
    def sleep(self,value):
        """
        input value of 0 wakes up MPU-6050
        value of 1 puts mpu to sleep
        """
        byte_change(self.i2c,MPU_ADDRESS,PWR_MGMNT,value,6)

        self.sleep_state = value

    @property
    def accel_range(self):
        """
        returns current range / sensitivity of accelerometer
        
        see sect. 4.5 & 4.17 of register-map
        """
        cfg_byte = byte_read(self.i2c,MPU_ADDRESS,ACCEL_CFG,len_array=1)
        cfg = struct.unpack('>B',cfg_byte)[0]

        range_int = int(''.join([str(bit) for bit in get_bits(cfg,4,3)]),2)
        self.accel_range_state = range_int
        return range_int

    @accel_range.setter
    def accel_range(self,range_int):
        """
        sets new range / sensitivity values
        takes AFS_SEL value
        see sect. 4.5 & 4.17 register-map
        """
        byte_change(self.i2c,MPU_ADDRESS,ACCEL_CFG,range_int,3,4)

        self.accel_range_state = range_int

    @property
    def accel(self):
        """
        returns current acceleration measurement of the form:
        
        (X, Y, Z) in m/s^2
        """
        accel_bytes_x = byte_read(self.i2c,MPU_ADDRESS,ACCELX_H,ACCELX_L,len_array=1)
        accel_bytes_y = byte_read(self.i2c,MPU_ADDRESS,ACCELY_H,ACCELY_L,len_array=1)
        accel_bytes_z = byte_read(self.i2c,MPU_ADDRESS,ACCELZ_H,ACCELZ_L,len_array=1)

        accel_x = struct.unpack('>h',accel_bytes_x)[0]
        accel_y = struct.unpack('>h',accel_bytes_y)[0]
        accel_z = struct.unpack('>h',accel_bytes_z)[0]

        try:
            range_factor = 3 - self.accel_range_state
            scale = 2 ** range_factor
        except AttributeError:
            self.accel_range_state = 3
            range_factor = 3 - self.accel_range_state
            scale = 2 ** range_factor

        return (accel_x / (2048*scale)) * 9.81, (accel_y / (2048*scale)) * 9.81, (accel_z / (2048*scale)) * 9.81

    @property
    def gyro_range(self):
        """
        returns current range / sensitivity of gyro
        
        see sect. 4.4 & 4.19 of register-map
        """
        cfg_byte = byte_read(self.i2c,MPU_ADDRESS,GYRO_CFG,len_array=1)
        cfg = struct.unpack('>B',cfg_byte)[0]

        range_int = int(''.join([str(bit) for bit in get_bits(cfg,4,3)]),2)
        self.gyro_range_state = range_int
        return range_int

    @gyro_range.setter
    def gyro_range(self,range_int):
        """
        sets new range / sensitivity values
        takes FS_SEL value
        see sect. 4.4 & 4.19 register-map
        """
        byte_change(self.i2c,MPU_ADDRESS,GYRO_CFG,range_int,3,4)

        self.gyro_range_state = range_int

    @property
    def gyro(self):
        """
        returns current gyro measurement of the form:
        
        (X, Y, Z) in °/s
        """
        gyro_bytes_x = byte_read(self.i2c,MPU_ADDRESS,GYROX_H,GYROX_L,len_array=1)
        gyro_bytes_y = byte_read(self.i2c,MPU_ADDRESS,GYROY_H,GYROY_L,len_array=1)
        gyro_bytes_z = byte_read(self.i2c,MPU_ADDRESS,GYROZ_H,GYROZ_L,len_array=1)

        gyro_x = struct.unpack('>h',gyro_bytes_x)[0]
        gyro_y = struct.unpack('>h',gyro_bytes_y)[0]
        gyro_z = struct.unpack('>h',gyro_bytes_z)[0]

        try:
            range_factor = 3 - self.gyro_range_state
            scale = 2 ** range_factor
        except AttributeError:
            self.gyro_range_state = 3
            range_factor = 3 - self.gyro_range_state
            scale = 2 ** range_factor

        return (gyro_x / (250*scale)), (gyro_y / (250*scale)), (gyro_z / (250*scale))

    @property
    def dlpf(self):
        """
        returns current state of the difital low pass filter
        
        see sect. 4.3 of register-map
        """
        cfg_byte = byte_read(self.i2c,MPU_ADDRESS,GEN_CFG,len_array=1)
        cfg = struct.unpack('>B',cfg_byte)[0]

        dlpf_int = int(''.join([str(bit) for bit in get_bits(cfg,0,1,2)]),2)
        self.dlpf_state = dlpf_int
        return self.dlpf_state

    @dlpf.setter
    def dlpf(self,value):
        """
        sets new state of the difital low pass filter
        takes DLPF_CFG value
        see sect. 4.3 of register-map
        """
        byte_change(self.i2c,MPU_ADDRESS,GEN_CFG,value,0,1,2)

        self.dlpf_state = value
