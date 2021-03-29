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
        try:
            next = stm.find()
            print(next)
            stm.next(next)
            if stm.current == 'Empty':
                print('NO POWER')
                break
        except Exception as e:
            raise(e)