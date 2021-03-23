from stm import StateMachine
import states
import time

stm = StateMachine()

def setup():
    """enter initial state,
       burn wires holding antenna,
       wait for commands,
       verify everything working"""
    stm.next(states.STATES['Idle'])
    ...

if __name__ == "__main__":
    setup()

    while True:
        next = stm.find()
        print(next)
        stm.next(next)
        time.sleep(0.1)