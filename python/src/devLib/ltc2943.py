from python.src.devLib.i2clib import byteChange
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
CHARGE_H = 0x02

# current sensing resistor value in Ohm
R_SENSE = 0.0011

# datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/2943fa.pdf
class LTC2943():

    def __init__(self,i2c):
        self.i2c = i2c # i2c object from busio.i2c

        self.setPrescaler(2) # set prescaler to 16 (qLsb = 0.604)
        # if Qbat <= 1978mAh (qLsb * 65535/2) then the charge register may start at 0x7FFF
        self.setCharge(0x7FFF)

    # page 10
    def setADC(self,value: int):
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
        i2clib.byteChange(self.i2c,ADDR,CTRL,{2:value>>1,1:value%2})

    # page 10
    def setPrescaler(self, value: int):
        """
        Sets the value of the charge prescaler.
        Depends upon capacity of battery and R_SENSE.

        Provide decimal value of bits to be written.
        """                                # getting single bits
        i2clib.byteChange(self.i2c,ADDR,CTRL,{5:value>>2,4:(value>>1)%2,3:value%2})

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

    # page 13
    def setCharge(self, value: int):
        """
        Sets the charge that the charge register will be counting from.
        
        Provide the register value in Hex.
        """
        # setting the two charge registers
        i2clib.byteWrite(self.i2c,ADDR,CHARGE_H,value,2)

    # page 13
    def charge(self, qLsb: int) -> int:
        """
        Gets the charge from integrating current through
        the sense resistor.

        Needs the qLsb as determined by R_SENSE, Prescaler and Qbat.
        """
        bytes = i2clib.byteRead(self.i2c,ADDR,CHARGE_H,len_array=2)
        raw = struct.unpack(">H",bytes)[0] # 2 bytes, big-endian, unsigned

        return (raw / qLsb) # conversion according to datasheet

    

    

