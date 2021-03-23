import comms
import sensors

class State(object):

    def __str__(self):
        return self.__name__



class Comms(State):

    def execute(self):
        """execute state-specific functions"""
        readings = sensors.read_all()
        data = comms.encode(readings)
        comms.transmit(data)

class Idle(State):

    def execute(self):
        """execute state-specific functions"""
        pass

class LowPower(State):

    def execute(self):
        """execute state-specific functions"""
        pass

class Tumble(State):

    def execute(self):
        """execute state-specific functions"""
        pass

STATES = {state.__name__ : state for state in [Comms, Idle, LowPower, Tumble]}