import i2clib
import struct
import os
import numpy as np

# important numbers
ADDR = 0x64

# registers
CTRL = 0x01
VOLT_H = 0x08
TEMP_H = 0x14

# datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/2943fa.pdf
class LTC2943():

    def __init__(self,i2c):
        self.i2c = i2c # i2c object from busio.i2c

    # page 10
    def setSleep(self,value: int):
        """
        Sets the operating mode of the ADC.

        Parameters
        -----
        value : 3 automatic, 2 scan, 1 manual, 0 sleep
        """
                                            # way to get bits from decimal
        i2clib.byteChange(self.i2c,ADDR,CTRL,{7:value//2,6:value%2})
    
    # page 10
    def setShutdown(self,value: int):
        """
        Sets the operating mode of the analog circuitry (for power saving).
        
        Parameters
        -----
        value : 0 on, 1 off
        """
        i2clib.byteChange(self.i2c,ADDR,CTRL,{0:value})

    # page 10
    def setAlarm(self,value: int):
        """
        Sets the operating mode of the alarm.
        Input of 3 is forbidden.
        
        Parameters 
        -----
        value : 2 alert mode, 1 charge complete mode, 0 off"""
                                            # way to get bits from decimal
        i2clib.byteChange(self.i2c,ADDR,CTRL,{2:value//2,1:value%2})

    # page 13
    def voltage(self) -> int:
        """
        Gets the voltage (Volts) from the voltage registers.
        """
        bytes = i2clib.byteRead(self.i2c,ADDR,VOLT_H,len_array=2)
        raw = struct.unpack(">H",bytes)[0] # 2 bytes, big-endian, unsigned

        return 23.6 * (raw / 65535) # conversion according to datasheet

    # page 14
    def temperature(self) -> int:
        """
        Gets the temperature (Kelvin) from the temperature registers.
        """
        bytes = i2clib.byteRead(self.i2c,ADDR,TEMP_H,len_array=2)
        raw = struct.unpack(">H",bytes)[0] # 2 bytes, big-endian, unsigned

        return 510 * (raw / 65535) # conversion according to datasheet

    

    

