from stm import StateMachine
import states
import times

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
            stm.next(next)
            var = rfm.receive(5)
            if stm.current == 'Empty':
                print('NO POWER')
                break
        except Exception as e:
            raise(e)

