from analogio import AnalogIn

class AnalogueDevice(object):
    """
    wrapper for easy reading of device on an adc-pin

    usage: dev = AnalogueDevice(board.A1)
           dev.conversion = lambda val : (val / 50) + 10
           print(dev.value)

    dev.conversion to be set to conversion of digital reading to measurement
    should be specified in datasheet of device
    """
    def __init__(self,pin):
        self.pin = AnalogIn(pin)
        self.convertFunc = lambda val: val             #pin value needs to be converted via method from datasheet

    @property
    def conversion(self):
        """
        returns conversion function set previously, else default of converted reading == raw reading

        :returns: conversion function
        :rtype: function
        """
        return self.convertFunc

    @conversion.setter
    def conversion(self,func):
        """
        sets conversion function of digital reading
        should be specified in datasheet

        :param func: conversion function
        :type func: function

        :returns: nothing
        :rtype: None
        """
        #testing return value of input function
        try:
            x = func(1)
            assert type(x) == int or type(x) == float
        except (TypeError,AssertionError):
            print('Conversion function must return int or float, keeping previous / default!')
            return None

        self.convertFunc = func

    @property
    def value(self):
        """
        returns scaled and converted reading of provided pin

        :returns: reading
        :rtype: float
        """
        #digital reading needs to be set because volt. on sensor != volt. on mcu
        reading = (sum(self.pin.value for i in range(8))) / 8 #filtering reading

        scaled_reading = self.scale((0,5),(0,5),reading)
        true_val = self.convertFunc(scaled_reading) 
        #print(f'MAX. VOLT: {VOLTAGE_MAX}, CURRENT VOLT.: {VOLTAGE_NOW:.2f}')   
        #print(f'READING: {self.pin.value}, SCALED READING: {scaled_reading:.2f}, CONVERTED: {true_val:.2f}') 
        return true_val

    def scale(self,valRange,targetRange,reading):
        """
        scales the incoming voltage in relation to the mcu voltage

        :param val_range: range from 0 to voltage on device
        :param target_range: range from 0 to voltage on mcu
        :param val: reading

        :type val_range: tuple
        :type target_range: tuple
        :type val: float

        :returns: scaled reading
        :rtype: float
        """
        try:
            assert type(valRange)==tuple and type(targetRange)==tuple
        except AssertionError:
            print('Ranges should be in tuple format, returning 0!')
            return 0

        mult = (max(targetRange)-min(targetRange)) / (max(valRange)-min(valRange))
        try:
            return mult * (reading + (min(targetRange)-min(valRange)))
        except TypeError:
            print('reading argument must be able to perform arithmetically, returning 0!')
            return 0