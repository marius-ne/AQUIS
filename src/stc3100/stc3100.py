from i2c_api import get_bits, set_bits, byte_read, byte_write, byte_change
import struct

#datasheet can be found here: https://www.st.com/resource/en/application_note/cd00248578-using-the-stc3100-battery-monitor-for-gas-gauge-applications-stmicroelectronics.pdf

STC_ADDRESS = 0x70

REG_MODE = 0
REG_CTRL = 1
CHARGE_L = 2
CHARGE_H = 3
COUNTER_L = 4
COUNTER_H = 5
CURRENT_L = 6
CURRENT_H = 7
VOLTAGE_L = 8
VOLTAGE_H = 9
TEMP_L = 10
TEMP_H = 11

class STC3100(object):

    def __init__(self,i2c):
        self.i2c = i2c

    @property
    def charge(self):
        EXT_R = 50 #external resistance in milliohm
        charge_bytes = byte_read(self.i2c,STC_ADDRESS,CHARGE_H,CHARGE_L,len_array=1) #read charge registers
        charge = struct.unpack('>h',charge_bytes)[0]                               #first item because unpack returns tuple

        charge = (charge * 6.7) / EXT_R                                             #conversion according to sect. 2.2 register-map
        return charge