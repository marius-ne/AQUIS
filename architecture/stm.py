import sensors
import states
import random
from log import log



class StateMachine(object):

    def __init__(self):
        self.TUMBLE_THRESH = (2**16) / 1.5
        self.VOLT_THRESH = 200
        self.SOLAR_THRESH = (2**16) / 2
        self.READINGS = {}

    def find(self):
        readings = sensors.read_all()
        self.READINGS = readings
        
        gyro = readings['mpu_6050'][0]
        volt = readings['stc_3100']
        photo = readings['photo'][2]
        comms = readings['antenna']
        if volt == 0:
            return states.STATES['Empty']
        elif volt < self.VOLT_THRESH:
            return states.STATES['LowPower']
        elif gyro > self.TUMBLE_THRESH:
            return states.STATES['Tumble']
        elif photo > self.SOLAR_THRESH:
            return states.STATES['SolarMax']
        elif comms:
            return states.STATES['Comms']
        else:
            return states.STATES['Idle']

    def next(self, state):
        self.current = state.__name__
        string = f'ENTERING {state.__name__}.'
        for k,v in self.READINGS.items():
            string += f'{k}: {v}'
        log(self.READINGS)
        state().execute()