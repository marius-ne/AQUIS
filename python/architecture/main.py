from stm import StateMachine

stm = StateMachine()

def setup():
    """enter initial state,
       burn wires holding antenna,
       wait for commands,
       verify everything working"""
    pass

if __name__ == "__main__":
    setup()

    while True:
        try:
            next = stm.find()
            stm.next(next)
            if stm.current == 'Empty':
                print('NO POWER')
                break
        except Exception as e:
            raise(e)

