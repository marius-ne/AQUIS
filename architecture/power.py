from random import choice
from numpy import arange

class PowerSys(object):

    #voltage on mcu, determines adc max value
    VOLTAGE_MAX = 4.2  

    @property
    def voltage(self):                                      
        VOLTAGE_NOW = choice([f for f in arange(1.0,4.0,0.1)])  #voltage on sensor
        return VOLTAGE_NOW

    @classmethod
    def charge(cls):
        """Charge batteries"""
        pass
