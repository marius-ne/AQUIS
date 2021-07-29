import sensors

"""
0 Empty
1 LowPower
2 Tumble
3 SolarMax
4 Overheat
5 Idle
"""
STATES = {0: "Empty", 1: "LowPower", 2: "Tumble", 3: "SolarMax", 4: "Overheat"}
FUNCS = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

class StateMachine(object):

    def __init__(self):
        self.TUMBLE_THRESH = 15
        self.VOLT_THRESH = 200
        self.SOLAR_THRESH = (2**16) / 2
        self.TEMP_THRESH = 30
        self.READINGS = {}

    def find(self):
        readings = sensors.read_all()
        self.READINGS = readings
        
        gyro = readings['mpu_6050']
        volt = readings['stc_3100']
        photo = readings['light']
        temp = readings['ds18b20']
        if volt == 0:
            print('Voltage reached 0.')
            return 0
        elif volt < self.VOLT_THRESH:
            print(f'Voltage fell below {self.VOLT_THRESH}, entering LowPower.')
            return 1
        elif sum(gyro) > self.TUMBLE_THRESH:
            print(f'Gyro rose above {self.TUMBLE_THRESH}, entering Tumble.')
            return 2
        elif photo > self.SOLAR_THRESH:
            print(f'Light-level rose above {self.SOLAR_THRESH}, entering SolarMax.')
            return 3
        elif temp > self.TEMP_THRESH:
            print(f'Temperature rose above {self.TEMP_THRESH} entering Overheat.')
            return 4
        else:
            print('No thresholds reached, staying idle.')
            return 5

    def next(self, state):
        self.current = state
        # string = f'ENTERING {STATES[state]}.'
        # for k,v in self.READINGS.items():
        #     string += f'{k}: {v}'
        #log(self.READINGS)             #logging the readings
        for func in FUNCS[state]:
            func()