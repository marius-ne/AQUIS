import sensors
import states
import random

TUMBLE_THRESH = random.choice([i for i in range(2**16)])
VOLT_THRESH = random.choice([i for i in range(2**16)])


class StateMachine(object):

    def __init__(self):
        pass

    def find(self):
        readings = sensors.read_all()
        gyro = readings['mpu_6050'][0]
        volt = readings['stc_3100'][1]
        comms = readings['antenna']
        if gyro > TUMBLE_THRESH:
            return states.STATES['Tumble']
        elif volt < VOLT_THRESH:
            return states.STATES['LowPower']
        elif comms:
            return states.STATES['Comms']
        else:
            return states.STATES['Idle']

    def next(self, state):
        self.current = state.__name__
        try:
            state.execute()
        except Exception as e:
            return False, e
        return True, 0