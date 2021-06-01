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
            print('Voltage reached 0.')
            return states.STATES['Empty']
        elif volt < self.VOLT_THRESH:
            print(f'Voltage fell below {self.VOLT_THRESH}, entering LowPower.')
            return states.STATES['LowPower']
        elif gyro > self.TUMBLE_THRESH:
            print(f'Gyro rose above {self.TUMBLE_THRESH}, entering Tumble.')
            return states.STATES['Tumble']
        elif photo > self.SOLAR_THRESH:
            print(f'Light-level rose above {self.SOLAR_THRESH}, entering SolarMax.')
            return states.STATES['SolarMax']
        elif comms:
            print(f'Antenna recognized signal, entering comms.')
            return states.STATES['Comms']
        else:
            print('No thresholds reached, staying idle.')
            return states.STATES['Idle']

    def next(self, state):
        self.current = state.__name__
        string = f'ENTERING {state.__name__}.'
        for k,v in self.READINGS.items():
            string += f'{k}: {v}'
        log(self.READINGS)
        state().execute()