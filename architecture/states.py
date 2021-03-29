import comms
import sensors
from power import PowerSys

class State(object):

    def __str__(self):
        return self.__name__



class Comms(State):

    def execute(self):
        """execute state-specific functions"""
        comms.transmit()

class Idle(State):

    def execute(self):
        """execute state-specific functions"""
        pass

class LowPower(State):

    def execute(self):
        """execute state-specific functions"""
        pass

class Empty(State):

    def execute(self):
        """execute state-specific functions"""
        pass

class Tumble(State):

    def execute(self):
        """execute state-specific functions"""
        pass

class SolarMax(State):

    def execute(self):
        """execute state-specific functions"""
        PowerSys.charge()

STATES = {state.__name__ : state for state in [Comms, Idle, LowPower, Tumble, SolarMax, Empty]}